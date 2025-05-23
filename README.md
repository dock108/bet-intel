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

**Enhanced Design & Functionality:**
- **Descriptive Outcome Labels**: Clear labels like "Red Sox Win", "Orioles Win" instead of generic codes
- **Smart EV Sorting**: Bookmakers automatically sorted by Expected Value (highest to lowest)
- **Accurate Best Line Logic**: Shows actual bookmaker with highest positive EV, or "No Positive EV Available"
- **Sport Icons**: Visual indicators (⚾ for baseball, 🏈 for football) for quick identification

**EV Indicators:**
- 🔥 **HOT**: EV > 2% (High-value opportunities)
- ✅ **SAFE**: EV > 0% (Positive expected value)
- ⚠️ **CAUTION**: EV > -2% (Near break-even)
- ❌ **AVOID**: EV < -2% (Negative expected value)

**Recommended P2P Bet Section:**
- **Multiple Outcome Display**: Shows all profitable outcomes (A, B, C) when available
- **Calculated P2P Odds**: Automatically applies 2% commission + 2.5% EV safety buffer
- **Clear Outcome Descriptions**: Shows exactly which team/outcome to bet on for each opportunity
- **Target EV**: Aims for 2.5% positive EV after all fees and buffers (between 2-3% range)
- **Dual Information**: For positive EV bets, shows both original odds/EV and fee-adjusted odds/EV
- **Adjusted EV Display**: Expected value after all fees and buffers applied
- **Affiliate Integration Ready**: Placeholder buttons for "Place Bets on [P2P Exchange Placeholder]"
- **Alternative Options**: Secondary button for additional P2P platforms

**Sorted Bookmaker Analysis:**
- **EV-Based Sorting**: All bookmakers ranked by their best available EV (highest first)
- **P2P Fee Transparency**: P2P exchanges show real EV after 2% fees are applied
- **Dual Display for P2P**: Shows both original odds and fee-adjusted odds
- **Fee Impact Warnings**: Clear alerts when P2P opportunities become negative EV after fees
- **Visual EV Indicators**: ✅ for positive EV bookmakers, ❌ for negative EV (after fees for P2P)
- **Descriptive Bet Labels**: Instead of "outcome_A", shows "Red Sox Win: +120"
- **EV Badges**: Color-coded badges showing each bookmaker's best EV percentage
- **P2P Identification**: Special badges and color coding for peer-to-peer exchanges
- **Expandable View**: "Show X more bookmakers" for comprehensive analysis

**Best Line Summary:**
- **Accurate Best Line**: Shows bookmaker with actual highest positive EV
- **No False Positives**: Clearly states "No Positive EV Available" when applicable
- **Quick Metrics**: Best EV percentage and positive opportunity count at a glance

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

### P2P Calculation Methodology
The platform applies a transparent approach to P2P exchange analysis:

**Fee Transparency (Real-Time Display):**
1. **Original Odds Display**: Shows the posted odds on P2P exchanges
2. **Fee-Adjusted Odds**: Displays odds after applying 2% commission
3. **Real EV Calculation**: Shows actual expected value after fees
4. **Impact Warnings**: Alerts when originally positive EV becomes negative after fees

**P2P Recommendation Logic:**
1. **Commission Removal**: Subtracts 2% for typical P2P exchange fees
2. **Safety Buffer**: Additional 2.5% EV buffer to account for:
   - Market movement between analysis and bet placement
   - Minor calculation variations
   - Risk management for user protection
3. **Target EV**: Aims for 2.5% positive EV after all adjustments (optimal 2-3% range)
4. **Multiple Outcomes**: Displays all profitable outcomes (A, B, C) when multiple opportunities exist
5. **Adjusted Odds Display**: Shows recommended odds after all adjustments
6. **Only True Positive EV**: Only displays P2P recommendations when final EV remains positive after all fees

**Sorting Priority**: P2P bookmakers are sorted by their fee-adjusted EV, ensuring traditional sportsbooks with positive EV rank above P2P exchanges with negative EV after fees.

### Affiliate Integration Framework
- **Placeholder System**: Ready-to-implement affiliate link structure
- **Exchange Flexibility**: Supports multiple P2P platforms simultaneously
- **Clear CTAs**: Dedicated action buttons for immediate bet placement
- **Alternative Options**: Secondary pathways for user choice and comparison

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