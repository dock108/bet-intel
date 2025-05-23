# Odds Aggregation & Discrepancy Detection

This document outlines the system for aggregating odds data from various snapshots and the initial logic for detecting discrepancies or potential positive expected value (EV) opportunities.

## 1. Data Aggregation

Odds data, once polled and stored as individual `OddsSnapshot` records, needs to be aggregated to provide a comprehensive view for each event. This allows for easier comparison across bookmakers and markets.

### Key Pydantic Schemas

The following Pydantic models are defined in `backend/odds_analyzer.py` to structure the aggregated data:

1.  **`OutcomeOdds`**: Represents a single outcome within a market.
    ```python
    class OutcomeOdds(BaseModel):
        name: str  # Name of the outcome (e.g., team name, "Over", "Under")
        price: float # Odds price (American odds format)
        point: Optional[float] = None # Point for spreads/totals
    ```

2.  **`MarketOdds`**: Represents all outcomes for a specific market (e.g., h2h, spreads) from a single bookmaker.
    ```python
    class MarketOdds(BaseModel):
        market_key: str  # e.g., 'h2h', 'spreads', 'totals'
        outcomes: List[OutcomeOdds]
        last_update: datetime # Timestamp of the last odds update for this market
    ```

3.  **`BookmakerEventOdds`**: Contains all market odds from a single bookmaker for a specific event.
    ```python
    class BookmakerEventOdds(BaseModel):
        bookmaker_key: str
        bookmaker_title: str
        is_p2p: bool # True if the bookmaker is a peer-to-peer exchange
        markets: List[MarketOdds]
    ```

4.  **`AggregatedEventOdds`**: The top-level model for an event, containing its details and a list of `BookmakerEventOdds`.
    ```python
    class AggregatedEventOdds(BaseModel):
        event_id: str # The unique external_id of the event
        sport_key: str
        sport_title: str
        home_team: str
        away_team: str
        commence_time: datetime
        bookmakers_odds: List[BookmakerEventOdds] # List of odds from all relevant bookmakers
    ```

### Aggregation Logic (`aggregate_event_odds` function)

The `aggregate_event_odds(db: Session, event_db_id: int) -> Optional[AggregatedEventOdds]` function in `backend/odds_analyzer.py` performs the following steps:
1.  Fetches the `Event` details from the database using its internal database ID (`event_db_id`).
2.  Retrieves all `OddsSnapshot` records associated with this event. Snapshots are ordered by `bookmaker_id` and then descending by `last_update` to ensure the most recent odds for each market are processed preferentially.
3.  Iterates through the snapshots and groups them by `bookmaker_id`.
4.  For each bookmaker, it further groups odds by `market_key`. The `outcomes_data` (a JSON string in `OddsSnapshot`) is parsed into a list of `OutcomeOdds`.
5.  Only the latest snapshot for each unique `market_key` per bookmaker is included in the final aggregated data.
6.  The results are structured into an `AggregatedEventOdds` object. If no event or no snapshots are found, it returns `None` or an `AggregatedEventOdds` object with empty `bookmakers_odds`, respectively.

## 2. Discrepancy Detection & Opportunity Identification

The goal is to identify potential betting opportunities. This involves comparing odds across different bookmakers and against a calculated "reference" or "fair" odds.

### Key Pydantic Schema

1.  **`PotentialOpportunity`**: Describes a detected opportunity.
    ```python
    class PotentialOpportunity(BaseModel):
        event_id: str
        sport_key: str
        home_team: str
        away_team: str
        commence_time: datetime
        market_key: str
        outcome_name: str
        bookmaker_key: str # The bookmaker offering the favorable odds
        bookmaker_odds: float # The specific odds offered
        reference_odds: float # Calculated reference/fair odds for comparison
        potential_ev: Optional[float] = None # Calculated Expected Value (placeholder)
        p2p_offerable_price: Optional[float] = None # Potential price on a P2P platform (placeholder)
        description: str # Explanation of why this is an opportunity
        snapshot_time: datetime # Timestamp of the underlying odds data
    ```

### Reference Odds Calculation (`calculate_reference_odds` function)

The `calculate_reference_odds(db: Session, aggregated_event: AggregatedEventOdds, target_outcome_name: str, market_key: str) -> Optional[float]` function in `backend/odds_analyzer.py` aims to establish a baseline for comparison:
1.  It queries the database for all `Bookmaker` entries that are `active`, not `is_p2p`, and in the `'us'` region.
2.  It then filters the `bookmakers_odds` within the provided `aggregated_event` data to consider only these selected US non-P2P bookmakers.
3.  For the specified `target_outcome_name` and `market_key`, it collects all `price` values from these filtered bookmakers.
4.  If prices are found, it calculates and returns their simple average. Otherwise, it returns `None`.
5.  This average serves as the initial "reference odds." Future improvements will involve more sophisticated fair odds calculations (e.g., removing vigorish, using weighted averages).

### Opportunity Detection Logic (`find_positive_ev_opportunities` function)

The `find_positive_ev_opportunities(aggregated_odds: AggregatedEventOdds, db: Session, p2p_commission_rate: float, ev_threshold: float) -> List[PotentialOpportunity]` function in `backend/odds_analyzer.py` identifies two main types of opportunities (currently, only the first is implemented with basic logic):

1.  **Sportsbook Odds vs. Reference Odds**:
    *   For each outcome offered by a non-P2P bookmaker in the `aggregated_odds`:
        *   The `calculate_reference_odds` function is called to get the average market price from other non-P2P US bookmakers.
        *   **Current Heuristic (Simplified)**:
            *   If both the bookmaker's price and the reference price are positive American odds, an opportunity is flagged if the bookmaker's price is greater than `reference_price * (1 + ev_threshold)`.
            *   If both are negative American odds, an opportunity is flagged if the absolute value of the bookmaker's price is less than `abs(reference_price) * (1 - ev_threshold)`.
            *   (Example: `ev_threshold = 0.01` means a 1% better price).
        *   **Future Improvement**: This logic will be replaced with a proper conversion of American odds to implied probabilities to calculate actual Expected Value (EV). `EV = (Probability of Winning * Payout) - (Probability of Losing * Stake)`.
    *   If an opportunity is identified, a `PotentialOpportunity` object is created and logged.

2.  **Peer-to-Peer (P2P) Opportunities (Conceptual - Not Fully Implemented)**:
    *   The system will eventually identify scenarios where:
        *   A user could offer odds on a P2P exchange that are more attractive to a backer than available sportsbook odds, while still being profitable for the layer (after commission).
        *   A user could take (back) odds on a P2P exchange that are better than any sportsbook offers.
    *   This requires comparing against the *best available* sportsbook odds (not just the average) and considering the P2P commission (`p2p_commission_rate`).

### Alerting & Logging

*   Detected opportunities are logged using the standard Python `logging` module.
*   The `notify_opportunity(opportunity: PotentialOpportunity)` function in `backend/odds_analyzer.py` serves as a placeholder. Currently, it logs the detected opportunity. In the future, this could be expanded to send real-time alerts (e.g., email, push notifications).

## 3. API Endpoint for Opportunities

A FastAPI endpoint is provided to fetch the currently detected opportunities.

### `GET /api/opportunities`

*   **Method**: `GET`
*   **URL**: `/api/opportunities`
*   **Response Body**: A JSON list of `PotentialOpportunity` objects.
    ```json
    [
        {
            "event_id": "unique_event_id_string",
            "sport_key": "baseball_mlb",
            "home_team": "Team A",
            "away_team": "Team B",
            "commence_time": "2025-05-24T00:00:00Z",
            "market_key": "h2h",
            "outcome_name": "Team A",
            "bookmaker_key": "draftkings",
            "bookmaker_odds": 150,
            "reference_odds": 135.5,
            "potential_ev": null,
            "p2p_offerable_price": null,
            "description": "DraftKings offers significantly better positive odds (150) than reference (135.50).",
            "snapshot_time": "2025-05-23T10:30:00Z"
        },
        // ... more opportunities
    ]
    ```
*   **Functionality**:
    1.  Retrieves all `Event` records from the database where `completed` is `False`.
    2.  For each active event:
        a.  Calls `aggregate_event_odds` to get the structured odds data.
        b.  If aggregation is successful, calls `find_positive_ev_opportunities` with the aggregated data.
    3.  Collects all `PotentialOpportunity` objects found across all events.
    4.  Returns the list. If no opportunities are found, an empty list is returned with a 200 OK status. 