"""
Odds polling service for scheduled data collection from The Odds API
"""

import asyncio
import logging
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import sys
import os

# Add the current directory to the Python path for imports  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import settings
except ImportError:
    from .config import settings

from .database import (
    SessionLocal, EventModel, BookmakerModel, 
    OddsSnapshotModel, PollingLogModel, initialize_database
)
from .odds_api_client import OddsAPIClient, OddsAPIError, RateLimitError
from .ev_service import calculate_evs_after_polling

# Configure logger
logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)


class OddsPoller:
    """Service for polling odds data from The Odds API"""
    
    def __init__(self):
        self.client = OddsAPIClient()
        self.polling_interval = settings.odds_polling_interval_minutes * 60  # Convert to seconds
        self.default_sport = settings.default_sport
        self.default_regions = settings.default_regions
        self.default_markets = settings.default_markets
        self.is_running = False
        
        logger.info(f"Initialized OddsPoller for {self.default_sport} with {settings.odds_polling_interval_minutes} minute intervals")
    
    def get_db(self) -> Session:
        """Get database session"""
        return SessionLocal()
    
    def parse_datetime(self, datetime_str: str) -> datetime:
        """Parse ISO datetime string to datetime object"""
        return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    
    def store_event(self, db: Session, event_data: Dict[str, Any]) -> EventModel:
        """
        Store or update event information
        
        Args:
            db: Database session
            event_data: Event data from API
            
        Returns:
            EventModel instance
        """
        external_id = event_data["id"]
        
        # Check if event already exists
        existing_event = db.query(EventModel).filter(
            EventModel.external_id == external_id
        ).first()
        
        if existing_event:
            # Update existing event
            existing_event.sport_title = event_data["sport_title"]
            existing_event.home_team = event_data["home_team"]
            existing_event.away_team = event_data["away_team"]
            existing_event.commence_time = self.parse_datetime(event_data["commence_time"])
            existing_event.updated_at = datetime.now(timezone.utc)
            return existing_event
        else:
            # Create new event
            new_event = EventModel(
                external_id=external_id,
                sport_key=event_data["sport_key"],
                sport_title=event_data["sport_title"],
                home_team=event_data["home_team"],
                away_team=event_data["away_team"],
                commence_time=self.parse_datetime(event_data["commence_time"])
            )
            db.add(new_event)
            db.flush()  # Get the ID
            return new_event
    
    def get_or_create_bookmaker(self, db: Session, bookmaker_data: Dict[str, Any]) -> BookmakerModel:
        """
        Get existing bookmaker or create new one
        
        Args:
            db: Database session
            bookmaker_data: Bookmaker data from API
            
        Returns:
            BookmakerModel instance
        """
        key = bookmaker_data["key"]
        
        existing = db.query(BookmakerModel).filter(BookmakerModel.key == key).first()
        if existing:
            return existing
        
        # Create new bookmaker (shouldn't happen often with our pre-seeded data)
        new_bookmaker = BookmakerModel(
            key=key,
            title=bookmaker_data["title"],
            region="us",  # Default region, could be improved with mapping
            is_p2p=False  # Default to false, could be improved with mapping
        )
        db.add(new_bookmaker)
        db.flush()
        return new_bookmaker
    
    def store_odds_snapshot(self, 
                           db: Session, 
                           event: EventModel, 
                           bookmaker: BookmakerModel, 
                           market_data: Dict[str, Any],
                           bookmaker_last_update: str,
                           is_opening: bool = False) -> OddsSnapshotModel:
        """
        Store odds snapshot
        
        Args:
            db: Database session
            event: Event model
            bookmaker: Bookmaker model
            market_data: Market data from API
            bookmaker_last_update: Last update timestamp from bookmaker
            is_opening: Whether this is opening odds
            
        Returns:
            OddsSnapshotModel instance
        """
        snapshot = OddsSnapshotModel(
            event_id=event.id,
            bookmaker_id=bookmaker.id,
            market_key=market_data["key"],
            outcomes_data=json.dumps(market_data["outcomes"]),
            last_update=self.parse_datetime(bookmaker_last_update),
            is_opening_odds=is_opening,
            is_closing_odds=False  # Will be set later when event is about to start
        )
        
        db.add(snapshot)
        return snapshot
    
    def process_odds_data(self, db: Session, odds_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Process and store odds data from API response
        
        Args:
            db: Database session
            odds_data: List of events with odds from API
            
        Returns:
            Dictionary with processing statistics
        """
        stats = {
            "events_processed": 0,
            "odds_snapshots_created": 0,
            "errors": 0
        }
        
        for event_data in odds_data:
            try:
                # Store event
                event = self.store_event(db, event_data)
                
                # Check if this is the first time we're seeing this event (opening odds)
                existing_snapshots = db.query(OddsSnapshotModel).filter(
                    OddsSnapshotModel.event_id == event.id
                ).count()
                is_opening = existing_snapshots == 0
                
                if is_opening and not event.opening_odds_captured_at:
                    event.opening_odds_captured_at = datetime.now(timezone.utc)
                
                # Process bookmakers and markets
                for bookmaker_data in event_data.get("bookmakers", []):
                    bookmaker = self.get_or_create_bookmaker(db, bookmaker_data)
                    
                    # Process each market for this bookmaker
                    for market_data in bookmaker_data.get("markets", []):
                        self.store_odds_snapshot(
                            db=db,
                            event=event,
                            bookmaker=bookmaker,
                            market_data=market_data,
                            bookmaker_last_update=bookmaker_data["last_update"],
                            is_opening=is_opening
                        )
                        stats["odds_snapshots_created"] += 1
                
                stats["events_processed"] += 1
                
            except Exception as e:
                logger.error(f"Error processing event {event_data.get('id', 'unknown')}: {e}")
                stats["errors"] += 1
        
        # Commit all changes
        db.commit()
        return stats
    
    def log_polling_result(self, 
                          db: Session, 
                          sport_key: str,
                          regions: str,
                          markets: str,
                          url: str,
                          response_status: int,
                          success: bool,
                          error_message: Optional[str] = None,
                          events_count: int = 0,
                          response_time_ms: Optional[float] = None,
                          quota_info: Optional[Dict[str, int]] = None):
        """Log polling attempt to database"""
        
        log_entry = PollingLogModel(
            sport_key=sport_key,
            regions=regions,
            markets=markets,
            request_url=url,
            response_status=response_status,
            success=success,
            error_message=error_message,
            events_count=events_count,
            response_time_ms=response_time_ms,
            requests_remaining=quota_info.get("requests_remaining") if quota_info else None,
            requests_used=quota_info.get("requests_used") if quota_info else None,
            requests_last=quota_info.get("requests_last") if quota_info else None
        )
        
        db.add(log_entry)
        db.commit()
    
    def poll_odds_once(self) -> bool:
        """
        Perform one polling cycle
        
        Returns:
            True if successful, False otherwise
        """
        db = self.get_db()
        success = False
        
        try:
            logger.info(f"Starting odds polling for {self.default_sport}")
            
            # Fetch odds data
            odds_data = self.client.get_odds(
                sport=self.default_sport,
                regions=self.default_regions,
                markets=self.default_markets,
                odds_format=settings.odds_format
            )
            
            # Extract metadata
            metadata = odds_data.get("_metadata", {})
            
            # Handle both wrapped and direct list responses
            if "data" in odds_data and isinstance(odds_data["data"], list):
                events_data = odds_data["data"]
            elif isinstance(odds_data, list):
                events_data = odds_data
            else:
                events_data = []
            
            logger.info(f"Received {len(events_data)} events from API")
            
            # Process and store data
            if events_data:
                stats = self.process_odds_data(db, events_data)
                logger.info(f"Processing complete: {stats}")
            else:
                stats = {"events_processed": 0, "odds_snapshots_created": 0, "errors": 0}
            
            # Log successful polling
            self.log_polling_result(
                db=db,
                sport_key=self.default_sport,
                regions=self.default_regions,
                markets=self.default_markets,
                url=f"{settings.odds_api_base_url}/sports/{self.default_sport}/odds",
                response_status=200,
                success=True,
                events_count=len(events_data),
                response_time_ms=metadata.get("response_time_ms"),
                quota_info={
                    "requests_remaining": metadata.get("requests_remaining"),
                    "requests_used": metadata.get("requests_used"),
                    "requests_last": metadata.get("requests_last")
                }
            )
            
            # Calculate EV for all events after successful odds polling
            try:
                logger.info("Starting EV calculations after odds polling...")
                ev_stats = calculate_evs_after_polling(db)
                logger.info(f"EV calculation complete: {ev_stats['events_with_evs']}/{ev_stats['total_events']} events, "
                           f"{ev_stats['total_calculations']} calculations using methods: "
                           f"{ev_stats['probability_methods']}")
            except Exception as e:
                logger.error(f"Error during EV calculation: {e}")
                # Don't fail the entire polling cycle for EV calculation errors
            
            success = True
            
        except RateLimitError as e:
            logger.warning(f"Rate limit hit: {e}")
            self.log_polling_result(
                db=db, sport_key=self.default_sport, regions=self.default_regions,
                markets=self.default_markets, url="rate_limited", response_status=429,
                success=False, error_message=str(e)
            )
            
        except OddsAPIError as e:
            logger.error(f"API error during polling: {e}")
            self.log_polling_result(
                db=db, sport_key=self.default_sport, regions=self.default_regions,
                markets=self.default_markets, url="api_error", response_status=500,
                success=False, error_message=str(e)
            )
            
        except Exception as e:
            logger.error(f"Unexpected error during polling: {e}")
            self.log_polling_result(
                db=db, sport_key=self.default_sport, regions=self.default_regions,
                markets=self.default_markets, url="unknown_error", response_status=500,
                success=False, error_message=str(e)
            )
            
        finally:
            db.close()
        
        return success
    
    async def start_polling(self):
        """Start the polling loop"""
        self.is_running = True
        logger.info(f"Starting odds polling every {settings.odds_polling_interval_minutes} minutes")
        
        while self.is_running:
            try:
                success = self.poll_odds_once()
                
                if success:
                    logger.info("Polling cycle completed successfully")
                else:
                    logger.warning("Polling cycle completed with errors")
                
                # Wait for next polling interval
                logger.info(f"Waiting {settings.odds_polling_interval_minutes} minutes until next poll")
                await asyncio.sleep(self.polling_interval)
                
            except KeyboardInterrupt:
                logger.info("Polling stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    def stop_polling(self):
        """Stop the polling loop"""
        self.is_running = False
        logger.info("Odds polling stopped")


async def main():
    """Main function for running the odds poller"""
    # Initialize database
    initialize_database()
    
    # Create and start poller
    poller = OddsPoller()
    
    try:
        await poller.start_polling()
    except KeyboardInterrupt:
        logger.info("Shutting down odds poller")
    finally:
        poller.stop_polling()


if __name__ == "__main__":
    asyncio.run(main()) 