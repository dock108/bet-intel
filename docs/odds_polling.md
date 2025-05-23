# Odds Polling System Documentation

## Overview

The Odds Polling System is responsible for collecting real-time sports betting odds from The Odds API and storing them in our database for analysis and value detection. The system polls data every 3 minutes and maintains a comprehensive historical record of odds movements.

## Architecture

### Components

1. **Configuration Management** (`config.py`)
   - Centralized settings using Pydantic
   - Environment variable management
   - API keys and configuration parameters

2. **Database Models** (`database.py`)
   - `SportModel`: Available sports (MLB, NFL, NBA, etc.)
   - `EventModel`: Individual games/matches
   - `BookmakerModel`: Sportsbooks and P2P exchanges
   - `OddsSnapshotModel`: Historical odds data
   - `PollingLogModel`: API polling logs and monitoring

3. **API Client** (`odds_api_client.py`)
   - HTTP client for The Odds API
   - Rate limiting and error handling
   - Quota tracking and monitoring

4. **Polling Service** (`odds_poller.py`)
   - Scheduled data collection every 3 minutes
   - Data processing and storage
   - Opening/closing odds tracking

## Data Flow

```
The Odds API → OddsAPIClient → OddsPoller → Database Storage
     ↓                          ↓               ↓
 Rate Limits           Data Processing    Historical Tracking
 Error Handling        Event Storage      Opening/Closing Odds
 Quota Monitoring      Bookmaker Mgmt     Performance Logs
```

## Configuration

### Environment Variables

```bash
# Required
ODDS_API_KEY=your_api_key_here

# Optional (with defaults)
ODDS_POLLING_INTERVAL_MINUTES=3
DEFAULT_SPORT=baseball_mlb
DEFAULT_REGIONS=us
DEFAULT_MARKETS=h2h,spreads,totals
ODDS_FORMAT=american
```

### Default Sport Focus

Currently configured for MLB (`baseball_mlb`) with:
- **Regions**: US sportsbooks
- **Markets**: Moneyline (h2h), spreads, totals
- **Format**: American odds

## Database Schema

### Events Table
- Stores game information (teams, dates, sport)
- Tracks opening/closing odds timestamps
- Links to multiple odds snapshots

### Odds Snapshots Table
- Full historical odds data
- Market-specific outcomes
- Bookmaker and timestamp information
- Opening/closing odds flags

### Polling Logs Table
- API request monitoring
- Success/failure tracking
- Quota usage monitoring
- Performance metrics

## API Endpoints

### Testing & Monitoring

- `GET /api/events` - Recent events in database
- `GET /api/polling-logs` - Polling history and status
- `GET /api/stats` - Database statistics
- `POST /api/poll-odds` - Manual polling trigger

### Example Usage

```bash
# Check system status
curl http://localhost:8000/health

# View recent events
curl http://localhost:8000/api/events?limit=5

# Trigger manual polling
curl -X POST http://localhost:8000/api/poll-odds

# View polling logs
curl http://localhost:8000/api/polling-logs?limit=10
```

## Running the System

### 1. Setup Environment

```bash
cd backend
cp .env.example .env
# Edit .env with your actual ODDS_API_KEY
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start FastAPI Server

```bash
python main.py
```

### 4. Start Polling Service (Separate Process)

```bash
python odds_poller.py
```

## Monitoring & Troubleshooting

### Quota Management
- Free tier: 500 requests/month
- Cost per MLB request: 3 (regions=us, markets=h2h,spreads,totals)
- ~167 MLB polls per month at current settings

### Error Handling
- Rate limiting protection
- Automatic retry logic
- Comprehensive logging
- Database transaction safety

### Performance Monitoring
- Response time tracking
- Success/failure rates
- Quota usage monitoring
- Event processing statistics

## Data Quality Features

### Opening Odds Tracking
- Automatically detects first odds for new events
- Flags opening odds in database
- Timestamp tracking for analytics

### Closing Odds Tracking
- Monitors events approaching start time
- Captures final odds before game begins
- Essential for performance analysis

### Historical Preservation
- Full odds snapshots at each poll
- Market-by-market storage
- Bookmaker attribution
- Time-series analysis ready

## Future Enhancements

1. **Multi-Sport Support**
   - NFL, MLB, NHL expansion
   - Sport-specific configuration

2. **P2P Exchange Integration**
   - Sporttrade API
   - ProphetX API
   - Novig integration

3. **Advanced Analytics**
   - Odds movement detection
   - Value opportunity alerts
   - Market efficiency analysis

4. **Performance Optimization**
   - Selective polling strategies
   - Intelligent quota management
   - Delta-only updates

## Troubleshooting Guide

### Common Issues

1. **API Key Errors**
   ```
   ValueError: ODDS_API_KEY is required
   ```
   Solution: Set valid API key in `.env` file

2. **Rate Limiting**
   ```
   RateLimitError: API rate limit exceeded
   ```
   Solution: Reduce polling frequency or upgrade API plan

3. **Database Connection**
   ```
   SQLAlchemy connection errors
   ```
   Solution: Check database file permissions and path

4. **No Events Returned**
   - Current sport season dates
   - API response empty (normal during off-season)
   - Network connectivity issues

### Logging Levels

- `INFO`: Normal operations and statistics
- `WARNING`: Rate limits and recoverable errors  
- `ERROR`: API failures and processing errors
- `DEBUG`: Detailed request/response data

Set logging level via `LOG_LEVEL` environment variable. 