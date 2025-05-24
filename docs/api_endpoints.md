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

This endpoint returns active sports betting events along with their EV calculations using two methods:
- **Standard EV**: Basic calculation using raw bookmaker odds (includes vig)
- **No-Vig EV**: Calculation using vig-removed fair odds

### Query Parameters

| Parameter | Type | Default | Description | Constraints |
|-----------|------|---------|-------------|-------------|
| `limit` | integer | 20 | Maximum number of events to return | 1-100 |
| `offset` | integer | 0 | Number of events to skip for pagination | ≥ 0 |
| `sport_key` | string | null | Filter by sport (e.g., 'baseball_mlb') | Optional |
| `bookmaker_key` | string | null | Filter by bookmaker (e.g., 'draftkings') | Optional |
| `market_key` | string | "h2h" | Market type filter | Default: moneyline |
| `positive_ev_only` | boolean | false | Only return events with positive EV opportunities | Optional |
| `min_ev_threshold` | float | null | Minimum EV threshold (e.g., 5.0 for $5+ EV) | Optional |
| `ev_method` | string | "any" | EV method for threshold filtering | 'standard', 'no_vig', 'any' |

### Example Requests

```bash
# Get all EV opportunities (default parameters)
curl "http://localhost:8000/api/ev-opportunities"

# Pagination - get second page with 10 events per page
curl "http://localhost:8000/api/ev-opportunities?limit=10&offset=10"

# Get only MLB games with positive EV
curl "http://localhost:8000/api/ev-opportunities?sport_key=baseball_mlb&positive_ev_only=true"


# DraftKings opportunities with any EV method >= $5
curl "http://localhost:8000/api/ev-opportunities?bookmaker_key=draftkings&min_ev_threshold=5.0&ev_method=any"

# Get upcoming events with standard EV >= $3, paginated
curl "http://localhost:8000/api/ev-opportunities?min_ev_threshold=3.0&ev_method=standard&limit=5&offset=0"
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
              "standard_implied_probability": 0.4545,
              "no_vig_fair_probability": 0.4762,
              "no_vig_fair_odds": 110,
              "vig_percentage": 0.0476,
              "has_positive_standard_ev": true,
              "has_positive_no_vig_ev": true,
              "calculated_at": "2025-05-23T14:30:00"
            },
            {
              "outcome_name": "outcome_B",
              "outcome_index": 1,
              "offered_odds": -150,
              "standard_ev": -8.0,
              "no_vig_ev": -12.5,
              "has_positive_standard_ev": false,
              "has_positive_no_vig_ev": false,
              "calculated_at": "2025-05-23T14:30:00"
            }
          ]
        }
      ],
      "opportunities_summary": {
        "total_bookmakers": 1,
        "positive_standard_ev_count": 1,
        "positive_no_vig_ev_count": 1,
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
        "meets_threshold": true,
        "threshold_details": {
          "min_ev_threshold": 5.0,
          "ev_method": "any"
        }
      }
    }
  ],
  "total": 1,
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total_events": 15,
    "returned_events": 1,
    "has_next": false,
    "has_previous": false,
    "next_offset": null,
    "previous_offset": null
  },
  "filters_applied": {
    "sport_key": null,
    "bookmaker_key": null,
    "market_key": "h2h",
    "positive_ev_only": false,
    "min_ev_threshold": null,
    "ev_method": "any",
    "limit": 20,
    "offset": 0
  },
  "metadata": {
    "generated_at": "2025-05-23T14:35:00",
    "ev_methods": {
      "standard_ev": "Expected value using raw bookmaker odds (includes vig)",
      "no_vig_ev": "Expected value using vig-removed fair odds"
    },
    "pagination_note": "Showing events 1-1 of 15 total events"
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
- `*_probability`: Supporting probability calculations
- `*_fair_odds`: Reference fair odds used
- `has_positive_*_ev`: Boolean flags for positive EV detection
- `calculated_at`: Timestamp of calculation

#### Opportunities Summary
- `total_bookmakers`: Number of bookmakers analyzed
- `positive_*_ev_count`: Count of positive EV opportunities by method
- `best_*_ev`: Best EV opportunity details by method
- `meets_threshold`: Whether event meets specified EV threshold (if applicable)
- `threshold_details`: Applied threshold settings (if applicable)

#### Pagination Object
- `limit`: Number of events requested per page
- `offset`: Number of events skipped for pagination
- `total_events`: Total number of events in database matching filters
- `returned_events`: Number of events returned in this response
- `has_next`: Boolean indicating if more events are available
- `has_previous`: Boolean indicating if previous page exists
- `next_offset`: Offset value for next page (null if no next page)
- `previous_offset`: Offset value for previous page (null if no previous page)

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

#### 4. Pagination Examples
```bash
# Get first page (events 1-20)
curl "http://localhost:8000/api/ev-opportunities?limit=20&offset=0"

# Get second page (events 21-40)
curl "http://localhost:8000/api/ev-opportunities?limit=20&offset=20"

# Get third page (events 41-60)
curl "http://localhost:8000/api/ev-opportunities?limit=20&offset=40"
```

#### 5. EV Threshold Filtering
```bash

# Medium opportunities: any EV method >= $5
curl "http://localhost:8000/api/ev-opportunities?min_ev_threshold=5.0&ev_method=any"

# Conservative opportunities: no-vig EV >= $3
curl "http://localhost:8000/api/ev-opportunities?min_ev_threshold=3.0&ev_method=no_vig"
```

#### 6. Combined Filtering
```bash

# Safe bets: positive EV across all methods
curl "http://localhost:8000/api/ev-opportunities?positive_ev_only=true&min_ev_threshold=1.0&ev_method=any"
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