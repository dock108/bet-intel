# Backend Odds API Integration

## Overview

The betting intelligence platform backend integrates with odds data providers to fetch real-time sports betting odds and calculate expected value (EV) opportunities. As of May 2025, we have migrated from The Odds API to **SportsGameOdds (SGO)** for improved coverage and reliability.

## Current Integration: SportsGameOdds (SGO) API

### Features
- 55+ leagues across 25+ sports
- Sub-minute update frequency
- Pre-match and live odds
- Player props, game props, and futures
- Results data for all odds
- Historical data availability
- Comprehensive bookmaker coverage including Pinnacle, DraftKings, FanDuel

### Setup

#### 1. Obtain API Credentials
1. Visit [SportsGameOdds.com](https://sportsgameodds.com)
2. Sign up for an account and select a plan
3. Obtain your API key from the dashboard

#### 2. Configure Environment
Update your `.env` file with the SGO API key:

```bash
# SportsGameOdds (SGO) API - NEW
SGO_API_KEY=your_sgo_api_key_here
```

#### 3. Configuration Settings
The SGO integration uses the following configuration in `config.py`:

```python
# SportsGameOdds (SGO) API Configuration
sgo_api_base_url: str = "https://api.sportsgameodds.com/v1"
sgo_polling_interval_minutes: int = 2
default_sport_id: str = "1"  # Baseball (MLB)
default_league_id: str = "1"  # MLB
```

### API Client Usage

#### Basic Usage
```python
from backend.sgo_api_client import SGOAPIClient

# Initialize client
client = SGOAPIClient()

# Get available sports
sports = client.get_sports()

# Get leagues for a sport
leagues = client.get_leagues(sport_id="1")

# Get events for a league
events = client.get_events(league_id="1", status="scheduled")

# Get odds for specific criteria
odds = client.get_odds(
    sport_id="1",
    league_id="1",
    market_type="moneyline"
)
```

#### Authentication
The SGO API uses header-based authentication:
```
x-api-key: your_api_key_here
```

This is automatically handled by the `SGOAPIClient` class.

### Available Endpoints

#### Core Data Endpoints
- `/sports` - Get available sports
- `/leagues` - Get available leagues
- `/events` - Get events/games
- `/odds` - Get odds data
- `/bookmakers` - Get available bookmakers
- `/teams` - Get team data
- `/results` - Get game results and scores

#### Event-Specific Endpoints
- `/events/{eventId}/odds` - Get odds for specific event

### Data Structure

#### Event Data
```json
{
  "eventID": "12345",
  "sportID": "1",
  "leagueID": "1",
  "sport": {"name": "Baseball"},
  "teams": {
    "home": {"name": "New York Yankees"},
    "away": {"name": "Boston Red Sox"}
  },
  "startTime": "2025-05-23T19:00:00Z"
}
```

#### Odds Data
```json
{
  "eventID": "12345",
  "bookmakerID": "draftkings",
  "bookmakerName": "DraftKings",
  "marketType": "moneyline",
  "odds": {
    "moneyline": {
      "home": -150,
      "away": 130
    }
  },
  "lastUpdate": "2025-05-23T18:45:00Z"
}
```

### Polling Service

#### SGO Odds Poller
The `SGOOddsPoller` class handles automated odds fetching:

```python
from backend.sgo_odds_poller import SGOOddsPoller

# Initialize poller
poller = SGOOddsPoller()

# Poll once
success = poller.poll_odds_once()

# Start continuous polling
await poller.start_polling()
```

#### Manual Polling via API
```bash
# Trigger SGO polling manually
curl -X POST http://localhost:8000/api/poll-odds-sgo
```

### Data Mapping

#### Market Type Mapping
SGO market types are mapped to internal format:
- `moneyline` → `h2h`
- `spread`/`pointspread` → `spreads`
- `total`/`totals` → `totals`

#### Bookmaker Detection
P2P platforms are automatically detected based on known mappings:
- Pinnacle, Betfair, Matchbook, SportTrade, NoVig → `is_p2p: true`
- Traditional sportsbooks → `is_p2p: false`

### Error Handling

#### Rate Limiting
SGO API enforces rate limits. The client handles:
- HTTP 429 responses
- Automatic retry logic (in development)
- Rate limit logging

#### Error Types
```python
from backend.sgo_api_client import SGOAPIError, SGORateLimitError

try:
    data = client.get_odds()
except SGORateLimitError:
    # Handle rate limit
    pass
except SGOAPIError as e:
    # Handle API error
    logger.error(f"SGO API error: {e}")
```

### Monitoring and Logging

#### Polling Logs
All polling activities are logged to the database via `PollingLogModel`:
- Success/failure status
- Response times
- Error messages
- Events processed count

#### Metrics Available
- Response time tracking
- Success/failure rates
- Data freshness
- Coverage statistics

### Migration Notes

#### From The Odds API
The migration includes:
1. **API Client**: New `SGOAPIClient` replacing `OddsAPIClient`
2. **Data Format**: Adapted data parsing for SGO response structure
3. **Endpoints**: Updated to use SGO endpoint patterns
4. **Authentication**: Changed from query parameter to header-based auth
5. **Polling Logic**: Enhanced poller with SGO-specific data handling

#### Backward Compatibility
- Legacy The Odds API integration maintained for transition period
- Database schema compatible with both data sources
- API endpoints support both data sources

### Rate Limits and Quotas

#### SGO Rate Limits
- Sub-minute update frequency supported
- Rate limits vary by subscription plan
- Monitor via response headers and logging

#### Best Practices
1. **Polling Frequency**: Start with 2-minute intervals
2. **Error Handling**: Implement exponential backoff
3. **Data Validation**: Validate incoming data structure
4. **Monitoring**: Track API usage and success rates

### Troubleshooting

#### Common Issues

**Authentication Errors**
```
Error: SGO_API_KEY is required
```
- Ensure `SGO_API_KEY` is set in `.env`
- Verify API key is valid and active

**Rate Limit Exceeded**
```
Error: API rate limit exceeded
```
- Increase polling interval
- Check subscription plan limits
- Monitor usage patterns

**Data Format Errors**
```
Error: Invalid JSON response
```
- Check API endpoint availability
- Verify request parameters
- Review SGO API documentation

#### Debugging Steps
1. Check environment variables
2. Verify API key validity
3. Test with minimal request
4. Review logs for detailed errors
5. Check SGO API status page

### Performance Optimization

#### Caching Strategy
- Database caching for recent odds
- In-memory caching for frequent requests
- TTL-based cache invalidation

#### Data Processing
- Batch processing for multiple events
- Parallel requests where appropriate
- Efficient database operations

### Security Considerations

#### API Key Management
- Store keys in environment variables
- Never commit keys to version control
- Rotate keys regularly
- Monitor for unauthorized usage

#### Data Validation
- Validate all incoming data
- Sanitize before database storage
- Implement data integrity checks

---

## Legacy Integration: The Odds API (Deprecated)

### Status: Maintained for Transition Period

The previous integration with The Odds API is maintained during the transition period but will be deprecated. New developments should use the SGO integration.

#### Legacy Endpoints
- `/api/poll-odds` - Legacy polling endpoint
- Configuration still available in `odds_api_*` settings

#### Migration Timeline
- **Phase 1**: Dual operation (current)
- **Phase 2**: SGO as primary, legacy as backup
- **Phase 3**: Full migration to SGO
- **Phase 4**: Legacy removal

### Support and Resources

#### Documentation
- [SGO API Documentation](https://sportsgameodds.com/docs/introduction)
- [Getting Started Guide](https://sportsgameodds.com/docs/getting-started)

#### Support Channels
- SGO API support: Available through dashboard
- Internal support: Backend development team

#### Related Files
- `backend/sgo_api_client.py` - SGO API client
- `backend/sgo_odds_poller.py` - SGO polling service
- `backend/config.py` - Configuration settings
- `backend/.env` - Environment variables 