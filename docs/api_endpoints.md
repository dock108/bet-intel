# API Endpoints Documentation

## Overview

This document describes the API endpoints available in the AI-Assisted P2P Betting Intelligence platform, focusing on Expected Value (EV) calculations and betting opportunities.

## Base URL

```
http://localhost:8000  # Development
```

## Authentication

*Currently no authentication required for MVP. Future versions will implement API key or JWT authentication.*

---

## GET /api/ev-opportunities

Retrieve events with comprehensive Expected Value calculations across all three calculation methods.

### Description

This endpoint returns active sports betting events along with their EV calculations using three distinct methods:
- **Standard EV**: Basic calculation using raw bookmaker odds (includes vig)
- **No-Vig EV**: Calculation using vig-removed fair odds
- **Weighted Fair Odds EV**: Sophisticated calculation using weighted consensus from Pinnacle (50%), DraftKings (25%), and FanDuel (25%)

### Query Parameters

| Parameter | Type | Default | Description | Constraints |
|-----------|------|---------|-------------|-------------|
| `limit` | integer | 20 | Maximum number of events to return | 1-100 |
| `sport_key` | string | null | Filter by sport (e.g., 'baseball_mlb') | Optional |
| `bookmaker_key` | string | null | Filter by bookmaker (e.g., 'draftkings') | Optional |
| `market_key` | string | "h2h" | Market type filter | Default: moneyline |
| `positive_ev_only` | boolean | false | Only return events with positive EV opportunities | Optional |

### Example Requests

```bash
# Get all EV opportunities (default parameters)
curl "http://localhost:8000/api/ev-opportunities"

# Get only MLB games with positive EV
curl "http://localhost:8000/api/ev-opportunities?sport_key=baseball_mlb&positive_ev_only=true"

# Get DraftKings opportunities only, limit to 10 events
curl "http://localhost:8000/api/ev-opportunities?bookmaker_key=draftkings&limit=10"

# Get upcoming events with any positive EV signals
curl "http://localhost:8000/api/ev-opportunities?positive_ev_only=true&limit=5"
```

### Response Format

```json
{
  "events": [
    {
      "event": {
        "external_id": "event_12345",
        "sport_key": "baseball_mlb",
        "sport_title": "MLB",
        "home_team": "New York Yankees",
        "away_team": "Boston Red Sox",
        "commence_time": "2025-05-23T19:05:00"
      },
      "ev_calculations": [
        {
          "bookmaker": {
            "key": "draftkings",
            "title": "DraftKings"
          },
          "outcomes": [
            {
              "outcome_name": "outcome_A",
              "outcome_index": 0,
              "offered_odds": 120,
              "standard_ev": 21.0,
              "no_vig_ev": 18.5,
              "weighted_fair_ev": 15.2,
              "standard_implied_probability": 0.4545,
              "no_vig_fair_probability": 0.4762,
              "weighted_fair_probability": 0.4800,
              "no_vig_fair_odds": 110,
              "weighted_fair_odds": 108,
              "vig_percentage": 0.0476,
              "books_used_in_weighted": "pinnacle,draftkings,fanduel",
              "has_positive_standard_ev": true,
              "has_positive_no_vig_ev": true,
              "has_positive_weighted_ev": true,
              "calculated_at": "2025-05-23T14:30:00"
            },
            {
              "outcome_name": "outcome_B",
              "outcome_index": 1,
              "offered_odds": -150,
              "standard_ev": -8.0,
              "no_vig_ev": -12.5,
              "weighted_fair_ev": -15.8,
              "has_positive_standard_ev": false,
              "has_positive_no_vig_ev": false,
              "has_positive_weighted_ev": false,
              "calculated_at": "2025-05-23T14:30:00"
            }
          ]
        }
      ],
      "opportunities_summary": {
        "total_bookmakers": 1,
        "positive_standard_ev_count": 1,
        "positive_no_vig_ev_count": 1,
        "positive_weighted_fair_ev_count": 1,
        "best_standard_ev": {
          "ev": 21.0,
          "bookmaker": "DraftKings",
          "outcome": "outcome_A",
          "odds": 120
        },
        "best_no_vig_ev": {
          "ev": 18.5,
          "bookmaker": "DraftKings",
          "outcome": "outcome_A",
          "odds": 120,
          "vig_percentage": 0.0476
        },
        "best_weighted_fair_ev": {
          "ev": 15.2,
          "bookmaker": "DraftKings",
          "outcome": "outcome_A",
          "odds": 120,
          "books_used": "pinnacle,draftkings,fanduel"
        }
      }
    }
  ],
  "total": 1,
  "filters_applied": {
    "sport_key": null,
    "bookmaker_key": null,
    "market_key": "h2h",
    "positive_ev_only": false,
    "limit": 20
  },
  "metadata": {
    "generated_at": "2025-05-23T14:35:00",
    "ev_methods": {
      "standard_ev": "Expected value using raw bookmaker odds (includes vig)",
      "no_vig_ev": "Expected value using vig-removed fair odds",
      "weighted_fair_ev": "Expected value using weighted consensus (Pinnacle 50%, DK 25%, FD 25%)"
    }
  }
}
```

### Response Fields

#### Event Object
- `external_id`: Unique identifier from odds API
- `sport_key`: Sport identifier (e.g., 'baseball_mlb')
- `sport_title`: Human-readable sport name
- `home_team`: Home team name
- `away_team`: Away team name
- `commence_time`: Game start time (ISO 8601 format)

#### EV Calculations Object
- `bookmaker`: Bookmaker details (key, title)
- `outcomes`: Array of outcome calculations

#### Outcome Object
- `outcome_name`: Outcome identifier ('outcome_A', 'outcome_B')
- `outcome_index`: Numeric outcome index (0, 1)
- `offered_odds`: American odds from bookmaker
- `standard_ev`: Standard EV calculation result
- `no_vig_ev`: No-vig EV calculation result
- `weighted_fair_ev`: Weighted fair odds EV result
- `*_probability`: Supporting probability calculations
- `*_fair_odds`: Reference fair odds used
- `has_positive_*_ev`: Boolean flags for positive EV detection
- `calculated_at`: Timestamp of calculation

#### Opportunities Summary
- `total_bookmakers`: Number of bookmakers analyzed
- `positive_*_ev_count`: Count of positive EV opportunities by method
- `best_*_ev`: Best EV opportunity details by method

### Error Responses

#### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Error fetching EV opportunities: specific error message"
}
```

### Usage Examples

#### 1. Finding Best Opportunities
```bash
# Get events with positive EV only, sorted by commence time
curl "http://localhost:8000/api/ev-opportunities?positive_ev_only=true&limit=10"
```

#### 2. Analyzing Specific Bookmaker
```bash
# Check DraftKings opportunities across all sports
curl "http://localhost:8000/api/ev-opportunities?bookmaker_key=draftkings"
```

#### 3. Sport-Specific Analysis
```bash
# Focus on MLB games only
curl "http://localhost:8000/api/ev-opportunities?sport_key=baseball_mlb&limit=5"
```

### Integration Notes

1. **Real-time Data**: Results reflect the most recent EV calculations stored in the database
2. **Data Freshness**: EV calculations are updated when new odds data is polled (every 3 minutes by default)
3. **Missing Data**: Events without EV calculations will return empty arrays unless `positive_ev_only=true`
4. **Performance**: Response time scales with the number of events and complexity of calculations

### Rate Limiting

*Currently no rate limiting implemented. Future versions will implement appropriate limits.*

---

## Other Endpoints

### GET /health
Simple health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "p2p-betting-intelligence"
}
```

### GET /api/events
Get recent events from database.

**Parameters:**
- `limit` (integer): Maximum events to return (default: 10)

### GET /api/stats
Get database statistics and system health.

### POST /api/poll-odds
Manually trigger odds polling (for testing/debugging).

---

## Future Endpoints (Planned)

- `POST /api/ev-calculations` - Calculate EV for user-provided probabilities
- `GET /api/events/{event_id}/ev-analysis` - Detailed EV analysis for specific event
- `GET /api/bookmakers` - List available bookmakers
- `GET /api/sports` - List available sports

---

## SDK Integration

Future versions will provide SDKs for:
- Python
- JavaScript/Node.js
- React hooks for frontend integration

For now, standard HTTP requests can be used with any programming language or tool (curl, Postman, etc.). 