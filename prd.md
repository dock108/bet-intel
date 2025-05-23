# Product Requirements Document (PRD): AI-Assisted Peer-to-Peer Betting Intelligence

## Overview

This product leverages real-time sportsbook odds data from top market-makers to empower users to identify and set advantageous "limit order-style" bets on emerging peer-to-peer (P2P) betting platforms like Sporttrade, ProphetX, and Novig. Initially, the product will use the free tier of The Odds API for odds data. The goal is to automate value identification, clearly communicate optimal betting strategies, educate users on the unique P2P betting model, and monetize through premium subscriptions and affiliate links.

## Objectives

* Provide real-time value detection comparing sportsbook odds to P2P exchanges.
* Empower users to confidently place advantageous "limit-order" style bets.
* Educate users unfamiliar with P2P exchanges (Sporttrade, ProphetX, Novig).
* Generate revenue via affiliate links and premium subscription plans.
* Capture and store opening and closing odds for future analytics and internal use.

## Product Tiers

### Free Version

* Limited to one selected sportsbook and one P2P exchange for data access.
* Basic odds search functionality.
* Limited educational content about P2P betting.
* Simple recommended odds for select events.

### Paid Version (Premium)

* Access to multiple sportsbooks (DraftKings, FanDuel, Pinnacle or Caesars).
* Access to multiple P2P platforms (Sporttrade, ProphetX, Novig).
* Advanced AI-driven formulas and machine learning (ML) integrations.
* Comprehensive Monte Carlo simulations and Bayesian odds adjustments.
* Aggregated odds and market averages from multiple sources.
* Full historical odds storage and detailed analytics.
* Real-time alerts and extensive educational resources.

## User Stories

* **Value Discovery:** Users see clearly labeled, real-time betting opportunities with positive expected value.
* **Odds Search:** Users easily search current market odds for specific events, viewing recommended odds to place limit orders on P2P exchanges.
* **Educational Component:** New users access quick, easy-to-understand content explaining peer-to-peer betting, its benefits, and how it differs from traditional sportsbooks.
* **Limit Order Betting:** Users set target odds for events (e.g., Pacers ML at -108 instead of market's -120), enabling "set it and forget it" bets, capitalizing if and when market conditions shift favorably.

## Must-Have Features

### 1. Odds Aggregation & Scraping

* Real-time odds sourcing initially from The Odds API (free tier).
* P2P odds sourcing from selected peer-to-peer exchange(s), initially through scraping liquidity data if necessary.

### 2. AI-Driven Value Calculation (Premium)

* Automated discrepancy detection (with customizable threshold).
* Recommended limit-order odds calculated via Bayesian and Monte Carlo methods.
* Aggregated odds and comprehensive market averages.

### 3. User Education and Onboarding

* Clear "What is P2P Betting?" onboarding section.
* Educational pop-ups/tooltips on demand explaining specific features.

### 4. Affiliate Monetization

* Integrated affiliate links directing users to sportsbooks (DraftKings, FanDuel, Caesars).
* Integrated referral and affiliate tracking for P2P platforms where available.

### 5. Limit Order Style Bet Suggestion

* Users input desired event and current market odds.
* Product outputs ideal odds to set as a "limit order" style bet on peer-to-peer platforms.
* Alerts users if and when suggested odds are available.

### 6. Simple, User-Focused Dashboard

* Web and mobile-friendly UI for ease-of-use.
* Quick "check-in" experience: instant updates and recommended bets at a glance.

### 7. Historical Odds Storage

* Automatically capture and store opening odds (first recorded odds).
* Automatically capture and store closing odds (final odds before event start).
* Data stored securely for future analytics, internal reviews, and performance tracking.

## Technical Requirements

* Backend: Python with FastAPI or Flask.
* Frontend: Minimal React web app, mobile-first responsive design.
* Database: SQLite for MVP; PostgreSQL/Supabase later.
* Deployment: Vercel or similar platform.
* APIs & Scraping: Initially using The Odds API (free tier); ProphetX API (official), Sporttrade API (official/request); liquidity scraping as necessary for P2P books.

## Monetization Strategy

* Affiliate Revenue: Commission from referrals to sportsbooks/P2P platforms.
* Premium Subscription: Real-time alerts, advanced analytics, unlimited searches, AI-driven insights.

## Roadmap & Timeline (60 Days MVP)

| Week | Milestone                                                              |
| ---- | ---------------------------------------------------------------------- |
| 1-2  | Secure The Odds API access and setup initial scraping (P2P liquidity). |
| 3-4  | Implement backend odds aggregation and value detection logic.          |
| 5    | Develop MVP frontend (dashboard, odds search, educational content).    |
| 6-7  | Integrate affiliate tracking; final UI/UX refinements.                 |
| 8    | Testing and internal beta launch; iterate based on user feedback.      |

## Legal Considerations

* No automated bet placement (user-initiated only).
* Ensure compliance with data sourcing terms.

## Conclusion

This product differentiates itself by empowering bettors to capitalize on peer-to-peer markets, offering clear value opportunities, robust educational support, innovative limit-order style betting recommendations, essential historical odds storage, and premium AI-driven analytics.
