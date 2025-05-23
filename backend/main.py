"""
AI-Assisted Peer-to-Peer Betting Intelligence - Backend
Main FastAPI application entry point
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from typing import List, Optional
from datetime import datetime

from backend.config import settings
from backend.database import (
    get_db, initialize_database, EventModel, OddsSnapshotModel, 
    PollingLogModel
)
from backend.odds_poller import OddsPoller
from backend.odds_analyzer import (
    aggregate_event_odds,
    find_positive_ev_opportunities,
    PotentialOpportunity
)
from backend.ev_calculator import get_ev_calculations_from_db

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Assisted P2P Betting Intelligence",
    description="Backend API for P2P betting intelligence platform",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
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
    min_ev_threshold: Optional[float] = Query(default=None, description="Minimum EV threshold (e.g., 5.0 for $5+ EV)"),
    ev_method: str = Query(default="any", description="EV method for threshold: 'standard', 'no_vig', 'weighted_fair', or 'any'"),
    db: Session = Depends(get_db)
):
    """
    Get events with their Expected Value (EV) calculations across all three methods:
    - Standard EV (with vig)
    - No-Vig EV (vig-removed fair odds)
    - Weighted Fair Odds EV (Pinnacle 50%, DraftKings 25%, FanDuel 25%)
    
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
    
    ### High-Value Opportunities:
    ```
    GET /api/ev-opportunities?min_ev_threshold=10.0&ev_method=weighted_fair&positive_ev_only=true
    ```
    Returns events with weighted fair EV >= $10.
    
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
        valid_ev_methods = ['any', 'standard', 'no_vig', 'weighted_fair']
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
                                "commence_time": event.commence_time.isoformat() if event.commence_time else None
                            },
                            "ev_calculations": [],
                            "opportunities_summary": {
                                "total_bookmakers": 0,
                                "positive_standard_ev_count": 0,
                                "positive_no_vig_ev_count": 0,
                                "positive_weighted_fair_ev_count": 0,
                                "best_standard_ev": None,
                                "best_no_vig_ev": None,
                                "best_weighted_fair_ev": None,
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
                        "weighted_fair_ev": calc['weighted_fair_ev'],
                        "standard_implied_probability": calc['standard_implied_probability'],
                        "no_vig_fair_probability": calc['no_vig_fair_probability'],
                        "weighted_fair_probability": calc['weighted_fair_probability'],
                        "no_vig_fair_odds": calc['no_vig_fair_odds'],
                        "weighted_fair_odds": calc['weighted_fair_odds'],
                        "vig_percentage": calc['vig_percentage'],
                        "books_used_in_weighted": calc['books_used_in_weighted'],
                        "has_positive_standard_ev": calc['has_positive_standard_ev'],
                        "has_positive_no_vig_ev": calc['has_positive_no_vig_ev'],
                        "has_positive_weighted_ev": calc['has_positive_weighted_ev'],
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
                    summary['positive_no_vig_ev_count'] == 0 and
                    summary['positive_weighted_fair_ev_count'] == 0
                ):
                    continue
                
                ev_opportunities.append({
                    "event": {
                        "external_id": event.external_id,
                        "sport_key": event.sport_key,
                        "sport_title": event.sport_title,
                        "home_team": event.home_team,
                        "away_team": event.away_team,
                        "commence_time": event.commence_time.isoformat() if event.commence_time else None
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
                "min_ev_threshold": min_ev_threshold,
                "ev_method": ev_method,
                "limit": limit,
                "offset": offset
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "ev_methods": {
                    "standard_ev": "Expected value using raw bookmaker odds (includes vig)",
                    "no_vig_ev": "Expected value using vig-removed fair odds",
                    "weighted_fair_ev": "Expected value using weighted consensus (Pinnacle 50%, DK 25%, FD 25%)"
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
            (calc.get('no_vig_ev') is not None and calc['no_vig_ev'] >= threshold) or
            (calc.get('weighted_fair_ev') is not None and calc['weighted_fair_ev'] >= threshold)
        )
    elif method == 'standard':
        return calc.get('standard_ev') is not None and calc['standard_ev'] >= threshold
    elif method == 'no_vig':
        return calc.get('no_vig_ev') is not None and calc['no_vig_ev'] >= threshold
    elif method == 'weighted_fair':
        return calc.get('weighted_fair_ev') is not None and calc['weighted_fair_ev'] >= threshold
    else:
        return False

def _calculate_opportunities_summary(ev_calculations: List[dict]) -> dict:
    """Calculate summary statistics for EV opportunities."""
    summary = {
        "total_bookmakers": 0,
        "positive_standard_ev_count": 0,
        "positive_no_vig_ev_count": 0,
        "positive_weighted_fair_ev_count": 0,
        "best_standard_ev": None,
        "best_no_vig_ev": None,
        "best_weighted_fair_ev": None
    }
    
    if not ev_calculations:
        return summary
    
    bookmakers = set()
    best_standard = None
    best_no_vig = None
    best_weighted = None
    
    for calc in ev_calculations:
        bookmakers.add(calc['bookmaker']['key'])
        
        # Count positive EVs
        if calc['has_positive_standard_ev']:
            summary['positive_standard_ev_count'] += 1
        if calc['has_positive_no_vig_ev']:
            summary['positive_no_vig_ev_count'] += 1
        if calc['has_positive_weighted_ev']:
            summary['positive_weighted_fair_ev_count'] += 1
        
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
        
        if calc['weighted_fair_ev'] is not None:
            if best_weighted is None or calc['weighted_fair_ev'] > best_weighted['ev']:
                best_weighted = {
                    "ev": calc['weighted_fair_ev'],
                    "bookmaker": calc['bookmaker']['title'],
                    "outcome": calc['outcome_name'],
                    "odds": calc['offered_odds'],
                    "books_used": calc['books_used_in_weighted']
                }
    
    summary.update({
        "total_bookmakers": len(bookmakers),
        "best_standard_ev": best_standard,
        "best_no_vig_ev": best_no_vig,
        "best_weighted_fair_ev": best_weighted
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 