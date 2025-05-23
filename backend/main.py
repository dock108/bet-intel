"""
AI-Assisted Peer-to-Peer Betting Intelligence - Backend
Main FastAPI application entry point
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging

from config import settings
from database import get_db, initialize_database, EventModel, OddsSnapshotModel, PollingLogModel
from odds_poller import OddsPoller

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 