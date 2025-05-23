## Repository Setup & Infrastructure
- [x] **Git Repository Initialization:** Initialize Git repository and verify setup.
- [x] **Project Structure Creation:** Create backend, frontend, docs, and tests directories.
- [x] **Gitignore Configuration:** Comprehensive .gitignore for Python, React, and development environments.
- [x] **README.md Creation:** Initial project documentation with setup instructions.
- [x] **Development Environment Preparation:** Basic project structure ready for development.
- [x] **Environment Template Creation:** Create .env.example files for configuration.
- [x] **Initial Dependencies Setup:** Create requirements.txt and package.json templates.

## Odds & Data Acquisition
- [x] **The Odds API Setup:** Sign up and integrate free tier for initial odds data.
- [x] **The Odds API Polling:** Implement polling every 3 minutes for real-time odds.
- [ ] **ProphetX API Integration:** Register, obtain credentials, verify odds retrieval.
- [ ] **Sporttrade API Request & Integration:** Request access or evaluate scraping odds.
- [ ] **Liquidity Scraping (if required):** Setup scraping for ProphetX and Sporttrade liquidity.
- [x] **Opening & Closing Odds Storage:** Capture and store initial and final odds per event.

## Odds Interface (Frontend - v0.dev)
- [ ] **Odds Search Bar:** Basic search component implementation.
- [ ] **Odds Results Display:** Display odds clearly from selected sportsbook and P2P.
- [ ] **Recommended Odds Component:** UI element clearly showing recommended limit-order odds.
- [ ] **Real-Time UI Updates:** Auto-refresh odds display based on polling interval.

## Value Detection Engine
- [ ] **Odds Aggregation Logic:** Combine and standardize sportsbook and P2P odds data.
- [ ] **Discrepancy Detection Logic:** Identify betting opportunities exceeding EV threshold.
- [ ] **Bayesian Odds Calculation (Premium):** Bayesian-adjusted odds recommendation logic.
- [ ] **Monte Carlo Simulation (Premium):** Implement predictive simulations for odds.
- [ ] **Automated Recommendation Pipeline:** Regularly update odds and recommendations.

## Limit Order Feature (Frontend - v0.dev)
- [ ] **Custom Odds Input Form:** Allow user-defined target odds.
- [ ] **Limit Order Monitoring:** Backend logic for monitoring user-set odds.
- [ ] **Limit Order Trigger Alert:** Notification system when limit odds are met.

## Notifications & Alerts
- [ ] **Alert System Infrastructure:** Notification setup (email, push notifications).
- [ ] **Recommended Odds Alert Trigger:** Real-time alert for recommended betting opportunities.
- [ ] **Odds Movement Alert Trigger:** User notification for significant odds changes.

## Affiliate Integration
- [ ] **Affiliate Setup:** Register with sportsbooks affiliate programs (DraftKings, FanDuel, Caesars).
- [ ] **Affiliate Links Component:** UI integration for tracked affiliate links/buttons.
- [ ] **P2P Affiliate Integration:** Setup available referral tracking (Sporttrade, ProphetX).

## User Education & Onboarding
- [ ] **P2P Betting Introduction Module:** Create concise educational onboarding content.
- [ ] **Educational Tooltip Component:** Implement tooltips for betting concepts and terminology.

## Dashboard & UI
- [ ] **Dashboard Wireframe (v0.dev):** Simple, responsive dashboard layout.
- [ ] **Responsive Mobile Optimization:** Ensure dashboard usability on mobile/tablet.
- [ ] **Odds Quick-View Dashboard:** Highlight key betting opportunities clearly on dashboard.

## Documentation & Repo Setup
- [ ] **Git Repository Setup:** Initialize repository and directory structure.
- [ ] **.gitignore File Creation:** Setup comprehensive `.gitignore`.
- [ ] **Initial README.md:** Document basic setup, project description, and installation instructions.

## User Management (Optional Stretch Goals)
- [ ] **Simple Authentication Setup:** Minimal user account creation/login.
- [ ] **User Preferences UI:** Basic notification and sports preferences management.

# Development Task Checklist

## Phase 1: Core Backend & Odds Polling (MVP)

-   [x] **Repository Setup**
    -   [x] Initialize Git repository.
    -   [x] Create `backend` and `frontend` directories.
    -   [x] Add basic `.gitignore`.
    -   [x] Create initial `README.md`.
    -   [x] Create `backend/.env.example` and `frontend/.env.example`.
    -   [x] Basic `backend/requirements.txt` and `frontend/package.json` (empty or placeholder).
-   [x] **Environment Configuration (`backend/config.py`)**
    -   [x] Use Pydantic for settings management.
    -   [x] Load settings from `.env` file (API Key, DB URL, Polling Interval, Default Sport/Regions/Markets).
-   [x] **Database Setup (`backend/database.py`)**
    -   [x] Define SQLAlchemy models for: `Sport`, `Event`, `Bookmaker`, `OddsSnapshot`, `PollingLog`.
    -   [x] Include fields for created_at, updated_at.
    -   [x] Function to initialize database and tables (SQLite initially).
-   [x] **Odds API Client (`backend/odds_api_client.py`)**
    -   [x] HTTP client using `httpx`.
    -   [x] Fetch active sports.
    -   [x] Fetch odds for a given sport, region, market.
    -   [x] Basic error handling (retries, rate limits).
    -   [x] Track API quota usage (requests remaining, used).
-   [x] **Odds Polling Service (`backend/odds_poller.py`)**
    -   [x] Service to poll The Odds API at a configurable interval (e.g., every 3 minutes).
    -   [x] Fetch odds for the configured default sport(s), regions, and markets.
    -   [x] Parse API response.
    -   [x] Store/update `Sport`, `Event`, `Bookmaker`, and `OddsSnapshot` data in the database.
    -   [x] Logic to identify and flag "opening odds" (first snapshot for an event-market-bookmaker).
    -   [x] Log polling activity to `PollingLog` table (success/failure, number of events processed, API quota info).
-   [x] **FastAPI Application (`backend/main.py`)**
    -   [x] Basic FastAPI app setup.
    -   [x] `/health` endpoint.
    -   [x] Endpoint to manually trigger an odds poll (for testing).
    -   [x] Endpoints to view stored events, polling logs, and basic DB stats.
-   [x] **Initial Documentation & Testing**
    -   [x] Document the odds polling system (`docs/odds_polling.md`).
    -   [x] Update `README.md` with setup instructions and system overview.
    -   [x] Basic test script (`backend/test_system.py`) to verify setup and core components (mocking API calls).

-   [ ] **Odds Aggregation & Discrepancy Detection (`backend/odds_analyzer.py`)**
    -   [x] **Odds Aggregation Logic**: Write Python logic to aggregate odds snapshots into clear, structured data per event.
        -   [x] Define Pydantic models for aggregated odds structures (e.g., `AggregatedEventOdds`, `BookmakerEventOdds`, `MarketOdds`, `OutcomeOdds`).
        -   [x] Implement `aggregate_event_odds` function.
    -   [x] **Document Aggregated Odds Schema**: Clearly document the schema in `docs/odds_aggregation_discrepancy.md`.
    -   [x] **Initial Discrepancy Detection**: Implement logic to detect odds discrepancies based on simple thresholds.
        -   [x] Implement `calculate_reference_odds` (e.g., average from non-P2P US bookmakers).
        -   [x] Implement initial `find_positive_ev_opportunities` comparing bookmaker odds to reference odds.
        -   [x] Define Pydantic model for `PotentialOpportunity`.
    -   [x] **Alert & Logging**: Log clearly when positive EV opportunities are detected.
        -   [x] Use Python `logging` for discrepancy logs.
        -   [x] Create placeholder `notify_opportunity` function.
    -   [x] **API Endpoint for Opportunities**: Expose a simple API endpoint (`GET /api/opportunities`) to fetch current detected opportunities.
    -   [x] **Document Endpoint & Logic**: Document usage in `docs/odds_aggregation_discrepancy.md` and link in `README.md`.
    -   [x] **Checklist Update**: Mark tasks as complete.

## Phase 2: Enhanced Analysis & P2P Logic

-   [ ] **Advanced Discrepancy/EV Calculation**
    -   [ ] Convert American odds to implied probabilities for all calculations.
    -   [ ] Implement proper Expected Value (EV) calculation: `EV = (ProbWin * Payout) - (ProbLose * Stake)`.
    -   [ ] Refine "fair odds" calculation (e.g., remove vigorish from reference bookmakers).
    -   [ ] Consider using a weighted average for reference odds based on bookmaker reliability/volume (if data available).
-   [ ] **P2P Opportunity Identification**
    -   [ ] Logic to identify when a user could *offer* (lay) odds on a P2P platform that are better (for the layer) than sportsbook lay odds (derived from back odds), after P2P commission.
    -   [ ] Logic to identify when a user could *take* (back) odds on a P2P platform that are better than best available sportsbook back odds.
    -   [ ] Update `PotentialOpportunity` model to clearly distinguish P2P lay/back opportunities.
-   [ ] **User Authentication & Accounts**
    -   [ ] Basic user registration and login (FastAPI Users or similar).
    -   [ ] Secure password hashing.
    -   [ ] JWT for API authentication.
-   [ ] **User Preferences/Alerts**
    -   [ ] Allow users to save preferred sports, markets, or types of opportunities.
    -   [ ] Basic notification system (e.g., email alerts for saved searches/opportunities) - (Integrate with placeholder `notify_opportunity`).
-   [ ] **API Enhancements**
    -   [ ] Endpoints for users to manage their preferences.
    -   [ ] Paginated responses for long lists (events, opportunities).
    -   [ ] Filtering options for opportunities API (by sport, market, EV threshold).

## Phase 3: Frontend Development

-   [ ] **Basic Frontend Structure**
    -   [ ] Choose frontend framework (e.g., React, Vue, Svelte).
    -   [ ] Setup project with routing, state management.
-   [ ] **Display Odds & Opportunities**
    -   [ ] Pages to display aggregated odds for events.
    -   [ ] Dashboard to show detected opportunities.
    -   [ ] User-friendly display of odds, EV, etc.
-   [ ] **User Interface for P2P Actions (Conceptual)**
    -   [ ] Mockups for how users might offer/take bets on a P2P platform based on identified opportunities.
    -   [ ] (Actual P2P matching/betting engine is out of scope for initial PRD, but UI can show intent).
-   [ ] **User Account Management Pages**
    -   [ ] Login, registration, profile, alert preferences.

## Phase 4: Deployment & Operations

-   [ ] **Containerization**
    -   [ ] Dockerfile for backend.
    -   [ ] Docker Compose for local development.
-   [ ] **Cloud Deployment (e.g., AWS, Google Cloud, Azure)**
    -   [ ] Choose a PaaS or IaaS solution.
    -   [ ] Setup production database (e.g., PostgreSQL, MySQL).
    -   [ ] CI/CD pipeline (GitHub Actions).
-   [ ] **Monitoring & Logging**
    -   [ ] Centralized logging for backend services.
    -   [ ] Basic application performance monitoring.

## Future Considerations / Wishlist

-   [ ] Historical odds data analysis & charting.
-   [ ] Machine learning models to predict odds movements or refine EV calculations.
-   [ ] Integration with more odds data sources.
-   [ ] Community features (forums, bet sharing).
-   [ ] Real-time WebSocket updates for odds changes.