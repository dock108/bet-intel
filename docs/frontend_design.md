# Frontend Design Documentation

## MVP Dashboard Design Overview

**Last Updated:** May 23, 2025  
**Version:** 1.0  
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

---

*This design documentation will be updated as we iterate on the dashboard based on user feedback and performance metrics.* 