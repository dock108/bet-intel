# Frontend Design Documentation

## MVP Dashboard Design Overview

**Last Updated:** May 23, 2025  
**Version:** 1.1  
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

## Data Flow & API Integration

### Primary API Endpoints Used
1. **`GET /api/ev-opportunities`** - Main dashboard data
2. **`GET /api/events`** - Upcoming events list
3. **`GET /api/stats`** - Quick stats bar data

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

---

*This design documentation will be updated as we iterate on the dashboard based on user feedback and performance metrics.* 