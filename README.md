# AI-Assisted Peer-to-Peer Betting Intelligence

**Created:** May 23, 2025

## Description

An innovative platform that leverages real-time sportsbook odds data from top market-makers (DraftKings, FanDuel, Pinnacle, Caesars) to empower users to identify and set advantageous "limit order-style" bets on emerging peer-to-peer (P2P) betting platforms like Sporttrade, ProphetX, and Novig. 

The platform automates value identification, clearly communicates optimal betting strategies, educates users on the unique P2P betting model, and generates revenue through premium subscriptions and affiliate links.

## Key Features

- **Real-time Value Detection**: Compare sportsbook odds to P2P exchanges
- **Limit Order-Style Betting**: Set target odds and get alerted when market conditions are favorable
- **AI-Driven Analytics**: Advanced Bayesian methods and Monte Carlo simulations (Premium)
- **Educational Platform**: Comprehensive P2P betting education for new users
- **Historical Data Storage**: Capture opening and closing odds for analytics
- **Multi-Platform Integration**: Support for multiple sportsbooks and P2P exchanges

## Product Tiers

### Free Version
- Limited to one sportsbook and one P2P exchange
- Basic odds search functionality
- Limited educational content
- Simple recommended odds for select events

### Premium Version
- Access to multiple sportsbooks and P2P platforms
- Advanced AI-driven formulas and ML integrations
- Comprehensive Monte Carlo simulations and Bayesian odds adjustments
- Real-time alerts and extensive educational resources
- Full historical odds storage and detailed analytics

## Quick Start

### Prerequisites

- Python 3.9+ (for backend)
- Node.js 16+ and npm (for frontend)
- Git
- **The Odds API key** (get free tier at https://the-odds-api.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bet-intel
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   # Backend configuration
   cd backend
   cp .env.example .env
   # Edit .env with your API credentials (especially ODDS_API_KEY)
   
   # Frontend configuration  
   cd ../frontend
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running Locally

1. **Start the Backend**
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python main.py
   ```

2. **Start the Odds Polling Service (Optional)**
   ```bash
   # In a separate terminal
   cd backend
   source venv/bin/activate
   python odds_poller.py
   ```

3. **Start the Frontend**
   ```bash
   cd frontend
   npm start
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Current Features (v0.1.0)

### ✅ Real-Time Odds Polling
- **The Odds API Integration**: Configured for MLB data with 3-minute intervals
- **Comprehensive Data Storage**: Events, bookmakers, odds snapshots with full history
- **Opening/Closing Odds Tracking**: Automatic detection and flagging for analytics
- **Rate Limiting & Error Handling**: Robust API management with quota tracking
- **Multiple Market Support**: Moneyline (h2h), spreads, and totals

### ✅ Backend Infrastructure
- **FastAPI Application**: RESTful API with automatic documentation
- **SQLite Database**: Lightweight storage with SQLAlchemy ORM
- **Configuration Management**: Environment-based settings with Pydantic
- **Monitoring Endpoints**: API status, polling logs, and database statistics

### 🔧 Testing & Development
- **Manual Polling Trigger**: `POST /api/poll-odds` for testing
- **Database Inspection**: View events, logs, and statistics via API
- **Comprehensive Logging**: Configurable log levels for debugging
- **Error Tracking**: Full error capture and monitoring

### 📊 Data Features
- **Historical Preservation**: Complete odds movement tracking
- **Multi-Bookmaker Support**: US sportsbooks (DraftKings, FanDuel, Caesars, etc.)
- **Market Flexibility**: Configurable sports, regions, and bet types
- **Performance Monitoring**: Response times and success rates

## API Examples

```bash
# Check system health
curl http://localhost:8000/health

# View recent MLB games
curl "http://localhost:8000/api/events?limit=5"

# Get polling statistics
curl http://localhost:8000/api/stats

# Trigger manual odds collection
curl -X POST http://localhost:8000/api/poll-odds

# View polling history
curl "http://localhost:8000/api/polling-logs?limit=10"
```

## Development Status

### Current Implementation (May 23, 2025)
- ✅ Repository setup and project structure
- ✅ The Odds API integration and polling system (MLB focus)
- ✅ Database models and data storage
- ✅ Basic FastAPI backend with monitoring endpoints
- ✅ Opening and closing odds tracking
- ✅ Comprehensive error handling and logging

### Next Steps (Week 1-2)
- [ ] ProphetX API integration for P2P market data
- [ ] Sporttrade API integration
- [ ] Basic value detection engine
- [ ] React frontend dashboard

### Upcoming (Week 3-4)
- [ ] Odds aggregation and comparison logic
- [ ] User interface for odds display
- [ ] Real-time notifications system
- [ ] Educational content integration

## Project Structure

```
bet-intel/
├── backend/          # Python FastAPI backend
├── frontend/         # React frontend
├── docs/            # Documentation
├── tests/           # Test files
├── checklist.md     # Development checklist
├── prd.md          # Product Requirements Document
└── README.md       # This file
```

## Development

### Backend (Python/FastAPI)
- API endpoints for odds aggregation
- Real-time data processing
- AI/ML algorithms for value detection
- Database management

### Frontend (React)
- User dashboard and interface
- Real-time odds display
- Educational content
- Responsive mobile design

## API Integrations

- **Pinnacle API**: Official odds data
- **ProphetX API**: P2P market data
- **Sporttrade API**: P2P trading data
- **DraftKings/FanDuel**: Scraping or aggregator APIs
- **OddsAPI**: Backup data source

## Usage

*[Coming Soon - Detailed usage instructions will be added as features are implemented]*

## Features

*[Coming Soon - Comprehensive feature documentation will be added during development]*

## Deployment

*[Coming Soon - Deployment instructions for Vercel and production environments]*

## Contributing

*[Coming Soon - Contribution guidelines and development workflow]*

## Legal Considerations

- No automated bet placement (user-initiated only)
- Compliance with data sourcing terms of service
- Responsible gambling practices

## License

*[License information to be added]*

## Support

*[Support information to be added]*

### 📈 **Current Data Coverage**:
- **Sport**: MLB (baseball_mlb) - active baseball season
- **Markets**: Moneyline, Spreads, Totals  
- **Bookmakers**: US sportsbooks from The Odds API
- **Frequency**: Every 3 minutes (configurable)
- **Storage**: Complete historical odds snapshots

---

**Note**: This project is currently in active development. Check the `checklist.md` file for current progress and upcoming milestones.

## Documentation

*   [Odds Polling System](./docs/odds_polling.md)
*   [Odds Aggregation & Discrepancy Detection](./docs/odds_aggregation_discrepancy.md)
*   [Odds Conversion (American Odds to Implied Probability)](./docs/odds_conversion.md)
*   [Vig Removal & Fair Odds Calculation](./docs/vig_removal.md)

## Getting Started

(To be expanded with setup and run instructions)

### Prerequisites

*   Python 3.9+
*   Pip

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Copy the example environment file and fill in your details:
    ```bash
    cp .env.example .env
    ```
    *   You will need an API key from [The Odds API](https://the-odds-api.com/).
5.  Initialize the database:
    *   The database (`bet_intel.db`) is created automatically if it doesn't exist when the application or poller starts.
    *   You can also initialize it manually by running `python -c "from database import initialize_database; initialize_database()"` from the `backend` directory.

### Running the Backend

*   **To start the FastAPI server (for API access and manual polling tests)**:
    ```bash
    python main.py
    ```
    The API will be available at `http://localhost:8000` and documentation at `http://localhost:8000/docs`.

*   **To start the continuous odds poller service**:
    ```bash
    python odds_poller.py
    ```
    This will poll for odds at the interval defined in your `.env` file (default is 3 minutes).

### Frontend Setup

(Placeholder - to be implemented)

## Development Tasks & Checklist

Refer to [checklist.md](./checklist.md) for ongoing tasks and progress.

## Technologies

*   **Backend**: Python, FastAPI, SQLAlchemy, Pydantic, HTTPretty (for testing)
*   **Frontend**: (To be decided - likely React or Vue.js)
*   **Database**: SQLite (initially)
*   **Odds Data**: The Odds API

## Contributing

(To be defined) 