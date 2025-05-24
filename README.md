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

2. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Start the FastAPI server:**
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
- `/` - Landing Page (conversion-focused introduction to Bet Intel)
- `/dashboard` - Live EV Dashboard (fetches real data)
- `/search-ai` - AI Search & Analysis (placeholder)
- `/education` - Education Center (comprehensive P2P betting guide)
- `/disclaimers` - Legal Disclaimers (comprehensive legal compliance)

## Frontend Features

### Landing Page (`/`)
**Purpose**: Conversion-focused landing page that introduces Bet Intel, showcases the value proposition, and guides users to explore the free dashboard and educational content.

**Content Sections**:
1. **Hero Section** - Compelling headline ("💡 Smarter Sports Betting Starts Here"), value proposition, and clear CTAs to dashboard and education
2. **What is Bet Intel?** - Four-card explanation of core platform features: real-time odds analysis, sharp line detection, P2P strategy optimization, and information-only service
3. **Free Features Available Now** - Three detailed feature cards highlighting Live EV Dashboard, Odds Comparisons, and Education Center with "FREE" badges and direct access buttons
4. **Premium Features Coming Soon** - Four preview cards for upcoming tools: AI Betting Assistant, Bet Alerts, Portfolio Tracker, and Advanced Analytics with "COMING SOON" badges
5. **Why P2P Betting CTA Section** - Explains "eBay for sports bets" concept, asymmetric risk benefits, and drives traffic to Education Center
6. **Final CTA Section** - Strong conversion section with social proof numbers and prominent dashboard access
7. **Footer** - Navigation links and responsible gambling disclaimer

**Conversion Features**:
- **Clear value proposition**: "Real-time +EV bets. Peer-to-peer odds intel. No fluff."
- **Multiple CTAs**: Primary focus on "Try the Free Dashboard" with secondary education links
- **Live dashboard preview**: Interactive card showing sample metrics (47 +EV bets, +4.2% best EV, 12 P2P opportunities)
- **Feature badges**: "FREE" for current features, "COMING SOON" for premium tools
- **Social proof elements**: "Join hundreds of sharp bettors" and "100% Free to Use"
- **Mobile-responsive design**: Optimized for all devices with Bootstrap framework

**Design Features**:
- **Hero section**: Full-width primary background with logo, headline, and preview card
- **Section variety**: Alternating backgrounds (white, light gray, primary, dark) for visual interest
- **Card-based layouts**: Consistent Bootstrap cards with headers, feature lists, and action buttons
- **Color-coded sections**: Green for free features, warning/secondary for premium, primary for CTAs
- **Professional branding**: BetIntel logo integration and consistent color scheme throughout
- **Footer disclaimer**: Soft responsible gambling message and platform clarification

### Dashboard Page
The main Dashboard (`/dashboard`) provides a comprehensive view of real-time EV opportunities:

#### Enhanced Summary Bar
- **Total Opportunities**: Live count of available betting opportunities
- **Best EV Available**: Highest expected value percentage currently available
- **Next Refresh Countdown**: Real-time countdown timer (3-minute intervals)
- **Active Sportsbooks**: Number of connected traditional sportsbooks
- **P2P Exchanges**: Number of peer-to-peer exchanges monitored
- **EV Method**: Calculation methodology (7-Step No-Vig)

### Education Page (`/education`)
**Purpose**: Comprehensive educational resource that teaches users P2P betting fundamentals, expected value concepts, and how to effectively use Bet Intel's recommendations.

**Content Sections**:
1. **What is P2P Betting?** - Explains peer-to-peer betting as "eBay for sports bets", key differences from traditional sportsbooks, and exchange commission structure
2. **Understanding Odds & Expected Value** - Covers American odds, implied probability, vig calculation, and EV formula with practical coin flip example
3. **How Bet Intel Calculates +EV** - Interactive 7-step methodology breakdown using Bootstrap accordion, sample calculations, and mathematical transparency
4. **What We're Offering** - Value proposition section explaining limit order strategy, analogies to eBay/stock trading, and reasons why others accept your odds
5. **How to Post a Bet** - Step-by-step guide from finding recommendations to posting on P2P exchanges, with supported platform buttons and sample bet example

**Design Features**:
- **Anchor-linkable sections** (`#p2p`, `#ev`, `#calculation`, `#offering`, `#howto`) for easy navigation
- **Visual learning aids**: Interactive accordions, comparison tables, flow diagrams, and highlighted formulas
- **Mobile-responsive Bootstrap layout** with cards, alerts, and progress indicators
- **BetIntel branding** with logo integration and consistent color scheme
- **Call-to-action section** linking to dashboard and legal disclaimers

### Disclaimers Page (`/disclaimers`)
**Purpose**: Comprehensive legal compliance page that protects Bet Intel from liability while educating users about their responsibilities and the risks associated with sports betting.

**Content Sections**:
1. **Nature of Service** - Clearly defines Bet Intel as informational analytics platform only, not a sportsbook or betting operator
2. **No Warranties or Guarantees** - Legal disclaimers about profit guarantees, accuracy limitations, and uncertainty inherent in sports outcomes
3. **Risk of Loss & Responsible Gambling** - Critical risk warnings, responsible gambling guidelines, and problem gambling resources (1-800-GAMBLER, ncpgambling.org)
4. **Age and Jurisdiction Requirements** - Legal age requirements (18+/21+), jurisdiction compliance responsibilities, and entertainment-only usage for restricted areas
5. **Affiliate Disclosure** - Transparency about affiliate relationships, objectivity commitments, and user choice preservation
6. **Methodology Transparency** - Links to Education Center for mathematical methodology, analysis scope, and calculation components
7. **Limitation of Liability** - Legal protection clauses, user responsibility acknowledgment, and service limitations
8. **Changes to Disclaimers** - Update policy and user notification procedures

**Legal Compliance Features**:
- **Professional tone** with clear, accessible language for legal requirements
- **Risk awareness emphasis** highlighting that betting should be entertainment, not investment
- **Responsible gambling resources** prominently featured with direct access buttons
- **User responsibility clarity** ensuring users understand their legal and financial responsibilities
- **Platform limitations** clearly distinguishing Bet Intel from actual betting operators
- **Affiliate transparency** maintaining trust while disclosing commercial relationships
- **Effective date tracking** for legal compliance and user notification
- **Cross-reference integration** linking to Education Center for methodology transparency

**Design Features**:
- **Bootstrap card layout** with color-coded sections for easy navigation
- **Alert boxes** for critical warnings and important information
- **Professional branding** with BetIntel logo integration and consistent styling
- **Mobile-responsive design** ensuring accessibility across all devices
- **Clear navigation** with prominent links back to Dashboard and Education Center
- **Contact accessibility** providing clear pathways for user questions and clarifications

#### OpportunityCard Component
Each betting opportunity is displayed using the reusable `OpportunityCard` component featuring a **Compact Design with Expandable Details**:

**Compact Card Layout (New Design):**
- **Essential Info First**: Displays only critical information by default for quick scanning
- **Smart Color Coding**: Cards have colored borders based on EV quality:
  - Green: Strong positive EV (>2%)
  - Blue: Positive EV (0-2%)
  - Yellow: Caution range (-2% to 0%)
  - Grey: Negative EV (<-2%)
- **Expandable Details**: Click "Details ⬇️" to reveal comprehensive analysis
- **Compact Spacing**: Reduced padding and margins for more cards per view

**Default Visible Information:**
- **Team Matchup**: Clear team names with sport icons (⚾ for baseball, 🏈 for football)
- **Event Details**: Sport, date, and time in compact format
- **Recommended Bets**: Up to 2 best opportunities with odds and EV percentages
- **Quick CTA**: Single "Place Bet" button for immediate action
- **EV Indicators**: Visual badges (🔥 HOT, ✅ SAFE, ⚠️ CAUTION, ❌ AVOID)

**Expandable Details Section:**
- **Summary Statistics**: Best EV, opportunity count, and bookmaker count
- **Detailed Bookmaker Analysis**: Complete list with EV-based sorting
- **P2P Fee Transparency**: Shows original odds vs fee-adjusted odds
- **Fee Impact Warnings**: Alerts when P2P opportunities become negative after fees
- **Visual EV Indicators**: ✅ for positive EV, ❌ for negative EV (after fees for P2P)

**Enhanced Design Features:**
- **Descriptive Outcome Labels**: Clear labels like "Red Sox Win", "Orioles Win" instead of generic codes
- **Smart EV Sorting**: Bookmakers automatically sorted by Expected Value (highest to lowest)
- **P2P Identification**: Special badges and color coding for peer-to-peer exchanges
- **Interactive Elements**: Smooth expand/collapse transitions with arrow indicators
- **Responsive Design**: Optimized spacing for both desktop and mobile devices

**P2P Calculation Display:**
- **Dual Information**: Shows both original odds/EV and fee-adjusted values
- **Target EV**: 2.5% positive EV after all fees and buffers (optimal 2-3% range)
- **Multiple Outcomes**: Displays all profitable outcomes when available
- **Clear Fee Impact**: Visual warnings when fees make opportunities unprofitable

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