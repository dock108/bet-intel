# Frontend Design Documentation

## MVP Dashboard Design Overview

**Last Updated:** May 23, 2025  
**Version:** 1.3  
**Target Platform:** Web (Responsive), Mobile-first

## Design Philosophy

The MVP dashboard follows a **data-first, minimal complexity** approach prioritizing:

1. **Immediate Value Recognition** - Users should instantly see top EV opportunities
2. **Cognitive Load Reduction** - Clean, scannable information hierarchy
3. **Mobile-First Responsive** - Primary interaction on mobile devices
4. **Progressive Disclosure** - Essential info first, details on demand

## Dashboard Structure & Layout

### Primary Navigation Layout
```
[Logo/Brand]                    [Settings] [Menu]
======================================
|              HEADER                  |
|  Quick Stats Bar + Search/Filter     |
======================================
|                                      |
|         MAIN CONTENT AREA            |
|                                      |
|  • Top EV Opportunities (Cards)      |
|  • Upcoming Events (List/Grid)       |
|  • Quick Actions                     |
|                                      |
======================================
|             FOOTER/NAV              |
| [Dashboard] [Search] [Alerts] [More] |
======================================
```

### Information Hierarchy

#### Level 1: Quick Stats Header
- **Total Active Opportunities** (count)
- **Best Current EV** (value + %)
- **Next Game** (time countdown)
- **Active Bookmakers** (count)

#### Level 2: Top EV Opportunities (Cards)
- **Primary Display:** 3-6 cards showing highest EV bets
- **Card Content:**
  - Event (Teams + Sport Icon)
  - Commence Time
  - Bookmaker
  - **EV Value** (highlighted, all 3 types)
  - **Odds** (American format)
  - Quick Action Button

#### Level 3: Upcoming Events List
- **Secondary Display:** Chronological list of events
- **Compact Format:**
  - Time | Sport | Teams
  - Best EV indicator
  - Number of opportunities

## Component Design Specifications

### EV Opportunity Card
```
┌─────────────────────────────────────┐
│ [SPORT_ICON] Sport Name        🔥  │
│ Away Team @ Home Team               │
│ ⏰ 7:30 PM ET • Today               │
│                                     │
│ 📊 DraftKings                       │
│ ┌─────────────────────────────────┐ │
│ │ Away Team Win  +150 → +EV $12.5│ │
│ │ Standard: +$8.2 | No-Vig: +$10│ │
│ │ Weighted: +$12.5              │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [View Details] [Add to Watchlist]   │
└─────────────────────────────────────┘
```

### Quick Stats Bar
```
┌─────────────────────────────────────┐
│ 🎯 12 Opportunities  ⭐ Best: +$24.5│
│ ⏰ Next: 45m         📱 6 Books     │
└─────────────────────────────────────┘
```

### Event List Item
```
┌─────────────────────────────────────┐
│ 7:30 PM  [🏀] Lakers @ Warriors     │
│ 🔥 3 EVs • Best: +$15.2 • DraftKings│
└─────────────────────────────────────┘
```

## Odds Search & Results Component Design

### Search Component Layout
```
┌─────────────────────────────────────┐
│ 🔍 [Search teams, events, sports...] │
│                               [🔧] │ 
├─────────────────────────────────────┤
│ 🏀 NBA  🏈 NFL  ⚾ MLB  🏒 NHL    │
│                                     │
│ [All Books] [EV > $5] [Today Only]  │
└─────────────────────────────────────┘
```

### Search Results Layout
```
┌─────────────────────────────────────┐
│ 📊 15 results • Sort: Best EV ▼     │
├─────────────────────────────────────┤
│ 🏀 Lakers @ Warriors  7:30 PM      │
│ Pin: +145 | DK: +150 | FD: +140    │
│ EV: +$24.5 (W) | +$21.4 (NV) | +$18│
│ [View Details]               [📍]   │
├─────────────────────────────────────┤
│ 🏈 Chiefs @ Bills  8:20 PM          │
│ Pin: -108 | DK: -110 | FD: -105    │
│ EV: +$12.3 (W) | +$10.2 (NV) | +$8 │
│ [View Details]               [📍]   │
└─────────────────────────────────────┘
```

### Search Component Specifications

#### Search Input Field
- **Placeholder:** "Search teams, events, sports..."
- **Auto-complete:** Real-time suggestions as user types
- **Search Scope:** Team names, event descriptions, sport types
- **Keyboard Support:** Enter to search, ESC to clear
- **Voice Search:** Microphone icon for mobile accessibility

#### Quick Sport Filters
- **Visual Design:** Horizontal pill buttons with sport icons
- **Sports Covered:** NBA (🏀), NFL (🏈), MLB (⚾), NHL (🏒), +More
- **Interaction:** Single-tap to filter, tap again to remove filter
- **Mobile Behavior:** Horizontal scroll for additional sports

#### Advanced Filter Panel
```
┌─────────────────────────────────────┐
│ 📅 Time Range                       │
│ ● Today  ○ Tomorrow  ○ This Week    │
│                                     │
│ 📊 Bookmakers                       │
│ ☑ Pinnacle  ☑ DraftKings  ☑ FanDuel│
│ ☑ Caesars   ☐ BetMGM      ☐ Betway │
│                                     │
│ 💰 EV Threshold                     │
│ [___$5___] Minimum Expected Value   │
│                                     │
│ [Clear All]              [Apply]    │
└─────────────────────────────────────┘
```

### Search Results Specifications

#### Results Header
- **Results Count:** "📊 15 results found"
- **Sort Options:** Best EV, Time, Sport, Alphabetical
- **View Toggle:** List view ⇄ Grid view (desktop only)
- **Refresh Button:** Manual refresh with loading indicator

#### Search Result Card
```
┌─────────────────────────────────────┐
│ 🏀 NBA • Today, 7:30 PM ET          │
│ Lakers @ Warriors                   │
│                                     │
│ 📊 Odds Comparison                  │
│ ┌─────────────────────────────────┐ │
│ │ Pin  DK   FD   Best EV          │ │
│ │+145 +150 +140  Lakers +$24.50  │ │
│ │-165 -170 -160  Warriors -$18.20│ │
│ └─────────────────────────────────┘ │
│                                     │
│ 💡 EV Analysis                      │
│ Weighted: +$24.50 | No-Vig: +$21.40│
│ Standard: +$18.20 | Confidence: High│
│                                     │
│ [View Full Analysis] [📍 Watchlist] │
└─────────────────────────────────────┘
```

#### Compact Result Item (Mobile)
```
┌─────────────────────────────────────┐
│ 7:30 PM  🏀  Lakers @ Warriors      │
│ Best: +$24.5 (DK +150) • 3 books   │
│ W: +$24.5 | NV: +$21.4 | S: +$18.2 │
│                              [📍]   │
└─────────────────────────────────────┘
```

### Search Interaction Patterns

#### Search Flow
1. **Initial State:** Empty search with sport filter pills visible
2. **Typing:** Real-time suggestions dropdown appears
3. **Selection:** Auto-search on suggestion click or Enter key
4. **Results:** Immediate display with loading states
5. **Refinement:** Filters update results without page reload

#### Auto-complete Suggestions
```
┌─────────────────────────────────────┐
│ 🔍 laker                            │
├─────────────────────────────────────┤
│ 🏀 Lakers @ Warriors (Tonight)      │
│ 🏀 Lakers vs Celtics (Tomorrow)     │
│ 📊 Los Angeles Lakers (Team)        │
│ 🏀 NBA (League)                     │
└─────────────────────────────────────┘
```

#### Filter Combinations
- **Sport + Time:** "NBA games today"
- **Team + Bookmaker:** "Lakers games on DraftKings"
- **EV + Time:** "High EV bets tonight"
- **Custom:** User-defined filter combinations

### Data Integration & API Usage

#### Primary Endpoints
- **`GET /api/ev-opportunities`** - Main search with query parameters
- **`GET /api/events`** - Event auto-complete suggestions
- **`GET /api/bookmakers`** - Available bookmaker options

#### Search Parameters
```typescript
interface SearchParams {
  query?: string              // Text search
  sport_key?: string         // Sport filter
  bookmaker_keys?: string[]  // Bookmaker filter
  min_ev_threshold?: number  // EV filter
  time_range?: 'today' | 'tomorrow' | 'week'
  sort_by?: 'ev' | 'time' | 'sport'
  limit?: number
  offset?: number
}
```

#### Real-time Search
- **Debounced Input:** 300ms delay to prevent excessive API calls
- **Cache Strategy:** Cache results for 30 seconds
- **Background Updates:** Refresh results every 60 seconds
- **Offline Handling:** Show cached results with offline indicator

### Loading & Empty States

#### Loading States
```
┌─────────────────────────────────────┐
│ 🔍 Searching...                     │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ ▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │ ← Skeleton loading
│ │ ▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│ │ ▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

#### Empty Search State
```
┌─────────────────────────────────────┐
│          🔍                         │
│    Search for Events & Odds         │
│                                     │
│  Try searching for:                 │
│  • "Lakers" - specific teams        │
│  • "NBA" - sports leagues          │
│  • "tonight" - time-based          │
│                                     │
│    [Popular: Lakers, Chiefs, etc.]  │
└─────────────────────────────────────┘
```

#### No Results State
```
┌─────────────────────────────────────┐
│          🤷‍♂️                         │
│    No Results Found                 │
│                                     │
│  No events match your search.       │
│  Try adjusting your filters or      │
│  search for different terms.        │
│                                     │
│  [Clear Filters] [Try Popular Terms]│
└─────────────────────────────────────┘
```

### Mobile Optimization

#### Mobile Search Interface
- **Full-width search bar** with prominent tap target
- **Bottom sheet filters** instead of sidebar
- **Swipe gestures** for quick actions
- **Voice search integration** for hands-free operation

#### Mobile Results Display
- **Compact card design** optimized for scrolling
- **Quick action buttons** (Watchlist, Share)
- **Infinite scroll** for seamless browsing
- **Pull-to-refresh** for manual updates

### Accessibility Features

#### Keyboard Navigation
- **Tab order:** Search → Filters → Results → Actions
- **Arrow keys:** Navigate through suggestions and results
- **Enter/Space:** Select items and trigger actions
- **Escape:** Close modals and clear search

#### Screen Reader Support
- **ARIA labels:** Descriptive labels for all interactive elements
- **Live regions:** Announce search results and updates
- **Role attributes:** Proper semantic markup for lists and buttons
- **Alt text:** Descriptive text for all icons and images

#### Visual Accessibility
- **High contrast mode** support
- **Focus indicators** clearly visible
- **Text scaling** up to 200% without layout breaks
- **Color-blind friendly** color combinations

### Performance Considerations

#### Search Optimization
- **Client-side caching** of frequent searches
- **Prefetch popular events** during idle time
- **Lazy loading** of images and non-critical content
- **Request batching** to minimize API calls

#### Rendering Performance
- **Virtual scrolling** for large result sets
- **Image optimization** with WebP format
- **CSS containment** for better paint performance
- **JavaScript code splitting** by feature

---

## Detailed Event View Component Design

### Event View Layout Structure
```
┌─────────────────────────────────────┐
│ [← Back] Lakers @ Warriors    [📍] │
│ NBA • Today, 7:30 PM ET             │
├─────────────────────────────────────┤
│                                     │
│         EV OPPORTUNITY SUMMARY      │
│  🔥 High Confidence • Best: +$24.50 │
│                                     │
├─────────────────────────────────────┤
│                                     │
│       COMPREHENSIVE ODDS TABLE      │
│                                     │
├─────────────────────────────────────┤
│                                     │
│         EV BREAKDOWN ANALYSIS       │
│                                     │
├─────────────────────────────────────┤
│                                     │
│        WHY THIS HAS POSITIVE EV     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│         LIMIT ORDER SECTION         │
│                                     │
└─────────────────────────────────────┘
```

### Event Header Component
```
┌─────────────────────────────────────┐
│ [← Back to Search] Lakers @ Warriors │
│ 🏀 NBA • Today, 7:30 PM ET          │
│ ⏰ Game starts in 4h 23m             │
│                                [📍] │
└─────────────────────────────────────┘
```

### EV Opportunity Summary
```
┌─────────────────────────────────────┐
│ 🔥 HIGH CONFIDENCE OPPORTUNITY      │
│                                     │
│ Best EV: +$24.50 (DraftKings)      │
│ Lakers Win at +150 odds             │
│                                     │
│ ⭐ Confidence Score: 94/100         │
│ 📊 Market Efficiency: Low          │
│ ⏰ Opportunity Window: 4h 23m       │
└─────────────────────────────────────┘
```

### Comprehensive Odds Comparison Table
```
┌─────────────────────────────────────┐
│ 📊 Complete Odds Comparison         │
│                                     │
│ Outcome    | Pin  | DK   | FD   | EV│
│ Lakers Win |+145  |+150  |+140  |+24│
│ Warriors W.|-165  |-170  |-160  |-18│
│ Over 225.5 |+110  |+105  |+115  | +5│
│ Under 225.5|-130  |-125  |-135  | -3│
│                                     │
│ 💡 Best Opportunities Highlighted   │
└─────────────────────────────────────┘
```

### EV Breakdown Analysis
```
┌─────────────────────────────────────┐
│ 📈 Expected Value Analysis          │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Weighted Fair EV:    +$24.50   │ │ ← Primary
│ │ No-Vig EV:          +$21.40   │ │
│ │ Standard EV:         +$18.20   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 🎯 Key Metrics:                     │
│ • True Probability: 41.2%           │
│ • Implied Probability: 40.0%       │
│ • Edge: +1.2%                      │
│ • Kelly Criterion: 2.4% of bankroll│
└─────────────────────────────────────┘
```

### EV Explanation Section
```
┌─────────────────────────────────────┐
│ 🧠 Why This Has Positive EV        │
│                                     │
│ 1. 📊 Market Inefficiency          │
│    DraftKings offering +150 while   │
│    fair odds should be around +143  │
│                                     │
│ 2. 🎯 Sharp Money Indicators        │
│    • Pinnacle (sharp book): +145    │
│    • Recent line movement: +140→+150│
│    • Volume: 67% on Warriors        │
│                                     │
│ 3. ⚖️ Calculated Fair Value        │
│    • Weighted model: 41.2% prob     │
│    • Vig-removed: 40.8% prob       │
│    • Historical: 41.5% prob        │
│                                     │
│ 💡 This represents a 2.4% edge over │
│    the true probability of the event│
└─────────────────────────────────────┘
```

### Limit Order Component
```
┌─────────────────────────────────────┐
│ 🎯 Set Limit Order                  │
│                                     │
│ Current: +150 → Target: [+155    ]  │
│ ┌─────────────────────────────────┐ │
│ │ I want to bet Lakers Win        │ │
│ │ At odds of +155 or better       │ │
│ │ Stake: $100                     │ │
│ │                                 │ │
│ │ Potential Profit: $155          │ │
│ │ Alert me when: ☑ Available     │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Set Alert] [Go to DraftKings]     │
└─────────────────────────────────────┘
```

### Detailed Event View Specifications

#### Navigation & Header
- **Back Button:** Clear navigation to previous page (Dashboard/Search)
- **Event Title:** Teams with @ symbol (Away @ Home format)
- **Context Info:** Sport, Date/Time, Countdown to game start
- **Quick Actions:** Watchlist toggle, Share button
- **Breadcrumb:** Dashboard > Search > Event (desktop)

#### EV Opportunity Summary
- **Confidence Indicator:** Visual badge (🔥 High, 📈 Medium, ✅ Low)
- **Best EV Display:** Prominent callout with bookmaker and odds
- **Quick Metrics:** Confidence score, market efficiency, time remaining
- **Visual Hierarchy:** Most important info largest and first

#### Comprehensive Odds Table
- **All Markets:** H2H, Spreads, Totals displayed in tabs or sections
- **All Bookmakers:** Minimum 3 books (Pinnacle, DraftKings, FanDuel)
- **EV Highlighting:** Color-coded cells for positive/negative EV
- **Sortable Columns:** Users can sort by EV, odds, bookmaker
- **Mobile Optimization:** Horizontal scroll or accordion layout

#### EV Analysis Section
```typescript
interface EVAnalysis {
  weightedFairEV: number      // Primary EV calculation
  noVigEV: number            // Vig-removed calculation  
  standardEV: number         // Raw odds calculation
  trueProbability: number    // Calculated fair probability
  impliedProbability: number // Bookmaker's implied probability
  edge: number              // Percentage edge
  kellyPercentage: number   // Suggested bet sizing
}
```

#### EV Explanation Logic
- **Market Inefficiency:** Why odds are mispriced
- **Sharp Money Indicators:** Professional betting patterns
- **Fair Value Calculation:** How true probability was determined
- **Historical Context:** Past performance in similar situations
- **Risk Assessment:** Variance and confidence intervals

#### Limit Order Functionality
- **Target Odds Input:** User-defined odds threshold
- **Stake Amount:** Bet sizing with kelly suggestion
- **Alert Options:** Email, push notification, SMS
- **Bookmaker Links:** Direct links with affiliate tracking
- **Order History:** Track previous limit orders

### Mobile Optimizations

#### Mobile Event View Layout
```
┌─────────────────────────────────────┐
│ [← Back] Lakers @ Warriors    [📍] │
│ 🏀 NBA • 7:30 PM • 4h 23m           │
├─────────────────────────────────────┤
│ 🔥 BEST: +$24.50 (DraftKings)      │
│ Lakers Win +150                     │
├─────────────────────────────────────┤
│ 📊 Odds (Tap to expand)             │
│ DK: +150 | Pin: +145 | FD: +140    │
├─────────────────────────────────────┤
│ 📈 EV: W:+$24.5 NV:+$21.4 S:+$18  │
├─────────────────────────────────────┤
│ 🧠 Why Positive EV? (Tap to read)   │
├─────────────────────────────────────┤
│ 🎯 Set Alert for Better Odds       │
│ [Target: +155] [Set Alert]          │
└─────────────────────────────────────┘
```

#### Mobile Interaction Patterns
- **Collapsible Sections:** Expandable details to save screen space
- **Swipe Gestures:** Swipe between different markets/outcomes
- **Sticky Headers:** Key info stays visible while scrolling
- **Bottom Action Bar:** Primary actions easily reachable

### Data Visualization Components

#### EV Trend Chart (Future Enhancement)
```
┌─────────────────────────────────────┐
│ 📈 EV Over Time (Last 24h)          │
│                                     │
│ +$30 ┌─────────────────┐            │
│ +$25 │        ●●●●●●●●●│            │
│ +$20 │      ●●        │            │
│ +$15 │    ●●          │            │
│ +$10 │  ●●            │            │
│ +$5  │●●              │            │
│ $0   └─────────────────┘            │
│      12h   6h    Now                │
└─────────────────────────────────────┘
```

#### Probability Distribution
```
┌─────────────────────────────────────┐
│ 🎲 Outcome Probabilities            │
│                                     │
│ Lakers Win    ████████░░ 41.2%      │
│ Warriors Win  ██████████ 58.8%      │
│                                     │
│ Fair Odds: Lakers +143, Warriors -167│
└─────────────────────────────────────┘
```

### Advanced Features

#### Historical Performance
- **Head-to-Head Record:** Last 10 games between teams
- **Recent Form:** Win/loss streaks and performance trends
- **Venue Analysis:** Home/away performance differences
- **Injury Report:** Key player availability impact

#### Market Analysis
- **Line Movement:** How odds have changed over time
- **Betting Volume:** Public vs sharp money percentages
- **Similar Games:** Historical outcomes in comparable situations
- **Weather Impact:** For outdoor sports

#### Risk Management
- **Variance Calculation:** Expected outcome distribution
- **Confidence Intervals:** Range of likely EV values
- **Bankroll Recommendations:** Kelly criterion and fractional kelly
- **Stop-Loss Suggestions:** Risk management thresholds

---

## Recommended Odds Component Design

### P2P Platform Integration Strategy

The Recommended Odds Component serves as a **manual guidance system** that bridges EV analysis with P2P platform execution. This component provides users with specific odds recommendations to manually set on peer-to-peer betting exchanges.

### Component Layout Structure
```
┌─────────────────────────────────────┐
│ 🎯 RECOMMENDED P2P ODDS             │
│ Manual Entry Guide                  │
├─────────────────────────────────────┤
│                                     │
│    P2P PLATFORM RECOMMENDATIONS     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│       MANUAL ENTRY GUIDANCE        │
│                                     │
├─────────────────────────────────────┤
│                                     │
│       EDUCATIONAL CONTENT           │
│                                     │
└─────────────────────────────────────┘
```

### P2P Platform Recommendations Section
```
┌─────────────────────────────────────┐
│ 🔥 Set These Odds Manually          │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 🏆 Novig                       │ │
│ │ Lakers Win: +165               │ │
│ │ Expected Fill: 15-30 min       │ │
│ │ Potential Profit: +$26.50     │ │
│ │ [Go to Novig] [Copy Odds]      │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 📈 Sporttrade                  │ │
│ │ Lakers Win: +160               │ │
│ │ Expected Fill: 20-45 min       │ │
│ │ Potential Profit: +$24.80     │ │
│ │ [Go to Sporttrade] [Copy Odds] │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ ⚡ ProphetX                     │ │
│ │ Lakers Win: +158               │ │
│ │ Expected Fill: 25-60 min       │ │
│ │ Potential Profit: +$23.70     │ │
│ │ [Go to ProphetX] [Copy Odds]   │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Manual Entry Guidance Section
```
┌─────────────────────────────────────┐
│ 📋 How to Set These Odds Manually   │
│                                     │
│ 1. 🔗 Click platform link above     │
│ 2. 🔍 Find "Lakers @ Warriors"       │
│ 3. 📝 Select "Lakers Win"            │
│ 4. 💰 Enter recommended odds         │
│ 5. 🎯 Set your stake amount          │
│ 6. ✅ Submit limit order             │
│                                     │
│ 💡 Your order will fill when someone │
│    accepts your odds or better      │
└─────────────────────────────────────┘
```

### Educational Content Section
```
┌─────────────────────────────────────┐
│ 🎓 Why P2P Betting?                 │
│                                     │
│ ✅ Better Odds: Set your own prices  │
│ ✅ No Limits: Bet any amount        │
│ ✅ Peer Trading: Bet against others  │
│ ✅ Fair Markets: Lower vig fees      │
│                                     │
│ ⚠️  Remember: Orders may not fill    │
│    immediately. Be patient!         │
│                                     │
│ [Learn More About P2P] [FAQ]        │
└─────────────────────────────────────┘
```

### Recommended Odds Component Specifications

#### P2P Platform Cards
- **Platform Branding:** Clear logos and colors for each platform
- **Recommended Odds:** Calculated based on EV analysis and platform liquidity
- **Expected Fill Time:** Historical data on order completion times
- **Potential Profit:** Real-time calculation based on stake
- **Direct Links:** Affiliate-tracked deep links to specific events
- **Copy Functionality:** One-click copy of recommended odds

#### Odds Calculation Logic
```typescript
interface P2POddsRecommendation {
  platform: 'novig' | 'sporttrade' | 'prophetx'
  recommendedOdds: number        // Calculated fair value + margin
  expectedFillTime: string       // "15-30 min" based on liquidity
  potentialProfit: number        // Based on default stake
  confidence: 'high' | 'medium' | 'low'
  liquidityScore: number         // 1-100 based on historical volume
}
```

#### Calculation Methodology
- **Base Fair Odds:** Start with weighted fair value calculation
- **Platform Premium:** Add 5-15 points based on platform liquidity
- **Fill Probability:** Adjust odds based on historical fill rates
- **Time Sensitivity:** Factor in game start time (closer = higher odds)

#### Manual Entry Guidance
- **Step-by-Step Instructions:** Clear, numbered process
- **Visual Cues:** Icons and highlights for each step
- **Platform-Specific Tips:** Unique guidance for each P2P platform
- **Error Prevention:** Common mistakes and how to avoid them

#### Educational Components
- **P2P Benefits:** Why use peer-to-peer vs traditional sportsbooks
- **Risk Disclosure:** Orders may not fill, partial fills possible
- **Best Practices:** Timing, stake sizing, patience requirements
- **FAQ Links:** Detailed explanations of P2P betting concepts

### Mobile Optimization

#### Mobile P2P Recommendations Layout
```
┌─────────────────────────────────────┐
│ 🎯 P2P Odds Recommendations         │
├─────────────────────────────────────┤
│ 🏆 Novig • Lakers +165             │
│ Profit: +$26.50 • Fill: 15-30m     │
│ [Go to Novig] [Copy: +165]          │
├─────────────────────────────────────┤
│ 📈 Sporttrade • Lakers +160        │
│ Profit: +$24.80 • Fill: 20-45m     │
│ [Go to Sporttrade] [Copy: +160]     │
├─────────────────────────────────────┤
│ ⚡ ProphetX • Lakers +158           │
│ Profit: +$23.70 • Fill: 25-60m     │
│ [Go to ProphetX] [Copy: +158]       │
└─────────────────────────────────────┘
```

#### Mobile Interaction Patterns
- **One-Tap Copy:** Odds automatically copied to clipboard
- **Deep Linking:** Direct navigation to specific event on platform
- **Swipe Actions:** Swipe to reveal additional platform options
- **Quick Stakes:** Pre-set stake amounts for rapid calculation

### Integration with Existing Event View

#### Placement Strategy
- **Position:** Between EV Analysis and Limit Order Alert sections
- **Hierarchy:** Secondary to traditional sportsbook analysis
- **Visual Weight:** Prominent but not overwhelming
- **Flow:** Natural progression from analysis to action

#### Data Synchronization
- **Real-Time Updates:** Odds refresh every 30 seconds
- **Availability Checks:** Verify event exists on each platform
- **Liquidity Monitoring:** Update fill time estimates based on volume
- **Error Handling:** Graceful degradation if platform unavailable

### P2P Platform Specifications

#### Novig Integration
- **Focus:** Highest liquidity, fastest fills
- **Odds Strategy:** Aggressive (fair value + 8-12 points)
- **Stake Recommendations:** $50-500 typical range
- **Deep Link Format:** `novig.com/bet/{event_id}?odds={odds}&stake={stake}`

#### Sporttrade Integration
- **Focus:** Balanced liquidity and odds
- **Odds Strategy:** Moderate (fair value + 6-10 points)  
- **Stake Recommendations:** $25-300 typical range
- **Deep Link Format:** `sporttrade.com/markets/{sport}/{event}?side={outcome}`

#### ProphetX Integration
- **Focus:** Advanced traders, higher stakes
- **Odds Strategy:** Conservative (fair value + 4-8 points)
- **Stake Recommendations:** $100-1000 typical range
- **Deep Link Format:** `prophetx.com/event/{event_id}/bet?type=back&odds={odds}`

### Advanced Features

#### Smart Recommendations
- **Liquidity Scoring:** Rank platforms by expected fill probability
- **Time-Based Adjustments:** More aggressive odds closer to game time
- **User Preferences:** Remember preferred platforms and stake sizes
- **Historical Performance:** Track which recommendations actually filled

#### Copy & Share Functionality
- **Odds Copying:** One-click copy of recommended odds to clipboard
- **Deep Link Sharing:** Share specific recommendations with others
- **Screenshot Tools:** Easy capture of recommendations for manual entry
- **QR Codes:** Mobile-friendly platform access

#### Risk Management
- **Stake Suggestions:** Based on Kelly criterion and bankroll management
- **Diversification Alerts:** Warn against over-concentration on single bet
- **Fill Rate Disclosure:** Historical percentage of similar orders that filled
- **Time Warnings:** Alert users about approaching game start times

### Error States & Edge Cases

#### Platform Unavailable
```
┌─────────────────────────────────────┐
│ ⚠️  Platform Temporarily Unavailable│
│                                     │
│ Novig is currently down for         │
│ maintenance. Try Sporttrade or      │
│ ProphetX instead.                   │
│                                     │
│ [Check Status] [Alternative Platforms]│
└─────────────────────────────────────┘
```

#### Low Liquidity Warning
```
┌─────────────────────────────────────┐
│ 🐌 Low Liquidity Alert              │
│                                     │
│ This event has limited trading      │
│ volume. Your order may take longer  │
│ to fill or may not fill at all.     │
│                                     │
│ [Understand Risks] [Continue Anyway]│
└─────────────────────────────────────┘
```

#### Event Not Available
```
┌─────────────────────────────────────┐
│ 🚫 Event Not Listed                 │
│                                     │
│ This event isn't available on P2P   │
│ platforms yet. Try traditional      │
│ sportsbooks instead.                │
│                                     │
│ [View Sportsbook Options]           │
└─────────────────────────────────────┘
```

### Performance Considerations

#### Loading Optimization
- **Lazy Loading:** Load P2P data after main event analysis
- **Caching Strategy:** Cache platform availability for 5 minutes
- **Progressive Enhancement:** Show basic odds first, enhance with fill times
- **Timeout Handling:** Fallback to manual entry if API calls fail

#### Real-Time Updates
- **WebSocket Integration:** Live odds updates from P2P platforms
- **Debounced Updates:** Limit update frequency to prevent UI flicker
- **Background Sync:** Refresh data when user returns to tab
- **Offline Handling:** Show last known good data with timestamp

---

## Color Palette & Visual Design

### Primary Colors
- **Success Green:** `#16a34a` (Positive EV)
- **Warning Amber:** `#d97706` (Moderate EV)
- **Danger Red:** `#dc2626` (Negative EV)
- **Primary Blue:** `#2563eb` (Actions, Links)
- **Neutral Gray:** `#6b7280` (Secondary text)

### Typography
- **Headers:** Inter Bold, 18-24px
- **Body:** Inter Regular, 14-16px
- **Numbers/EV:** Inter Medium, 16-20px (prominent)
- **Metadata:** Inter Regular, 12-14px

### Visual Hierarchy Indicators
- **High EV (>$15):** Green background, bold text
- **Medium EV ($5-15):** Amber border, medium weight
- **Low EV (<$5):** Standard card, normal weight

## Responsive Design Breakpoints

### Mobile (320px - 768px)
- **Single column layout**
- **Stacked EV cards** (full width)
- **Horizontal scroll** for stats bar
- **Bottom navigation** (fixed)

### Tablet (768px - 1024px)
- **Two column layout** for opportunity cards
- **Side navigation** (collapsible)
- **Expanded filter options**

### Desktop (1024px+)
- **Three column layout** for cards
- **Full sidebar navigation**
- **Advanced filtering panel**
- **Keyboard shortcuts**

## Component Library Selection

### Primary UI Framework: **Tailwind CSS + Headless UI**
**Rationale:** 
- Rapid prototyping capability
- Mobile-first responsive utilities
- Minimal bundle size
- Easy customization

### Key Components Needed:

#### 1. **Card Component**
```typescript
interface EVOpportunityCard {
  event: EventData
  evCalculations: EVCalculation[]
  bookmaker: Bookmaker
  primaryAction: () => void
}
```

#### 2. **Stats Display Component**
```typescript
interface QuickStats {
  totalOpportunities: number
  bestEvValue: number
  nextGameTime: string
  activeBookmakers: number
}
```

#### 3. **Event List Component**
```typescript
interface EventListItem {
  event: EventData
  opportunityCount: number
  bestEv: EVSummary
  timeToCommence: string
}
```

#### 4. **Filter Panel Component**
```typescript
interface FilterOptions {
  sportKeys: string[]
  bookmakers: string[]
  evThreshold: number
  timeRange: TimeRange
}
```

#### 5. **Search Component**
```typescript
interface SearchComponent {
  query: string
  suggestions: SearchSuggestion[]
  filters: FilterOptions
  onSearch: (query: string) => void
  onFilter: (filters: FilterOptions) => void
}
```

#### 6. **Search Results Component**
```typescript
interface SearchResults {
  results: SearchResult[]
  totalCount: number
  loading: boolean
  sortBy: SortOption
  viewMode: 'list' | 'grid'
}
```

#### 7. **Detailed Event View Component**
```typescript
interface DetailedEventView {
  event: EventData
  evAnalysis: EVAnalysis
  oddsComparison: OddsComparison[]
  explanation: EVExplanation
  limitOrder: LimitOrderConfig
  onBack: () => void
  onSetAlert: (config: AlertConfig) => void
}
```

#### 8. **Limit Order Component**
```typescript
interface LimitOrderComponent {
  currentOdds: number
  targetOdds: number
  stakeAmount: number
  outcome: string
  bookmaker: string
  onSetAlert: (config: LimitOrderConfig) => void
}
```

#### 9. **Recommended Odds Component**
```typescript
interface RecommendedOddsComponent {
  event: EventData
  p2pRecommendations: P2POddsRecommendation[]
  userStake: number
  onCopyOdds: (platform: string, odds: number) => void
  onPlatformNavigate: (platform: string, deepLink: string) => void
}
```

## Data Flow & API Integration

### Primary API Endpoints Used
1. **`GET /api/ev-opportunities`** - Main dashboard data
2. **`GET /api/events`** - Upcoming events list
3. **`GET /api/stats`** - Quick stats bar data
4. **`GET /api/events/{event_id}/analysis`** - Detailed event analysis
5. **`POST /api/alerts`** - Create limit order alerts
6. **`GET /api/p2p/recommendations/{event_id}`** - P2P platform odds recommendations

### Real-time Updates Strategy
- **Initial Load:** Full data fetch
- **Polling:** Every 60 seconds for EV updates
- **WebSocket (Future):** Real-time odds changes

### Caching Strategy
- **Client-side caching:** 30 seconds for opportunity data
- **Background refresh:** Update cache silently
- **Error fallback:** Show cached data with timestamp

## User Experience (UX) Considerations

### Primary User Goals
1. **Quick EV Identification** - See best opportunities immediately
2. **Event Discovery** - Find upcoming games with value
3. **Opportunity Comparison** - Compare EV across bookmakers
4. **Action Taking** - Easy navigation to bookmaker

### Interaction Patterns

#### Card Interactions
- **Tap/Click:** View detailed breakdown
- **Long Press:** Add to watchlist (mobile)
- **Swipe Left:** Quick dismiss (mobile)
- **Swipe Right:** Quick action to bookmaker (mobile)

#### Filter Interactions  
- **Quick Filters:** Sport type, Time range (buttons)
- **Advanced Filters:** EV threshold, Bookmaker selection (modal)
- **Sort Options:** EV value, Time, Sport (dropdown)

#### Navigation Patterns
- **Bottom Tab Navigation** (mobile)
- **Side Navigation** (tablet/desktop)
- **Breadcrumb Navigation** for detail views

## Accessibility & Performance

### Accessibility Standards (WCAG 2.1 AA)
- **Color Contrast:** Minimum 4.5:1 ratio
- **Keyboard Navigation:** Full functionality without mouse
- **Screen Reader Support:** Proper ARIA labels
- **Focus Indicators:** Clear visual focus states

### Performance Targets
- **First Contentful Paint:** < 1.5s
- **Largest Contentful Paint:** < 2.5s
- **Cumulative Layout Shift:** < 0.1
- **First Input Delay:** < 100ms

### Optimization Strategies
- **Code Splitting:** Load dashboard components on-demand
- **Image Optimization:** Sport icons as SVG sprites
- **API Batching:** Combine multiple data requests
- **Lazy Loading:** Defer non-critical content

## Testing Strategy

### Component Testing
- **Unit Tests:** Individual component logic
- **Integration Tests:** API data integration
- **Visual Regression:** Ensure design consistency

### User Testing
- **Usability Testing:** 5-8 users, task-based scenarios
- **A/B Testing:** EV display formats, card layouts
- **Performance Testing:** Real device testing across breakpoints

### Key Testing Scenarios
1. **Quick EV Recognition** - Time to identify best opportunity
2. **Mobile Usability** - One-handed operation
3. **Data Loading States** - Skeleton screens, error handling
4. **Filter Effectiveness** - Narrow down relevant opportunities

## Design System & Reusability

### Component Structure
```
/components
  /dashboard
    - EVOpportunityCard.tsx
    - QuickStatsBar.tsx
    - EventList.tsx
    - FilterPanel.tsx
  /search
    - SearchBar.tsx
    - SearchResults.tsx
    - SearchFilters.tsx
    - ResultCard.tsx
  /event-detail
    - EventHeader.tsx
    - EVAnalysis.tsx
    - OddsTable.tsx
    - EVExplanation.tsx
    - LimitOrder.tsx
    - RecommendedOdds.tsx
  /shared
    - Button.tsx
    - Card.tsx
    - Badge.tsx
    - Spinner.tsx
```

### Design Token System
```typescript
// Design tokens
const tokens = {
  spacing: { xs: 4, sm: 8, md: 16, lg: 24, xl: 32 },
  colors: { /* defined above */ },
  typography: { /* defined above */ },
  shadows: { card: '0 1px 3px rgba(0,0,0,0.12)' },
  borderRadius: { sm: 4, md: 8, lg: 12 }
}
```

## Next Steps & Future Enhancements

### Immediate Next Phase (Post-MVP)
1. **Advanced Filtering Panel** - More granular controls
2. **Watchlist Functionality** - Save favorite opportunities  
3. **Historical EV Trends** - Charts and analytics
4. **Custom Alerts Setup** - User-defined thresholds

### Future Enhancement Opportunities
1. **Dark Mode Support** - Theme switching
2. **Personalization** - AI-driven recommendations
3. **Social Features** - Community EV discussions
4. **Mobile App** - Native iOS/Android applications

---

## Design Validation Checklist

- [ ] Mobile-first responsive design ✓
- [ ] Clear information hierarchy ✓  
- [ ] Minimal cognitive load ✓
- [ ] Immediate value recognition ✓
- [ ] Accessible design patterns ✓
- [ ] Performance-optimized approach ✓
- [ ] Scalable component architecture ✓
- [ ] Search & Results component design ✓
- [ ] Detailed Event View design ✓
- [ ] Recommended Odds Component design ✓

---

*This design documentation will be updated as we iterate on the dashboard based on user feedback and performance metrics.* 