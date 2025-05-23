import logging
from typing import List, Optional, Dict
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import json
import sys
import os

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import get_settings
except ImportError:
    from .config import get_settings

from .database import EventModel, OddsSnapshotModel, BookmakerModel

logger = logging.getLogger(__name__)
settings = get_settings()

# --- Pydantic Models for Structured Odds Data ---

class OutcomeOdds(BaseModel):
    name: str
    price: float
    point: Optional[float] = None

class MarketOdds(BaseModel):
    market_key: str  # e.g., 'h2h', 'spreads', 'totals'
    outcomes: List[OutcomeOdds]
    last_update: datetime

class BookmakerEventOdds(BaseModel):
    bookmaker_key: str
    bookmaker_title: str
    is_p2p: bool
    markets: List[MarketOdds]

class AggregatedEventOdds(BaseModel):
    event_id: str  # external_id from Event model
    sport_key: str
    sport_title: str
    home_team: str
    away_team: str
    commence_time: datetime
    bookmakers_odds: List[BookmakerEventOdds]

class PotentialOpportunity(BaseModel):
    event_id: str
    sport_key: str
    home_team: str
    away_team: str
    commence_time: datetime
    market_key: str
    outcome_name: str
    bookmaker_key: str  # The bookmaker offering the favorable odds
    bookmaker_odds: float
    reference_odds: float  # e.g., average market odds, or specific non-p2p bookmaker
    potential_ev: Optional[float] = None  # Calculated Expected Value
    p2p_offerable_price: Optional[float] = None  # Price user could offer on P2P
    description: str  # e.g., "Sportsbook X offers better odds than market average" or "P2P offer possible"
    snapshot_time: datetime

# --- Odds Aggregation Logic ---

def aggregate_event_odds(db: Session, event_db_id: int) -> Optional[AggregatedEventOdds]:
    """
    Aggregates all odds snapshots for a given event from the database.
    """
    event = db.query(EventModel).filter(EventModel.id == event_db_id).first()
    if not event:
        logger.warning(f"Event with DB ID {event_db_id} not found for aggregation.")
        return None

    logger.info(f"Aggregating odds for event: {event.external_id} ({event.home_team} vs {event.away_team})")

    snapshots = db.query(OddsSnapshotModel).filter(OddsSnapshotModel.event_id == event_db_id).order_by(OddsSnapshotModel.bookmaker_id, OddsSnapshotModel.last_update.desc()).all()

    if not snapshots:
        logger.info(f"No odds snapshots found for event {event.external_id}")
        return AggregatedEventOdds(
            event_id=event.external_id,
            sport_key=event.sport_key,
            sport_title=event.sport_title,
            home_team=event.home_team,
            away_team=event.away_team,
            commence_time=event.commence_time,
            bookmakers_odds=[]
        )

    # Group snapshots by bookmaker
    bookmakers_data_map: Dict[int, BookmakerEventOdds] = {}

    for snap in snapshots:
        bookmaker_db = db.query(BookmakerModel).filter(BookmakerModel.id == snap.bookmaker_id).first()
        if not bookmaker_db:
            logger.warning(f"Bookmaker with ID {snap.bookmaker_id} not found for snapshot {snap.id}. Skipping.")
            continue

        if snap.bookmaker_id not in bookmakers_data_map:
            bookmakers_data_map[snap.bookmaker_id] = BookmakerEventOdds(
                bookmaker_key=bookmaker_db.key,
                bookmaker_title=bookmaker_db.title,
                is_p2p=bookmaker_db.is_p2p,
                markets=[]
            )
        
        # Ensure outcomes_data is valid JSON and parse it
        try:
            outcomes_list = json.loads(snap.outcomes_data)
            if not isinstance(outcomes_list, list):
                logger.warning(f"Parsed outcomes_data is not a list for snapshot {snap.id}. Skipping. Data: {snap.outcomes_data}")
                continue
        except json.JSONDecodeError:
            logger.error(f"Failed to parse outcomes_data for snapshot {snap.id}. Data: {snap.outcomes_data}")
            continue
            
        market_outcomes = []
        for outcome_data in outcomes_list:
            if not isinstance(outcome_data, dict) or "name" not in outcome_data or "price" not in outcome_data:
                logger.warning(f"Invalid outcome data format in snapshot {snap.id}: {outcome_data}. Skipping.")
                continue
            market_outcomes.append(
                OutcomeOdds(
                    name=outcome_data["name"],
                    price=float(outcome_data["price"]),
                    point=float(outcome_data.get("point")) if outcome_data.get("point") is not None else None,
                )
            )

        # Add market to the bookmaker, ensuring we only add the latest for each market_key
        existing_market_keys = {m.market_key for m in bookmakers_data_map[snap.bookmaker_id].markets}
        if snap.market_key not in existing_market_keys:
            bookmakers_data_map[snap.bookmaker_id].markets.append(
                MarketOdds(
                    market_key=snap.market_key,
                    outcomes=market_outcomes,
                    last_update=snap.last_update
                )
            )
        # If market_key exists, we assume snapshots are ordered by last_update desc,
        # so the first one encountered is the latest.

    return AggregatedEventOdds(
        event_id=event.external_id,
        sport_key=event.sport_key,
        sport_title=event.sport_title,
        home_team=event.home_team,
        away_team=event.away_team,
        commence_time=event.commence_time,
        bookmakers_odds=list(bookmakers_data_map.values())
    )

# --- Discrepancy Detection Logic ---

def calculate_reference_odds(db: Session, aggregated_event: AggregatedEventOdds, target_outcome_name: str, market_key: str) -> Optional[float]:
    """
    Calculates reference odds for a specific outcome from active, non-P2P, US-region bookmakers.
    Filters bookmakers from the provided AggregatedEventOdds.
    """
    prices: List[float] = []
    logger.debug(f"Calculating reference odds for outcome '{target_outcome_name}' in market '{market_key}' for event '{aggregated_event.event_id}'")

    active_us_non_p2p_bookmaker_keys = {
        b.key for b in db.query(BookmakerModel)
        .filter(BookmakerModel.active.is_(True), BookmakerModel.is_p2p.is_(False), BookmakerModel.region == 'us')
        .all()
    }

    if not active_us_non_p2p_bookmaker_keys:
        logger.warning("No active, non-P2P, US-region bookmakers found in the database to calculate reference odds.")
        return None

    for bookmaker_odds_data in aggregated_event.bookmakers_odds:
        if bookmaker_odds_data.bookmaker_key not in active_us_non_p2p_bookmaker_keys:
            logger.debug(f"Skipping bookmaker {bookmaker_odds_data.bookmaker_key} (not active/non-P2P/US) for reference odds calculation.")
            continue

        for market in bookmaker_odds_data.markets:
            if market.market_key == market_key:
                for outcome in market.outcomes:
                    if outcome.name == target_outcome_name:
                        prices.append(outcome.price)
                        logger.debug(f"Included price {outcome.price} from {bookmaker_odds_data.bookmaker_key} for {target_outcome_name}")
                        break  # Found outcome in this market for this bookie
                break  # Found market for this bookie

    if not prices:
        logger.info(f"No prices found from active US non-P2P bookmakers for outcome '{target_outcome_name}' in market '{market_key}' for event '{aggregated_event.event_id}'")
        return None

    reference_price = sum(prices) / len(prices)
    logger.info(f"Calculated reference odds for '{target_outcome_name}' in market '{market_key}' for event '{aggregated_event.event_id}': {reference_price:.2f} from {len(prices)} prices.")
    return reference_price

def find_positive_ev_opportunities(
    aggregated_odds: AggregatedEventOdds,
    db: Session, 
    p2p_commission_rate: float = settings.P2P_COMMISSION_RATE,
    ev_threshold: float = 0.01  # Minimum 1% EV to be considered an opportunity
) -> List[PotentialOpportunity]:
    """
    Identifies potential positive EV opportunities by comparing bookmaker odds
    against reference odds or identifying P2P opportunities.
    """
    opportunities: List[PotentialOpportunity] = []
    logger.info(f"Finding EV opportunities for event: {aggregated_odds.event_id} with EV threshold {ev_threshold} and P2P commission {p2p_commission_rate}")

    for bookie_data in aggregated_odds.bookmakers_odds:
        # We don't evaluate P2P bookies against reference odds derived from traditional ones
        # P2P bookies will be evaluated for offering better odds than traditional ones later.
        # if bookie_data.is_p2p:
        #     continue

        for market in bookie_data.markets:
            for outcome in market.outcomes:
                reference_price = calculate_reference_odds(
                    db=db, 
                    aggregated_event=aggregated_odds, 
                    target_outcome_name=outcome.name, 
                    market_key=market.market_key
                )

                if reference_price is None:
                    logger.debug(f"No reference price for {outcome.name} in {market.market_key}, event {aggregated_odds.event_id}. Skipping EV calc for {bookie_data.bookmaker_key}")
                    continue

                current_bookie_price = outcome.price

                is_opportunity = False
                description = ""
                
                if not bookie_data.is_p2p:
                    if current_bookie_price > 0 and reference_price > 0:
                        if current_bookie_price > reference_price * (1 + ev_threshold):
                            is_opportunity = True
                            description = f"{bookie_data.bookmaker_title} offers significantly better positive odds ({current_bookie_price}) than reference ({reference_price:.2f})."
                    elif current_bookie_price < 0 and reference_price < 0:  # Both are negative (underdog prices)
                        if abs(current_bookie_price) < abs(reference_price) * (1 - ev_threshold):  # e.g. -110 vs -130 average
                            is_opportunity = True
                            description = f"{bookie_data.bookmaker_title} offers significantly better negative odds ({current_bookie_price}) than reference ({reference_price:.2f})."

                if is_opportunity:
                    opportunity = PotentialOpportunity(
                        event_id=aggregated_odds.event_id,
                        sport_key=aggregated_odds.sport_key,
                        home_team=aggregated_odds.home_team,
                        away_team=aggregated_odds.away_team,
                        commence_time=aggregated_odds.commence_time,
                        market_key=market.market_key,
                        outcome_name=outcome.name,
                        bookmaker_key=bookie_data.bookmaker_key,
                        bookmaker_odds=current_bookie_price,
                        reference_odds=reference_price,
                        potential_ev=None,  # To be calculated properly later
                        p2p_offerable_price=None,  # To be calculated later
                        description=description,
                        snapshot_time=market.last_update  # Time of the snapshot for this market data
                    )
                    opportunities.append(opportunity)
                    notify_opportunity(opportunity)

    logger.info(f"Found {len(opportunities)} potential EV opportunities for event {aggregated_odds.event_id}")
    return opportunities

# --- Alerting & Logging ---

def notify_opportunity(opportunity: PotentialOpportunity):
    """
    Placeholder for a notification function.
    Currently, it just logs the opportunity.
    """
    logger.info(f"NOTIFICATION - New Opportunity Detected: {opportunity.model_dump_json(indent=2)}")

if __name__ == '__main__':
    # Example usage (for testing purposes)
    # This would require a mock DB setup or connection to a live one
    logging.basicConfig(level=logging.INFO)
    logger.info("Odds Analyzer module loaded.")
    # Mock data or test DB calls would go here
    # example_event_id = "some_event_external_id"
    # with next(get_db()) as db:
    #     event = db.query(EventModel).filter(EventModel.external_id == example_event_id).first()
    #     if event:
    #         aggregated = aggregate_event_odds(db, event.id)
    #         if aggregated:
    #             opportunities = find_positive_ev_opportunities(aggregated, db)
    #             logger.info(f"Found {len(opportunities)} opportunities.")
    #         else:
    #             logger.warning(f"Could not aggregate odds for event {example_event_id}")
    #     else:
    #         logger.warning(f"Event {example_event_id} not found.") 