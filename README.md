# Bet Intel - AI Betting Intelligence Platform

**Date**: May 23, 2025  
**Phase**: 2 - Frontend Scaffolding Complete

## Project Overview

Bet Intel is an AI-assisted peer-to-peer betting intelligence platform that identifies Expected Value (EV) opportunities across traditional sportsbooks and P2P exchanges. The platform uses advanced statistical models and real-time data polling to help users find profitable betting opportunities.

## Current Status

✅ **Completed in Phase 2:**
- Modern React frontend scaffolded with Bootstrap UI framework
- Multi-page routing implemented (Dashboard, SearchAI, Education, Disclaimers)
- Backend FastAPI services operational with EV calculation endpoints
- Real-time data polling from odds APIs
- Dashboard displaying live EV opportunities

🚧 **Upcoming Features (Future Phases):**
- AI-powered search and analysis tools
- Bayesian probability models
- Monte Carlo simulation capabilities
- Advanced educational content
- Comprehensive legal documentation

## Repository Structure

```
bet-intel/
├── backend/                    # FastAPI backend services
│   ├── main.py                # Main API server with EV endpoints
│   ├── requirements.txt       # Python dependencies
│   └── ...
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   │   ├── Navigation.js  # Main navigation header
│   │   │   └── OpportunityCard.js # Betting opportunity display card
│   │   ├── pages/            # Page components
│   │   │   ├── Dashboard.js   # Main EV dashboard (active)
│   │   │   ├── SearchAI.js    # AI search (placeholder)
│   │   │   ├── Education.js   # Educational content (placeholder)
│   │   │   └── Disclaimers.js # Legal disclaimers (placeholder)
│   │   ├── App.js            # Main React app with routing
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Bootstrap imports and custom styles
│   ├── public/
│   │   └── index.html        # HTML template with Bootstrap CDN
│   └── package.json          # Node.js dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore rules
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`
   - Health check: `http://localhost:8000/health`
   - EV endpoint: `http://localhost:8000/api/future-games-with-ev`

### Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the React development server:**
   ```bash
   npm start
   ```
   
   The frontend will be available at `http://localhost:3000`

### Full Application Access

Once both servers are running:
- **Frontend**: http://localhost:3000 (React app with Bootstrap UI)
- **Backend API**: http://localhost:8000 (FastAPI with EV calculations)

## Available Endpoints

### Backend API
- `GET /health` - Health check endpoint
- `GET /api/future-games-with-ev` - Returns EV opportunities with detailed analysis
  - Optional parameter: `?limit=10` to limit results
  
#### EV Data Structure
The `/api/future-games-with-ev` endpoint returns comprehensive betting data:

```json
{
  "total": 10,
  "methodology": {
    "calculation_method": "7-Step No-Vig",
    "core_bookmakers": {...},
    "explanation": "Advanced statistical methodology description"
  },
  "events": [
    {
      "home_team": "Team A",
      "away_team": "Team B", 
      "sport": "americanfootball_nfl",
      "commence_time": "2025-05-23T19:00:00Z",
      "summary": {
        "best_available_ev": 3.45,
        "positive_ev_count": 8
      },
      "bookmaker_analysis": {
        "bookmaker_key": {
          "bookmaker": {
            "title": "DraftKings",
            "is_p2p": false
          },
          "outcomes": {
            "h2h": [
              {
                "offered_odds": -110,
                "ev_percentage": 2.34,
                "fair_odds": -105
              }
            ]
          }
        }
      }
    }
  ]
}
```

### Frontend Pages
- `/` or `/dashboard` - Live EV Dashboard (fetches real data)
- `/search-ai` - AI Search & Analysis (placeholder)
- `/education` - Education Center (placeholder)
- `/disclaimers` - Legal Disclaimers (placeholder)

## Frontend Features

### Dashboard Page
The main Dashboard (`/dashboard`) provides a comprehensive view of real-time EV opportunities:

#### Enhanced Summary Bar
- **Total Opportunities**: Live count of available betting opportunities
- **Best EV Available**: Highest expected value percentage currently available
- **Next Refresh Countdown**: Real-time countdown timer (3-minute intervals)
- **Active Sportsbooks**: Number of connected traditional sportsbooks
- **P2P Exchanges**: Number of peer-to-peer exchanges monitored
- **EV Method**: Calculation methodology (7-Step No-Vig)

#### OpportunityCard Component
Each betting opportunity is displayed using the reusable `OpportunityCard` component featuring:

**EV Indicators:**
- 🔥 **HOT**: EV > 2% (High-value opportunities)
- ✅ **SAFE**: EV > 0% (Positive expected value)
- ⚠️ **CAUTION**: EV > -2% (Near break-even)
- ❌ **AVOID**: EV < -2% (Negative expected value)

**Matchup Details:**
- Team names and sport classification
- Event start time and date
- Best available EV percentage and dollar value
- Positive EV opportunity count

**Recommended Opportunities:**
- Best betting line identification
- Recommended stake size (2-5% of bankroll)
- Bookmaker/exchange source

**Detailed Analysis:**
- Up to 3 top bookmakers with odds comparison
- P2P exchange identification with special badges
- Individual outcome EV percentages
- Expandable view for additional bookmakers

### Real-Time Features
- **Auto-refresh**: Data updates every 3 minutes automatically
- **Live countdown**: Visual timer showing next refresh
- **Loading states**: Smooth loading indicators during data fetching
- **Error handling**: Graceful error messages with retry functionality
- **Responsive design**: Optimized for desktop, tablet, and mobile devices

## Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Python 3.8+** - Core language
- **Odds API Integration** - Real-time sports betting data
- **7-Step No-Vig EV Calculation** - Proprietary methodology

### Frontend
- **React 18** - Modern frontend framework
- **React Router** - Client-side routing
- **Bootstrap 5** - Responsive UI framework
- **Font Awesome** - Icons
- **Axios** - HTTP client for API requests

## Development Notes

### Current Implementation
- Dashboard successfully fetches and displays live EV data from the backend
- Responsive design works across desktop and mobile devices
- Auto-refresh functionality updates data every 3 minutes
- Error handling and loading states implemented

### Methodology
The platform uses a **7-Step No-Vig methodology** for EV calculations across 6+ core bookmakers, providing accurate expected value assessments for both traditional sportsbooks and P2P exchanges.

## Future Development

The next phases will focus on:
1. **AI Integration** - Natural language queries and advanced filtering
2. **Bayesian Models** - Advanced probability calculations
3. **Monte Carlo Simulations** - Risk assessment and scenario modeling
4. **Educational Content** - Comprehensive betting strategy resources
5. **Legal Framework** - Complete terms of service and compliance documentation

## Contributing

This is currently a private development project. Future phases will include contribution guidelines and open-source considerations.

## License

Proprietary - All rights reserved.

---

**Last Updated**: May 23, 2025  
**Current Phase**: 2 Complete - Ready for Phase 3 AI Integration 