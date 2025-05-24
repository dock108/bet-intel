"""
Database models and configuration for the betting intelligence platform
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
import logging
import os
import sys

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import settings with fallback for relative imports
try:
    from config import settings
except ImportError:
    from .config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()


class SportModel(Base):
    """Model for sports available in the system"""
    __tablename__ = "sports"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    group = Column(String(100))
    description = Column(String(255))
    active = Column(Boolean, default=True)
    has_outrights = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    events = relationship("EventModel", back_populates="sport")


class EventModel(Base):
    """Model for sports events/games"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(100), unique=True, index=True, nullable=False)  # API event ID
    sport_key = Column(String(50), ForeignKey("sports.key"), nullable=False)
    sport_title = Column(String(100), nullable=False)
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    commence_time = Column(DateTime(timezone=True), nullable=False)
    completed = Column(Boolean, default=False)
    
    # Opening and closing odds timestamps for analytics
    opening_odds_captured_at = Column(DateTime(timezone=True))
    closing_odds_captured_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sport = relationship("SportModel", back_populates="events")
    odds_snapshots = relationship("OddsSnapshotModel", back_populates="event")
    ev_calculations = relationship("EVCalculationModel", back_populates="event")


class BookmakerModel(Base):
    """Model for bookmakers/sportsbooks"""
    __tablename__ = "bookmakers"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    region = Column(String(10), nullable=False)  # us, uk, eu, au
    is_p2p = Column(Boolean, default=False)  # True for P2P exchanges
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    odds_snapshots = relationship("OddsSnapshotModel", back_populates="bookmaker")
    ev_calculations = relationship("EVCalculationModel", back_populates="bookmaker")


class OddsSnapshotModel(Base):
    """Model for storing odds snapshots with full historical data"""
    __tablename__ = "odds_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    bookmaker_id = Column(Integer, ForeignKey("bookmakers.id"), nullable=False)
    
    # Market information
    market_key = Column(String(50), nullable=False)  # h2h, spreads, totals
    
    # Outcomes data (stored as JSON-like text for flexibility)
    outcomes_data = Column(Text, nullable=False)  # JSON string of outcomes
    
    # Odds metadata
    last_update = Column(DateTime(timezone=True), nullable=False)  # From bookmaker
    snapshot_time = Column(DateTime(timezone=True), server_default=func.now())  # When we captured it
    
    # Flags for opening/closing odds
    is_opening_odds = Column(Boolean, default=False)
    is_closing_odds = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    event = relationship("EventModel", back_populates="odds_snapshots")
    bookmaker = relationship("BookmakerModel", back_populates="odds_snapshots")

    # Composite index for efficient queries
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )


class EVCalculationModel(Base):
    """Model for storing multiple Expected Value calculations for each event/bookmaker/market combination"""
    __tablename__ = "ev_calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    bookmaker_id = Column(Integer, ForeignKey("bookmakers.id"), nullable=False)
    market_key = Column(String(50), nullable=False)  # h2h, spreads, totals
    
    # Outcome information
    outcome_name = Column(String(100), nullable=False)  # Team name or outcome description
    outcome_index = Column(Integer, nullable=False)  # 0 for outcome A, 1 for outcome B, etc.
    offered_odds = Column(Float, nullable=False)  # American odds offered by bookmaker
    
    # Three types of EV calculations
    standard_ev = Column(Float)  # EV using raw bookmaker odds (with vig)
    no_vig_ev = Column(Float)    # EV using vig-removed fair odds
    
    # Supporting data for each calculation method
    standard_implied_probability = Column(Float)  # Implied probability from raw odds
    no_vig_fair_probability = Column(Float)      # Fair probability after vig removal
    
    # Reference odds used in calculations
    no_vig_fair_odds = Column(Float)      # Fair odds after vig removal
    
    # Calculation metadata
    calculation_method_details = Column(Text)  # JSON string with calculation details
    vig_percentage = Column(Float)        # Vig percentage for no-vig calculation
    
    # Timestamps
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    odds_snapshot_time = Column(DateTime(timezone=True))  # When the odds were captured
    
    # Quality indicators
    has_positive_standard_ev = Column(Boolean, default=False)
    has_positive_no_vig_ev = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    event = relationship("EventModel", back_populates="ev_calculations")
    bookmaker = relationship("BookmakerModel", back_populates="ev_calculations")

    # Composite index for efficient queries
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )


class PollingLogModel(Base):
    """Model for tracking API polling status and errors"""
    __tablename__ = "polling_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    sport_key = Column(String(50), nullable=False)
    regions = Column(String(100), nullable=False)
    markets = Column(String(100), nullable=False)
    
    # Request details
    request_url = Column(String(500), nullable=False)
    response_status = Column(Integer, nullable=False)
    
    # API quota tracking
    requests_remaining = Column(Integer)
    requests_used = Column(Integer)
    requests_last = Column(Integer)
    
    # Success/error tracking
    success = Column(Boolean, nullable=False)
    error_message = Column(Text)
    events_count = Column(Integer, default=0)
    
    # Performance metrics
    response_time_ms = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_bookmakers(db):
    """Initialize bookmakers table with common sportsbooks"""
    bookmakers_data = [
        # US Sportsbooks
        {"key": "draftkings", "title": "DraftKings", "region": "us", "is_p2p": False},
        {"key": "fanduel", "title": "FanDuel", "region": "us", "is_p2p": False},
        {"key": "caesars", "title": "Caesars", "region": "us", "is_p2p": False},
        {"key": "betmgm", "title": "BetMGM", "region": "us", "is_p2p": False},
        {"key": "pointsbetus", "title": "PointsBet (US)", "region": "us", "is_p2p": False},
        {"key": "betrivers", "title": "BetRivers", "region": "us", "is_p2p": False},
        {"key": "unibet", "title": "Unibet", "region": "us", "is_p2p": False},
        
        # P2P Exchanges
        {"key": "sporttrade", "title": "Sporttrade", "region": "us", "is_p2p": True},
        {"key": "prophetx", "title": "ProphetX", "region": "us", "is_p2p": True},
        {"key": "novig", "title": "Novig", "region": "us", "is_p2p": True},
        
        # International
        {"key": "pinnacle", "title": "Pinnacle", "region": "eu", "is_p2p": False},
        {"key": "betfair", "title": "Betfair", "region": "uk", "is_p2p": True},
    ]
    
    for bm_data in bookmakers_data:
        existing = db.query(BookmakerModel).filter(BookmakerModel.key == bm_data["key"]).first()
        if not existing:
            bookmaker = BookmakerModel(**bm_data)
            db.add(bookmaker)
    
    db.commit()


def init_sports(db):
    """Initialize sports table with common sports"""
    sports_data = [
        {"key": "basketball_nba", "title": "NBA", "group": "Basketball", 
         "description": "US Basketball", "active": True, "has_outrights": False},
        {"key": "americanfootball_nfl", "title": "NFL", "group": "American Football",
         "description": "US Football", "active": True, "has_outrights": False},
        {"key": "baseball_mlb", "title": "MLB", "group": "Baseball",
         "description": "Major League Baseball", "active": True, "has_outrights": False},
        {"key": "icehockey_nhl", "title": "NHL", "group": "Ice Hockey",
         "description": "US Ice Hockey", "active": True, "has_outrights": False},
    ]
    
    for sport_data in sports_data:
        existing = db.query(SportModel).filter(SportModel.key == sport_data["key"]).first()
        if not existing:
            sport = SportModel(**sport_data)
            db.add(sport)
    
    db.commit()


def initialize_database():
    """Initialize database with tables and default data"""
    create_tables()
    db = SessionLocal()
    try:
        init_bookmakers(db)
        init_sports(db)
    finally:
        db.close() 