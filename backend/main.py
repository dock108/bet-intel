"""
AI-Assisted Peer-to-Peer Betting Intelligence - Backend
Main FastAPI application entry point
"""

# Weighted fair odds logic has been phased out, but some fields remain for
# backward compatibility. Unused sections are marked accordingly.

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone, timedelta
import pytz
import logging
import sys
import os

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import settings
    from database import (
        get_db, initialize_database, EventModel, OddsSnapshotModel, 
        PollingLogModel, EVCalculationModel, BookmakerModel
    )
    from odds_poller import OddsPoller
    from odds_analyzer import (
        aggregate_event_odds,
        find_positive_ev_opportunities,
        PotentialOpportunity
    )
    from ev_calculator import get_ev_calculations_from_db
except ImportError:
    from .config import settings
    from .database import (
        get_db, initialize_database, EventModel, OddsSnapshotModel, 
        PollingLogModel, EVCalculationModel, BookmakerModel
    )
    from .odds_poller import OddsPoller
    from .odds_analyzer import (
        aggregate_event_odds,
        find_positive_ev_opportunities,
        PotentialOpportunity
    )
    from .ev_calculator import get_ev_calculations_from_db

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)

# Timezone utility functions
def get_local_timezone():
    """Get the user's local timezone. Defaults to US/Eastern for sports betting."""
    try:
        # Try to get system timezone
        return pytz.timezone('US/Eastern')  # Sports betting is often US-focused
    except Exception:
        return pytz.UTC

def convert_to_local_time(utc_time_str):
    """Convert UTC time string to local timezone."""
    if not utc_time_str:
        return None
    
    try:
        # Parse the UTC time (assume it's UTC if no timezone info)
        if isinstance(utc_time_str, str):
            dt = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        else:
            dt = utc_time_str
            
        # If no timezone info, assume UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
            
        # Convert to local timezone
        local_tz = get_local_timezone()
        local_dt = dt.astimezone(local_tz)
        
        return local_dt.isoformat()
    except Exception as e:
        logger.warning(f"Failed to convert time {utc_time_str}: {e}")
        return utc_time_str

def is_game_live(commence_time):
    """Check if a game is currently live (started within last 4 hours)."""
    if not commence_time:
        return False
        
    try:
        if isinstance(commence_time, str):
            dt = datetime.fromisoformat(commence_time.replace('Z', '+00:00'))
        else:
            dt = commence_time
            
        # If no timezone, assume UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
            
        now = datetime.now(timezone.utc)
        
        # Game is live if it started in the last 4 hours (typical game duration + buffer)
        return dt <= now <= (dt + timedelta(hours=4))
    except Exception as e:
        logger.warning(f"Failed to check if game is live for {commence_time}: {e}")
        return False

app = FastAPI(
    title="AI-Assisted P2P Betting Intelligence",
    description="Backend API for P2P betting intelligence platform",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and perform startup tasks"""
    logger.info("Starting up application...")
    initialize_database()
    logger.info("Database initialized successfully")

@app.get("/")
async def root():
    """Root endpoint for API health check"""
    return {"message": "AI-Assisted P2P Betting Intelligence API", "status": "active"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "p2p-betting-intelligence"}

@app.get("/api/events")
async def get_events(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent events from database"""
    try:
        events = db.query(EventModel).order_by(EventModel.created_at.desc()).limit(limit).all()
        return {
            "events": [
                {
                    "id": event.id,
                    "external_id": event.external_id,
                    "sport": event.sport_key,
                    "home_team": event.home_team,
                    "away_team": event.away_team,
                    "commence_time": event.commence_time.isoformat() if event.commence_time else None,
                    "created_at": event.created_at.isoformat() if event.created_at else None
                }
                for event in events
            ],
            "total": len(events)
        }
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        raise HTTPException(status_code=500, detail="Error fetching events")

@app.get("/api/ev-opportunities")
async def get_ev_opportunities(
    limit: int = Query(default=20, ge=1, le=100, description="Maximum number of events to return"),
    offset: int = Query(default=0, ge=0, description="Number of events to skip for pagination"),
    sport_key: Optional[str] = Query(default=None, description="Filter by sport key (e.g., 'baseball_mlb')"),
    bookmaker_key: Optional[str] = Query(default=None, description="Filter by bookmaker key (e.g., 'draftkings')"),
    market_key: str = Query(default="h2h", description="Market type (default: h2h for moneyline)"),
    positive_ev_only: bool = Query(default=False, description="Only return events with positive EV opportunities"),
    exclude_live_games: bool = Query(default=True, description="Exclude games that have already started"),
    min_ev_threshold: Optional[float] = Query(default=None, description="Minimum EV threshold (e.g., 5.0 for $5+ EV)"),
    ev_method: str = Query(default="any", description="EV method for threshold: 'standard', 'no_vig', or 'any'"),
    db: Session = Depends(get_db)
):
    """
    Get events with their Expected Value (EV) calculations across all three methods:
    - Standard EV (with vig)
    - No-Vig EV (vig-removed fair odds)
    
    Returns structured data showing betting opportunities and value analysis with pagination support.
    
    ## Examples:
    
    ### Basic Usage:
    ```
    GET /api/ev-opportunities
    ```
    Returns first 20 events with all EV calculations.
    
    ### Pagination:
    ```
    GET /api/ev-opportunities?limit=10&offset=20
    ```
    Returns events 21-30 (third page with 10 per page).
    
    ### Filter by Sport:
    ```
    GET /api/ev-opportunities?sport_key=baseball_mlb&limit=5
    ```
    Returns first 5 MLB games with EV calculations.
    
    
    ### Bookmaker-Specific Analysis:
    ```
    GET /api/ev-opportunities?bookmaker_key=draftkings&min_ev_threshold=5.0&ev_method=any
    ```
    Returns DraftKings opportunities with any EV method >= $5.
    
    ## Response Format:
    Returns events array with complete EV analysis, pagination info, and opportunity summaries.
    """
    try:
        logger.info(f"EV opportunities request: limit={limit}, offset={offset}, sport={sport_key}, "
                    f"bookmaker={bookmaker_key}, min_ev={min_ev_threshold}, method={ev_method}")
        
        # Validate EV method parameter
        valid_ev_methods = ['any', 'standard', 'no_vig']
        if ev_method not in valid_ev_methods:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid ev_method. Must be one of: {', '.join(valid_ev_methods)}"
            )
        
        # Build base query for events
        query = db.query(EventModel).filter(EventModel.completed.is_(False))
        
        if sport_key:
            # Validate sport key exists
            valid_sports = ['baseball_mlb', 'basketball_nba', 'americanfootball_nfl', 'icehockey_nhl']
            if sport_key not in valid_sports:
                logger.warning(f"Potentially invalid sport_key: {sport_key}")
            query = query.filter(EventModel.sport_key == sport_key)
        
        # Get total count for pagination info
        total_events = query.count()
        
        # Order by commence time (soonest first) and apply pagination
        events = query.order_by(EventModel.commence_time.asc()).offset(offset).limit(limit).all()
        
        if not events:
            return {
                "events": [],
                "total": 0,
                "pagination": {
                    "limit": limit,
                    "offset": offset,
                    "total_events": total_events,
                    "has_next": False,
                    "has_previous": offset > 0
                },
                "message": "No active events found matching criteria"
            }
        
        ev_opportunities = []
        
        for event in events:
            try:
                # Filter out live games if requested
                if exclude_live_games and is_game_live(event.commence_time):
                    logger.debug(f"Skipping live game: {event.home_team} vs {event.away_team}")
                    continue
                
                # Get EV calculations for this event
                ev_calculations = get_ev_calculations_from_db(
                    db=db,
                    event_external_id=event.external_id,
                    bookmaker_key=bookmaker_key,
                    market_key=market_key
                )
                
                if not ev_calculations:
                    # If no EV calculations exist, still include event with empty calculations
                    if not positive_ev_only and min_ev_threshold is None:
                        ev_opportunities.append({
                            "event": {
                                "external_id": event.external_id,
                                "sport_key": event.sport_key,
                                "sport_title": event.sport_title,
                                "home_team": event.home_team,
                                "away_team": event.away_team,
                                "commence_time": convert_to_local_time(event.commence_time),
                                "is_live": is_game_live(event.commence_time)
                            },
                            "ev_calculations": [],
                            "opportunities_summary": {
                                "total_bookmakers": 0,
                                "positive_standard_ev_count": 0,
                                "positive_no_vig_ev_count": 0,
                                "best_standard_ev": None,
                                "best_no_vig_ev": None,
                                "meets_threshold": False
                            }
                        })
                    continue
                
                # Apply EV threshold filtering
                if min_ev_threshold is not None:
                    threshold_met = False
                    for calc in ev_calculations:
                        if _meets_ev_threshold(calc, min_ev_threshold, ev_method):
                            threshold_met = True
                            break
                    
                    if not threshold_met:
                        continue
                
                # Group calculations by bookmaker
                bookmaker_calculations = {}
                for calc in ev_calculations:
                    bookmaker_key_calc = calc['bookmaker']['key']
                    if bookmaker_key_calc not in bookmaker_calculations:
                        bookmaker_calculations[bookmaker_key_calc] = {
                            "bookmaker": calc['bookmaker'],
                            "outcomes": []
                        }
                    bookmaker_calculations[bookmaker_key_calc]["outcomes"].append({
                        "outcome_name": calc['outcome_name'],
                        "outcome_index": calc['outcome_index'],
                        "offered_odds": calc['offered_odds'],
                        "standard_ev": calc['standard_ev'],
                        "no_vig_ev": calc['no_vig_ev'],
                        "standard_implied_probability": calc['standard_implied_probability'],
                        "no_vig_fair_probability": calc['no_vig_fair_probability'],
                        "no_vig_fair_odds": calc['no_vig_fair_odds'],
                        "vig_percentage": calc['vig_percentage'],
                        "has_positive_standard_ev": calc['has_positive_standard_ev'],
                        "has_positive_no_vig_ev": calc['has_positive_no_vig_ev'],
                        "calculated_at": calc['calculated_at'].isoformat() if calc['calculated_at'] else None
                    })
                
                # Calculate opportunities summary
                summary = _calculate_opportunities_summary(ev_calculations)
                
                # Add threshold information to summary
                if min_ev_threshold is not None:
                    summary['meets_threshold'] = any(
                        _meets_ev_threshold(calc, min_ev_threshold, ev_method) 
                        for calc in ev_calculations
                    )
                    summary['threshold_details'] = {
                        'min_ev_threshold': min_ev_threshold,
                        'ev_method': ev_method
                    }
                else:
                    summary['meets_threshold'] = True
                
                # Apply positive EV filter if requested
                if positive_ev_only and (
                    summary['positive_standard_ev_count'] == 0 and
                    summary['positive_no_vig_ev_count'] == 0
                ):
                    continue
                
                ev_opportunities.append({
                    "event": {
                        "external_id": event.external_id,
                        "sport_key": event.sport_key,
                        "sport_title": event.sport_title,
                        "home_team": event.home_team,
                        "away_team": event.away_team,
                        "commence_time": convert_to_local_time(event.commence_time),
                        "is_live": is_game_live(event.commence_time)
                    },
                    "ev_calculations": list(bookmaker_calculations.values()),
                    "opportunities_summary": summary
                })
                
            except Exception as e:
                logger.error(f"Error processing EV calculations for event {event.external_id}: {e}")
                # Continue processing other events rather than failing entirely
                continue
        
        # Calculate pagination info
        has_next = (offset + limit) < total_events
        has_previous = offset > 0
        
        return {
            "events": ev_opportunities,
            "total": len(ev_opportunities),
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total_events": total_events,
                "returned_events": len(ev_opportunities),
                "has_next": has_next,
                "has_previous": has_previous,
                "next_offset": offset + limit if has_next else None,
                "previous_offset": max(0, offset - limit) if has_previous else None
            },
            "filters_applied": {
                "sport_key": sport_key,
                "bookmaker_key": bookmaker_key,
                "market_key": market_key,
                "positive_ev_only": positive_ev_only,
                "exclude_live_games": exclude_live_games,
                "min_ev_threshold": min_ev_threshold,
                "ev_method": ev_method,
                "limit": limit,
                "offset": offset
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "ev_methods": {
                    "standard_ev": "Expected value using raw bookmaker odds (includes vig)",
                    "no_vig_ev": "Expected value using vig-removed fair odds"
                },
                "pagination_note": f"Showing events {offset + 1}-{offset + len(ev_opportunities)} of {total_events} total events"
            }
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching EV opportunities: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while fetching EV opportunities. Please try again later."
        )


def _meets_ev_threshold(calc: dict, threshold: float, method: str) -> bool:
    """Check if a calculation meets the specified EV threshold."""
    if method == 'any':
        return (
            (calc.get('standard_ev') is not None and calc['standard_ev'] >= threshold) or
            (calc.get('no_vig_ev') is not None and calc['no_vig_ev'] >= threshold)
        )
    elif method == 'standard':
        return calc.get('standard_ev') is not None and calc['standard_ev'] >= threshold
    elif method == 'no_vig':
        return calc.get('no_vig_ev') is not None and calc['no_vig_ev'] >= threshold
    else:
        return False

def _calculate_opportunities_summary(ev_calculations: List[dict]) -> dict:
    """Calculate summary statistics for EV opportunities."""
    summary = {
        "total_bookmakers": 0,
        "positive_standard_ev_count": 0,
        "positive_no_vig_ev_count": 0,
        "best_standard_ev": None,
        "best_no_vig_ev": None
    }
    
    if not ev_calculations:
        return summary
    
    bookmakers = set()
    best_standard = None
    best_no_vig = None
    
    for calc in ev_calculations:
        bookmakers.add(calc['bookmaker']['key'])
        
        # Count positive EVs
        if calc['has_positive_standard_ev']:
            summary['positive_standard_ev_count'] += 1
        if calc['has_positive_no_vig_ev']:
            summary['positive_no_vig_ev_count'] += 1
        
        # Track best EVs
        if calc['standard_ev'] is not None:
            if best_standard is None or calc['standard_ev'] > best_standard['ev']:
                best_standard = {
                    "ev": calc['standard_ev'],
                    "bookmaker": calc['bookmaker']['title'],
                    "outcome": calc['outcome_name'],
                    "odds": calc['offered_odds']
                }
        
        if calc['no_vig_ev'] is not None:
            if best_no_vig is None or calc['no_vig_ev'] > best_no_vig['ev']:
                best_no_vig = {
                    "ev": calc['no_vig_ev'],
                    "bookmaker": calc['bookmaker']['title'],
                    "outcome": calc['outcome_name'],
                    "odds": calc['offered_odds'],
                    "vig_percentage": calc['vig_percentage']
                }
        
    
    summary.update({
        "total_bookmakers": len(bookmakers),
        "best_standard_ev": best_standard,
        "best_no_vig_ev": best_no_vig
    })
    
    return summary

@app.get("/api/polling-logs")
async def get_polling_logs(limit: int = 20, db: Session = Depends(get_db)):
    """Get recent polling logs"""
    try:
        logs = db.query(PollingLogModel).order_by(PollingLogModel.created_at.desc()).limit(limit).all()
        return {
            "logs": [
                {
                    "id": log.id,
                    "sport_key": log.sport_key,
                    "success": log.success,
                    "response_status": log.response_status,
                    "events_count": log.events_count,
                    "response_time_ms": log.response_time_ms,
                    "requests_remaining": log.requests_remaining,
                    "error_message": log.error_message,
                    "created_at": log.created_at.isoformat() if log.created_at else None
                }
                for log in logs
            ],
            "total": len(logs)
        }
    except Exception as e:
        logger.error(f"Error fetching polling logs: {e}")
        raise HTTPException(status_code=500, detail="Error fetching polling logs")

@app.post("/api/poll-odds")
async def poll_odds_manual():
    """Manually trigger odds polling for testing"""
    try:
        logger.info("Manual odds polling triggered")
        poller = OddsPoller()
        success = poller.poll_odds_once()
        
        return {
            "success": success,
            "message": "Odds polling completed" if success else "Odds polling failed"
        }
    except Exception as e:
        logger.error(f"Error during manual polling: {e}")
        raise HTTPException(status_code=500, detail=f"Polling error: {str(e)}")

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get database statistics"""
    try:
        events_count = db.query(EventModel).count()
        odds_count = db.query(OddsSnapshotModel).count()
        logs_count = db.query(PollingLogModel).count()
        
        recent_successful_polls = db.query(PollingLogModel).filter(
            PollingLogModel.success.is_(True)
        ).order_by(PollingLogModel.created_at.desc()).limit(5).all()
        
        return {
            "events_count": events_count,
            "odds_snapshots_count": odds_count,
            "polling_logs_count": logs_count,
            "recent_successful_polls": [
                {
                    "sport_key": log.sport_key,
                    "events_count": log.events_count,
                    "created_at": log.created_at.isoformat() if log.created_at else None
                }
                for log in recent_successful_polls
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Error fetching stats")

@app.get("/api/opportunities", response_model=List[PotentialOpportunity], tags=["Analysis"])
async def get_opportunities(db: Session = Depends(get_db)):
    """
    Fetches all currently detected positive EV opportunities.
    This endpoint iterates through all non-completed events, aggregates their odds,
    and then runs the discrepancy detection logic.
    """
    logger.info("Received request for /api/opportunities")
    opportunities: List[PotentialOpportunity] = []
    
    active_events = db.query(EventModel).filter(EventModel.completed.is_(False)).all()
    if not active_events:
        logger.info("No active events found to analyze for opportunities.")
        return []

    logger.info(f"Found {len(active_events)} active events to analyze.")

    for event_db in active_events:
        logger.debug(f"Analyzing event: {event_db.external_id} ({event_db.home_team} vs {event_db.away_team})")
        aggregated_odds_data = aggregate_event_odds(db, event_db.id)
        if aggregated_odds_data:
            event_opportunities = find_positive_ev_opportunities(aggregated_odds_data, db)
            if event_opportunities:
                opportunities.extend(event_opportunities)
                logger.info(f"Found {len(event_opportunities)} opportunities for event {event_db.external_id}")
        else:
            logger.warning(f"Could not aggregate odds for event ID {event_db.id}, skipping opportunity analysis for it.")
            
    logger.info(f"Total opportunities found across all events: {len(opportunities)}")
    if not opportunities:
        # Return 200 with empty list if no opportunities, which is valid
        logger.info("No opportunities found after analysis.")

    return opportunities

@app.get("/api/events-with-ev")
async def get_events_with_ev(
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    sport_key: Optional[str] = Query(None),
    min_ev: Optional[float] = Query(-1000),
    db: Session = Depends(get_db)
):
    """
    Get events with their EV calculations for the frontend
    """
    try:
        # Base query for events
        events_query = db.query(EventModel)
        
        # Apply sport filter
        if sport_key:
            events_query = events_query.filter(EventModel.sport_key == sport_key)
        
        # Get events with pagination
        events = events_query.order_by(EventModel.commence_time).offset(offset).limit(limit).all()
        
        result_events = []
        
        for event in events:
            # Get EV calculations for this event
            ev_calcs = db.query(EVCalculationModel).join(BookmakerModel).filter(
                EVCalculationModel.event_id == event.id
            ).all()
            
            # Group EV calculations by bookmaker
            bookmaker_data = {}
            best_ev = -float('inf')
            
            for ev_calc in ev_calcs:
                bookmaker_key = ev_calc.bookmaker.key
                if bookmaker_key not in bookmaker_data:
                    bookmaker_data[bookmaker_key] = {
                        'bookmaker': {
                            'key': ev_calc.bookmaker.key,
                            'title': ev_calc.bookmaker.title,
                            'is_p2p': ev_calc.bookmaker.is_p2p
                        },
                        'outcomes': []
                    }
                
                # Track best EV for filtering
                if ev_calc.standard_ev and ev_calc.standard_ev > best_ev:
                    best_ev = ev_calc.standard_ev
                
                bookmaker_data[bookmaker_key]['outcomes'].append({
                    'outcome_name': ev_calc.outcome_name,
                    'outcome_index': ev_calc.outcome_index,
                    'offered_odds': ev_calc.offered_odds,
                    'standard_ev': ev_calc.standard_ev,
                    'no_vig_ev': ev_calc.no_vig_ev,
                    'has_positive_ev': ev_calc.has_positive_standard_ev
                })
            
            # Apply EV filter
            if best_ev >= min_ev:
                result_events.append({
                    'event': {
                        'id': event.id,
                        'external_id': event.external_id,
                        'sport_key': event.sport_key,
                        'sport_title': event.sport_title,
                        'home_team': event.home_team,
                        'away_team': event.away_team,
                        'commence_time': event.commence_time.isoformat(),
                        'completed': event.completed
                    },
                    'ev_calculations': list(bookmaker_data.values()),
                    'best_ev': best_ev
                })
        
        return {
            'events': result_events,
            'total': len(result_events),
            'pagination': {
                'limit': limit,
                'offset': offset,
                'returned_events': len(result_events)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/future-games-with-ev")
async def get_future_games_with_ev(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get future games with comprehensive EV analysis from all core bookmakers
    """
    try:
        # Core 6 bookmakers for comprehensive analysis
        CORE_BOOKMAKERS = {
            'pinnacle': 'Pinnacle',
            'draftkings': 'DraftKings', 
            'fanduel': 'FanDuel',
            'novig': 'Novig',
            'prophetx': 'ProphetX',
            'betopenly': 'BetOpenly'
        }
        
        # Get future events only
        current_time = datetime.now(timezone.utc)
        future_events = db.query(EventModel).filter(
            EventModel.commence_time > current_time
        ).order_by(EventModel.commence_time).limit(limit).all()
        
        events_with_comprehensive_ev = []
        for event in future_events:
            # Get all EV calculations for this event
            ev_calcs = db.query(EVCalculationModel).join(BookmakerModel).filter(
                EVCalculationModel.event_id == event.id
            ).all()
            
            # Group by bookmaker and outcome
            bookmaker_data = {}
            for ev in ev_calcs:
                bookmaker_key = ev.bookmaker.key
                
                # Only include core bookmakers
                if bookmaker_key not in CORE_BOOKMAKERS:
                    continue
                    
                if bookmaker_key not in bookmaker_data:
                    bookmaker_data[bookmaker_key] = {
                        "bookmaker": {
                            "key": bookmaker_key,
                            "title": CORE_BOOKMAKERS[bookmaker_key],
                            "is_p2p": ev.bookmaker.is_p2p
                        },
                        "outcomes": {}
                    }
                
                outcome_key = ev.outcome_name
                if outcome_key not in bookmaker_data[bookmaker_key]["outcomes"]:
                    bookmaker_data[bookmaker_key]["outcomes"][outcome_key] = []
                
                # Parse the detailed calculation if available
                calculation_details = {}
                if ev.calculation_method_details:
                    try:
                        import json
                        calculation_details = json.loads(ev.calculation_method_details)
                    except (json.JSONDecodeError, TypeError):
                        calculation_details = {}
                
                bookmaker_data[bookmaker_key]["outcomes"][outcome_key].append({
                    "offered_odds": ev.offered_odds,
                    "ev_percentage": round(ev.standard_ev, 2),
                    "has_positive_ev": ev.has_positive_standard_ev,
                    "no_vig_fair_probability": round(ev.no_vig_fair_probability, 4),
                    "no_vig_fair_odds": round(ev.no_vig_fair_odds, 2),
                    "calculation_details": calculation_details,
                    "calculated_at": ev.created_at.isoformat()
                })
            
            # Calculate what odds would be needed for positive EV
            positive_ev_analysis = calculate_positive_ev_requirements(bookmaker_data)
            
            events_with_comprehensive_ev.append({
                "event_id": event.external_id,
                "sport": event.sport_key,
                "home_team": event.home_team,
                "away_team": event.away_team,
                "commence_time": event.commence_time.isoformat(),
                "bookmaker_analysis": bookmaker_data,
                "positive_ev_requirements": positive_ev_analysis,
                "summary": {
                    "total_bookmakers": len(bookmaker_data),
                    "positive_ev_count": sum(1 for bm_data in bookmaker_data.values() 
                                             for outcomes in bm_data["outcomes"].values() 
                                             for outcome in outcomes if outcome["has_positive_ev"]),
                    "best_available_ev": max([outcome["ev_percentage"] 
                                              for bm_data in bookmaker_data.values() 
                                              for outcomes in bm_data["outcomes"].values() 
                                              for outcome in outcomes] or [0])
                }
            })
        
        return {
            "events": events_with_comprehensive_ev,
            "total": len(events_with_comprehensive_ev),
            "methodology": {
                "core_bookmakers": CORE_BOOKMAKERS,
                "calculation_method": "7-Step No-Vig & +EV Logic",
                "explanation": "Shows comprehensive analysis from all 6 core bookmakers with detailed EV calculations"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting comprehensive EV data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve comprehensive EV data")

def calculate_positive_ev_requirements(bookmaker_data):
    """Calculate what odds would be needed for positive EV"""
    requirements = {}
    
    for bookmaker_key, bm_data in bookmaker_data.items():
        for outcome_key, outcomes in bm_data["outcomes"].items():
            for outcome in outcomes:
                if not outcome["has_positive_ev"]:
                    # Calculate what odds would give +2% EV
                    fair_prob = outcome["no_vig_fair_probability"]
                    if fair_prob > 0:
                        # For +2% EV: (1/odds - fair_prob) * 100 = 2
                        # So: 1/odds = fair_prob + 0.02
                        # Therefore: odds = 1 / (fair_prob + 0.02)
                        required_decimal_odds = 1 / (fair_prob + 0.02)
                        if required_decimal_odds > 1:
                            # Convert to American odds
                            if required_decimal_odds >= 2.0:
                                required_american_odds = int((required_decimal_odds - 1) * 100)
                            else:
                                required_american_odds = int(-100 / (required_decimal_odds - 1))
                            
                            requirements[f"{bookmaker_key}_{outcome_key}"] = {
                                "bookmaker": bm_data["bookmaker"]["title"],
                                "outcome": outcome_key,
                                "current_odds": outcome["offered_odds"],
                                "required_odds_for_2pct_ev": required_american_odds,
                                "improvement_needed": abs(required_american_odds - outcome["offered_odds"])
                            }
    
    return requirements

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 