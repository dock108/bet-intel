"""
Expected Value (EV) Calculation Service

This service handles calculating and storing EV data for all events using the corrected 7-step methodology.
Integrates with the odds polling workflow to provide accurate EV calculations.
"""

import logging
import json
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from .database import EventModel, OddsSnapshotModel, BookmakerModel, EVCalculationModel
from .ev_calculator import calculate_comprehensive_ev, store_ev_calculations_to_db

logger = logging.getLogger(__name__)


class EVCalculationService:
    """Service for calculating Expected Value using the corrected 7-step methodology"""
    
    def __init__(self):
        self.market_key = 'h2h'  # Focus on moneyline markets
        self.min_bookmakers = 2  # Minimum bookmakers required for EV calculation
        
    def calculate_evs_for_event(self, db: Session, event: EventModel) -> Dict[str, any]:
        """
        Calculate EV for a single event using the new 7-step methodology.
        
        Args:
            db: Database session
            event: Event to calculate EVs for
            
        Returns:
            Dict with calculation results and statistics
        """
        result = {
            'event_external_id': event.external_id,
            'success': False,
            'calculations_stored': 0,
            'bookmakers_processed': 0,
            'error': None
        }
        
        try:
            logger.debug(f"Calculating EVs for event: {event.home_team} vs {event.away_team}")
            
            # Get odds snapshots for this event
            h2h_snapshots = db.query(OddsSnapshotModel).filter(
                OddsSnapshotModel.event_id == event.id,
                OddsSnapshotModel.market_key == self.market_key
            ).all()
            
            if len(h2h_snapshots) < self.min_bookmakers:
                result['error'] = f"Insufficient bookmakers ({len(h2h_snapshots)} < {self.min_bookmakers})"
                return result
            
            # Group odds by bookmaker and convert to required format
            bookmaker_odds_data = self._group_odds_for_calculation(db, h2h_snapshots)
            
            if len(bookmaker_odds_data) < self.min_bookmakers:
                result['error'] = f"Insufficient valid bookmaker odds ({len(bookmaker_odds_data)} < {self.min_bookmakers})"
                return result
            
            logger.debug(f"Found odds from {len(bookmaker_odds_data)} bookmakers: {list(bookmaker_odds_data.keys())}")
            
            # Calculate EVs for each bookmaker using the 7-step methodology
            calculations_stored = 0
            bookmakers_processed = 0
            
            for bookmaker_key in bookmaker_odds_data.keys():
                try:
                    # Calculate comprehensive EV for this bookmaker
                    ev_results = calculate_comprehensive_ev(
                        bookmaker_odds_data=bookmaker_odds_data,
                        target_bookmaker=bookmaker_key,
                        is_alternate_line=False  # Assuming main lines for h2h market
                    )
                    
                    if 'error' not in ev_results:
                        # Store in database
                        stored_calcs = store_ev_calculations_to_db(
                            db=db,
                            event_external_id=event.external_id,
                            bookmaker_key=bookmaker_key,
                            market_key=self.market_key,
                            ev_results=ev_results,
                            odds_snapshot_time=None  # Will use default timestamp
                        )
                        calculations_stored += len(stored_calcs)
                        bookmakers_processed += 1
                        
                        logger.debug(f"Stored {len(stored_calcs)} EV calculations for {bookmaker_key}")
                    else:
                        logger.warning(f"EV calculation failed for {bookmaker_key}: {ev_results.get('error')}")
                    
                except Exception as e:
                    logger.error(f"Error calculating EV for {bookmaker_key}: {e}")
                    continue
            
            result['calculations_stored'] = calculations_stored
            result['bookmakers_processed'] = bookmakers_processed
            result['success'] = calculations_stored > 0
            
            if result['success']:
                logger.debug(f"Stored {calculations_stored} EV calculations for {event.external_id} "
                           f"across {bookmakers_processed} bookmakers")
            
        except Exception as e:
            logger.error(f"Error calculating EVs for event {event.external_id}: {e}")
            result['error'] = str(e)
        
        return result
    
    def calculate_evs_for_all_events(self, db: Session) -> Dict[str, any]:
        """
        Calculate EVs for all events with available odds using the 7-step methodology.
        
        Args:
            db: Database session
            
        Returns:
            Dict with calculation statistics
        """
        stats = {
            'total_events': 0,
            'events_with_evs': 0,
            'total_calculations': 0,
            'total_bookmakers_processed': 0,
            'errors': []
        }
        
        try:
            # Get all events that have odds snapshots
            events_with_odds = db.query(EventModel).join(OddsSnapshotModel).filter(
                OddsSnapshotModel.market_key == self.market_key
            ).distinct().all()
            
            stats['total_events'] = len(events_with_odds)
            logger.info(f"Starting EV calculations for {stats['total_events']} events")
            
            for event in events_with_odds:
                try:
                    event_result = self.calculate_evs_for_event(db, event)
                    
                    if event_result['success']:
                        stats['events_with_evs'] += 1
                        stats['total_calculations'] += event_result['calculations_stored']
                        stats['total_bookmakers_processed'] += event_result['bookmakers_processed']
                    else:
                        if event_result['error']:
                            stats['errors'].append({
                                'event_external_id': event.external_id,
                                'error': event_result['error']
                            })
                            
                except Exception as e:
                    error_msg = f"Failed to calculate EVs for event {event.external_id}: {e}"
                    logger.error(error_msg)
                    stats['errors'].append({
                        'event_external_id': event.external_id,
                        'error': str(e)
                    })
        
        except Exception as e:
            logger.error(f"Error in EV calculation process: {e}")
            stats['errors'].append({'global_error': str(e)})
        
        logger.info(f"EV calculation complete: {stats['events_with_evs']}/{stats['total_events']} events, "
                   f"{stats['total_calculations']} total calculations, "
                   f"{len(stats['errors'])} errors")
        
        return stats
    
    def _group_odds_for_calculation(self, db: Session, snapshots: List[OddsSnapshotModel]) -> Dict[str, Dict]:
        """
        Group odds snapshots by bookmaker and convert to format required by 7-step calculation.
        
        Returns:
            Dict of {bookmaker_key: {'odds_a': float, 'odds_b': float}}
        """
        bookmaker_odds_data = {}
        
        for snapshot in snapshots:
            bookmaker = db.query(BookmakerModel).filter(BookmakerModel.id == snapshot.bookmaker_id).first()
            if not bookmaker:
                continue
                
            try:
                outcomes = json.loads(snapshot.outcomes_data)
                if len(outcomes) >= 2:  # Need both outcomes for h2h
                    # Convert to format expected by 7-step calculation
                    bookmaker_odds_data[bookmaker.key] = {
                        'odds_a': outcomes[0]['price'],  # Away team (outcome A)
                        'odds_b': outcomes[1]['price']   # Home team (outcome B)
                    }
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                logger.warning(f"Invalid odds data in snapshot {snapshot.id}: {e}")
                continue
        
        return bookmaker_odds_data


# Convenience function for integration with odds poller
def calculate_evs_after_polling(db: Session) -> Dict[str, any]:
    """
    Calculate EVs for all events after odds polling completes using the 7-step methodology.
    
    This function is designed to be called from the odds poller
    after new odds data has been stored.
    
    Args:
        db: Database session
        
    Returns:
        Dict with calculation statistics
    """
    ev_service = EVCalculationService()
    return ev_service.calculate_evs_for_all_events(db) 