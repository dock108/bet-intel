# Frontend-Backend API Integration Documentation

## Overview

**Last Updated:** May 23, 2025  
**Version:** 1.0  
**Integration Type:** REST API with JSON responses  
**Refresh Strategy:** Real-time polling every 3 minutes

This document outlines the complete integration between the Bet Intel frontend wireframes and the FastAPI backend, enabling live odds data, EV calculations, and P2P recommendations display.

## API Base Configuration

### Base URL Configuration
```javascript
const API_CONFIG = {
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://api.betintel.com' 
    : 'http://localhost:8000',
  timeout: 10000,
  retryAttempts: 3,
  refreshInterval: 180000 // 3 minutes in milliseconds
};
```

### Authentication Headers
```javascript
const getHeaders = () => ({
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'User-Agent': 'BetIntel-Frontend/1.0',
  // Future: 'Authorization': `Bearer ${getAuthToken()}`
});
```

## Core API Endpoints

### 1. EV Opportunities Endpoint

**Endpoint:** `GET /api/ev-opportunities`  
**Purpose:** Retrieve dashboard data with live EV calculations  
**Refresh Rate:** Every 3 minutes  

#### Request Parameters
```typescript
interface EVOpportunitiesParams {
  sport_key?: string;           // Filter by sport (e.g., 'basketball_nba')
  bookmaker_keys?: string[];    // Filter by bookmakers
  min_ev_threshold?: number;    // Minimum EV value (default: 0)
  time_range?: 'today' | 'tomorrow' | 'week';
  sort_by?: 'ev_standard' | 'ev_no_vig' | 'commence_time';
  limit?: number;               // Number of results (default: 50)
  offset?: number;              // Pagination offset (default: 0)
}
```

#### Response Structure
```typescript
interface EVOpportunitiesResponse {
  opportunities: EVOpportunity[];
  total_count: number;
  last_updated: string;        // ISO timestamp
  next_refresh: string;        // ISO timestamp
  summary_stats: {
    total_opportunities: number;
    best_ev_value: number;
    next_game_time: string;
    active_bookmakers: number;
  };
}

interface EVOpportunity {
  id: string;
  event: {
    id: string;
    sport_key: string;
    sport_title: string;
    commence_time: string;
    home_team: string;
    away_team: string;
  };
  market: {
    type: 'h2h' | 'spreads' | 'totals';
    description: string;
    outcome: string;
  };
  bookmaker: {
    key: string;
    title: string;
    last_update: string;
  };
  odds: {
    current: number;           // American format
    opening?: number;
  };
  ev_calculations: {
    standard: number;          // Raw EV calculation
    no_vig: number;           // Vig-removed EV
    confidence_score: number; // 0-100
  };
  probabilities: {
    implied: number;          // From current odds
    fair_calculated: number;  // Our calculated fair probability
    edge_percentage: number;  // Percentage edge
  };
  kelly_criterion: {
    percentage: number;       // Suggested bet percentage
    suggested_stake: number;  // Dollar amount (based on $2000 bankroll)
  };
}
```

#### Frontend Implementation
```javascript
class EVDataService {
  constructor() {
    this.baseURL = API_CONFIG.baseURL;
    this.refreshTimer = null;
    this.cache = new Map();
  }

  async fetchEVOpportunities(params = {}) {
    const url = new URL(`${this.baseURL}/api/ev-opportunities`);
    
    // Add query parameters
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (Array.isArray(value)) {
          value.forEach(v => url.searchParams.append(key, v));
        } else {
          url.searchParams.append(key, value.toString());
        }
      }
    });

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: getHeaders(),
        signal: AbortSignal.timeout(API_CONFIG.timeout)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      this.updateCache('ev-opportunities', data, params);
      return data;
    } catch (error) {
      console.error('Failed to fetch EV opportunities:', error);
      return this.getCachedData('ev-opportunities', params);
    }
  }
}
```

### 2. Event Details Endpoint

**Endpoint:** `GET /api/events/{event_id}/analysis`  
**Purpose:** Detailed analysis for specific event  
**Refresh Rate:** Every 3 minutes when viewed  

#### Response Structure
```typescript
interface EventAnalysisResponse {
  event: EventDetails;
  opportunities: EVOpportunity[];
  odds_comparison: OddsComparison[];
  ev_explanation: EVExplanation;
  p2p_recommendations?: P2PRecommendation[];
  market_analysis: MarketAnalysis;
}

interface EventDetails {
  id: string;
  sport_key: string;
  sport_title: string;
  commence_time: string;
  home_team: string;
  away_team: string;
  venue?: string;
  time_until_commence: number; // seconds
}

interface OddsComparison {
  market_type: string;
  outcomes: {
    [outcome: string]: {
      pinnacle?: number;
      draftkings?: number;
      fanduel?: number;
      best_ev: number;
      best_bookmaker: string;
    };
  };
}

interface EVExplanation {
  primary_opportunity: {
    outcome: string;
    bookmaker: string;
    current_odds: number;
    fair_odds_calculated: number;
    edge_explanation: string;
  };
  market_inefficiency: {
    description: string;
    factors: string[];
  };
  sharp_money_indicators: {
    pinnacle_line: number;
    line_movement: {
      from: number;
      to: number;
      direction: 'up' | 'down';
    };
    public_betting_percentage: number;
  };
  fair_value_calculation: {
    weighted_model_probability: number;
    vig_removed_probability: number;
    historical_probability: number;
    consensus_probability: number;
  };
}
```

### 3. P2P Recommendations Endpoint

**Endpoint:** `GET /api/p2p/recommendations/{event_id}`  
**Purpose:** P2P platform odds recommendations  
**Refresh Rate:** Every 5 minutes  

#### Response Structure
```typescript
interface P2PRecommendationsResponse {
  event_id: string;
  recommendations: P2PRecommendation[];
  last_updated: string;
  market_conditions: {
    liquidity_score: number;    // 0-100
    volatility: 'low' | 'medium' | 'high';
    time_sensitivity: number;   // hours until event
  };
}

interface P2PRecommendation {
  platform: 'novig' | 'sporttrade' | 'prophetx';
  platform_info: {
    name: string;
    logo_url: string;
    deep_link: string;
  };
  recommended_odds: number;
  expected_fill_time: {
    min_minutes: number;
    max_minutes: number;
    confidence: 'low' | 'medium' | 'high';
  };
  potential_profit: number;     // Based on $100 stake
  liquidity_score: number;      // Platform-specific 0-100
  historical_fill_rate: number; // Percentage
  risk_assessment: {
    fill_probability: number;
    time_risk: 'low' | 'medium' | 'high';
    liquidity_risk: 'low' | 'medium' | 'high';
  };
}
```

### 4. Quick Stats Endpoint

**Endpoint:** `GET /api/stats`  
**Purpose:** Dashboard summary statistics  
**Refresh Rate:** Every 3 minutes  

#### Response Structure
```typescript
interface QuickStatsResponse {
  total_opportunities: number;
  best_ev_value: number;
  best_ev_event: {
    teams: string;
    sport: string;
    commence_time: string;
  };
  next_game: {
    teams: string;
    sport: string;
    commence_time: string;
    time_until: number; // seconds
  };
  active_bookmakers: string[];
  market_efficiency: {
    score: number;        // 0-100, lower = more opportunities
    trend: 'improving' | 'declining' | 'stable';
  };
  data_freshness: {
    last_odds_update: string;
    next_scheduled_update: string;
    update_frequency: number; // seconds
  };
}
```

## Real-Time Data Management

### Refresh Strategy Implementation

```javascript
class RealTimeDataManager {
  constructor() {
    this.refreshInterval = API_CONFIG.refreshInterval;
    this.activeRefreshers = new Map();
    this.isVisible = true;
    this.setupVisibilityHandling();
  }

  startAutoRefresh(dataType, fetchFunction, params = {}) {
    // Stop existing refresher if any
    this.stopAutoRefresh(dataType);

    // Immediate fetch
    fetchFunction(params);

    // Setup interval
    const intervalId = setInterval(() => {
      if (this.isVisible) {
        fetchFunction(params);
      }
    }, this.refreshInterval);

    this.activeRefreshers.set(dataType, intervalId);
  }

  stopAutoRefresh(dataType) {
    const intervalId = this.activeRefreshers.get(dataType);
    if (intervalId) {
      clearInterval(intervalId);
      this.activeRefreshers.delete(dataType);
    }
  }

  setupVisibilityHandling() {
    document.addEventListener('visibilitychange', () => {
      this.isVisible = !document.hidden;
      
      if (this.isVisible) {
        // Refresh all active data when tab becomes visible
        this.refreshAllActiveData();
      }
    });
  }

  refreshAllActiveData() {
    // Implementation would trigger refresh for all active refreshers
    this.activeRefreshers.forEach((intervalId, dataType) => {
      // Trigger immediate refresh
      this.triggerRefresh(dataType);
    });
  }
}
```

### WebSocket Future Enhancement

```javascript
class WebSocketManager {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    try {
      this.ws = new WebSocket(`${API_CONFIG.wsBaseURL}/ws/odds-updates`);
      
      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleRealtimeUpdate(data);
      };

      this.ws.onclose = () => {
        this.handleReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      console.error('Failed to establish WebSocket connection:', error);
      this.handleReconnect();
    }
  }

  handleRealtimeUpdate(data) {
    switch (data.type) {
      case 'odds_update':
        this.updateOddsDisplay(data.payload);
        break;
      case 'ev_recalculation':
        this.updateEVDisplay(data.payload);
        break;
      case 'new_opportunity':
        this.addNewOpportunity(data.payload);
        break;
    }
  }
}
```

## Error Handling & Loading States

### Error Handling Strategy

```javascript
class APIErrorHandler {
  static handle(error, context = 'API Request') {
    const errorInfo = {
      timestamp: new Date().toISOString(),
      context,
      error: error.message,
      stack: error.stack
    };

    // Log error
    console.error(`${context} failed:`, errorInfo);

    // Determine error type and appropriate user message
    let userMessage = 'Something went wrong. Please try again.';
    let shouldRetry = false;

    if (error.name === 'TimeoutError') {
      userMessage = 'Request timed out. Please check your connection.';
      shouldRetry = true;
    } else if (error.message.includes('NetworkError')) {
      userMessage = 'Network error. Please check your internet connection.';
      shouldRetry = true;
    } else if (error.message.includes('500')) {
      userMessage = 'Server error. Our team has been notified.';
      shouldRetry = true;
    } else if (error.message.includes('404')) {
      userMessage = 'Data not found. It may have been removed or updated.';
      shouldRetry = false;
    }

    // Show user-friendly error
    this.showErrorToUser(userMessage, shouldRetry);

    // Track error for analytics
    this.trackError(errorInfo);

    return { handled: true, shouldRetry, userMessage };
  }

  static showErrorToUser(message, canRetry = false) {
    // Create error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg shadow-lg z-50';
    errorDiv.innerHTML = `
      <div class="flex items-center">
        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
        </svg>
        <span>${message}</span>
        <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-red-500 hover:text-red-700">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
        </button>
      </div>
    `;

    document.body.appendChild(errorDiv);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (errorDiv.parentElement) {
        errorDiv.remove();
      }
    }, 5000);
  }
}
```

### Loading States Management

```javascript
class LoadingStateManager {
  static show(containerId, type = 'card') {
    const container = document.getElementById(containerId);
    if (!container) return;

    const loadingHTML = this.getLoadingTemplate(type);
    container.innerHTML = loadingHTML;
    container.classList.add('loading');
  }

  static hide(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.classList.remove('loading');
  }

  static getLoadingTemplate(type) {
    switch (type) {
      case 'card':
        return `
          <div class="animate-pulse">
            <div class="bg-gray-200 rounded-lg h-32 mb-4"></div>
            <div class="space-y-2">
              <div class="bg-gray-200 rounded h-4 w-3/4"></div>
              <div class="bg-gray-200 rounded h-4 w-1/2"></div>
            </div>
          </div>
        `;
      case 'table':
        return `
          <div class="animate-pulse">
            ${Array(5).fill().map(() => `
              <div class="flex space-x-4 py-3 border-b border-gray-200">
                <div class="bg-gray-200 rounded h-4 w-1/4"></div>
                <div class="bg-gray-200 rounded h-4 w-1/4"></div>
                <div class="bg-gray-200 rounded h-4 w-1/4"></div>
                <div class="bg-gray-200 rounded h-4 w-1/4"></div>
              </div>
            `).join('')}
          </div>
        `;
      case 'stats':
        return `
          <div class="animate-pulse grid grid-cols-2 md:grid-cols-4 gap-4">
            ${Array(4).fill().map(() => `
              <div class="text-center p-3 bg-gray-50 rounded-lg">
                <div class="bg-gray-200 rounded h-6 w-16 mx-auto mb-2"></div>
                <div class="bg-gray-200 rounded h-3 w-12 mx-auto"></div>
              </div>
            `).join('')}
          </div>
        `;
      default:
        return `
          <div class="flex items-center justify-center p-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span class="ml-3 text-gray-600">Loading...</span>
          </div>
        `;
    }
  }
}
```

## Data Transformation & Display

### EV Opportunity Card Rendering

```javascript
class EVCardRenderer {
  static renderOpportunityCard(opportunity) {
    const {
      event,
      market,
      bookmaker,
      odds,
      ev_calculations,
      probabilities,
      kelly_criterion
    } = opportunity;

    return `
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden card-hover" 
           data-opportunity-id="${opportunity.id}">
        <!-- Sport & Confidence Badge -->
        <div class="flex items-center justify-between p-4 pb-2">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 text-sm font-bold mr-3">
              ${this.getSportIcon(event.sport_key)}
            </div>
            <span class="text-sm font-medium text-gray-600">${event.sport_title}</span>
          </div>
          <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${this.getConfidenceBadgeClasses(ev_calculations.confidence_score)}">
            ${this.getConfidenceLabel(ev_calculations.confidence_score)}
          </span>
        </div>

        <!-- Event Info -->
        <div class="px-4 pb-3">
          <h3 class="text-lg font-semibold text-gray-900 mb-1">
            ${event.away_team} @ ${event.home_team}
          </h3>
          <p class="text-sm text-gray-600">
            ${this.formatDateTime(event.commence_time)} • ${market.description}
          </p>
        </div>

        <!-- Bookmaker & Odds -->
        <div class="px-4 pb-3">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-gray-600">📊 ${bookmaker.title}</span>
            <span class="text-lg font-mono font-semibold text-gray-900">
              ${this.formatOdds(odds.current)}
            </span>
          </div>
          <div class="text-sm text-blue-600 font-medium">${market.outcome}</div>
        </div>

        <!-- EV Calculations -->
        <div class="bg-green-50 border-t border-green-200 p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-green-800">Expected Value</span>
            <span class="text-xl font-bold text-green-600">
              ${this.formatCurrency(ev_calculations.no_vig)}
            </span>
          </div>
          <div class="grid grid-cols-3 gap-2 text-xs text-green-700">
            <div>
              <div>Standard: ${this.formatCurrency(ev_calculations.standard)}</div>
            </div>
            <div>
              <div>No-Vig: ${this.formatCurrency(ev_calculations.no_vig)}</div>
            </div>
          </div>
        </div>

        <!-- Kelly Criterion -->
        <div class="px-4 py-3 bg-gray-50 border-t border-gray-200">
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-600">Suggested Stake:</span>
            <span class="font-medium text-gray-900">
              ${this.formatCurrency(kelly_criterion.suggested_stake)} 
              <span class="text-gray-500">(${kelly_criterion.percentage.toFixed(1)}%)</span>
            </span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="p-4 pt-2">
          <div class="grid grid-cols-2 gap-3">
            <button onclick="viewEventDetails('${event.id}')" 
                    class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium text-sm">
              View Details
            </button>
            <button onclick="addToWatchlist('${opportunity.id}')" 
                    class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition font-medium text-sm">
              📍 Watch
            </button>
          </div>
        </div>
      </div>
    `;
  }

  static getSportIcon(sportKey) {
    const icons = {
      'basketball_nba': '🏀',
      'americanfootball_nfl': '🏈',
      'baseball_mlb': '⚾',
      'icehockey_nhl': '🏒',
      'soccer_epl': '⚽'
    };
    return icons[sportKey] || '🏆';
  }

  static getConfidenceBadgeClasses(score) {
    if (score >= 80) return 'bg-green-100 text-green-800';
    if (score >= 60) return 'bg-yellow-100 text-yellow-800';
    return 'bg-gray-100 text-gray-800';
  }

  static getConfidenceLabel(score) {
    if (score >= 80) return '🔥 HIGH';
    if (score >= 60) return '📈 MEDIUM';
    return '✅ LOW';
  }

  static formatOdds(odds) {
    return odds > 0 ? `+${odds}` : odds.toString();
  }

  static formatCurrency(amount) {
    const sign = amount >= 0 ? '+' : '';
    return `${sign}$${Math.abs(amount).toFixed(2)}`;
  }

  static formatDateTime(isoString) {
    const date = new Date(isoString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const timeString = date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });

    if (date.toDateString() === today.toDateString()) {
      return `Today, ${timeString}`;
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return `Tomorrow, ${timeString}`;
    } else {
      return `${date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      })}, ${timeString}`;
    }
  }
}
```

## Performance Optimization

### Data Caching Strategy

```javascript
class DataCache {
  constructor(maxAge = 180000) { // 3 minutes default
    this.cache = new Map();
    this.maxAge = maxAge;
  }

  set(key, data, customTTL = null) {
    const ttl = customTTL || this.maxAge;
    const expiry = Date.now() + ttl;
    
    this.cache.set(key, {
      data,
      expiry,
      accessed: Date.now()
    });
  }

  get(key) {
    const cached = this.cache.get(key);
    
    if (!cached) return null;

    if (Date.now() > cached.expiry) {
      this.cache.delete(key);
      return null;
    }

    // Update access time
    cached.accessed = Date.now();
    return cached.data;
  }

  clear() {
    this.cache.clear();
  }

  cleanup() {
    const now = Date.now();
    for (const [key, cached] of this.cache.entries()) {
      if (now > cached.expiry) {
        this.cache.delete(key);
      }
    }
  }
}
```

### Batch Request Optimization

```javascript
class BatchRequestManager {
  constructor() {
    this.pendingRequests = new Map();
    this.batchDelay = 100; // ms
  }

  async batchRequest(endpoint, params) {
    const key = `${endpoint}-${JSON.stringify(params)}`;
    
    // If request already pending, return existing promise
    if (this.pendingRequests.has(key)) {
      return this.pendingRequests.get(key);
    }

    // Create new request promise
    const requestPromise = new Promise((resolve, reject) => {
      setTimeout(async () => {
        try {
          const result = await this.executeRequest(endpoint, params);
          resolve(result);
        } catch (error) {
          reject(error);
        } finally {
          this.pendingRequests.delete(key);
        }
      }, this.batchDelay);
    });

    this.pendingRequests.set(key, requestPromise);
    return requestPromise;
  }
}
```

## Integration Testing

### API Integration Tests

```javascript
describe('API Integration Tests', () => {
  test('EV Opportunities endpoint returns valid data', async () => {
    const data = await evDataService.fetchEVOpportunities();
    
    expect(data).toHaveProperty('opportunities');
    expect(data).toHaveProperty('total_count');
    expect(data).toHaveProperty('last_updated');
    expect(Array.isArray(data.opportunities)).toBe(true);
    
    if (data.opportunities.length > 0) {
      const opportunity = data.opportunities[0];
      expect(opportunity).toHaveProperty('event');
      expect(opportunity).toHaveProperty('ev_calculations');
    }
  });

  test('Event details endpoint returns complete analysis', async () => {
    const data = await evDataService.fetchEventAnalysis('test-event-id');
    
    expect(data).toHaveProperty('event');
    expect(data).toHaveProperty('opportunities');
    expect(data).toHaveProperty('ev_explanation');
    expect(data.event).toHaveProperty('commence_time');
  });

  test('Error handling works correctly', async () => {
    // Mock network error
    global.fetch = jest.fn().mockRejectedValue(new Error('Network error'));
    
    const result = await evDataService.fetchEVOpportunities();
    expect(result).toBeDefined(); // Should return cached data or empty state
  });
});
```

## Mobile Optimization

### Responsive Data Loading

```javascript
class MobileOptimizedDataLoader {
  constructor() {
    this.isMobile = window.innerWidth < 768;
    this.isSlowNetwork = this.detectSlowNetwork();
  }

  detectSlowNetwork() {
    if ('connection' in navigator) {
      const connection = navigator.connection;
      return connection.effectiveType === 'slow-2g' || 
             connection.effectiveType === '2g' ||
             connection.saveData;
    }
    return false;
  }

  async loadDataForMobile() {
    if (this.isMobile || this.isSlowNetwork) {
      // Load essential data first
      const quickStats = await this.loadQuickStats();
      this.renderQuickStats(quickStats);

      // Load opportunities in batches
      await this.loadOpportunitiesInBatches();
    } else {
      // Load all data normally
      await this.loadAllData();
    }
  }

  async loadOpportunitiesInBatches(batchSize = 10) {
    let offset = 0;
    let hasMore = true;

    while (hasMore) {
      const batch = await evDataService.fetchEVOpportunities({
        limit: batchSize,
        offset: offset
      });

      this.renderOpportunityBatch(batch.opportunities);
      
      hasMore = batch.opportunities.length === batchSize;
      offset += batchSize;

      // Add delay between batches to prevent overwhelming
      await this.delay(100);
    }
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

---

## Integration Checklist

- [ ] ✅ **EV Opportunities API Integration**
- [ ] ✅ **Event Details API Integration**  
- [ ] ✅ **P2P Recommendations API Integration**
- [ ] ✅ **Real-time Data Refresh (3 min intervals)**
- [ ] ✅ **Error Handling & User Feedback**
- [ ] ✅ **Loading States & Skeleton Screens**
- [ ] ✅ **Data Caching & Performance Optimization**
- [ ] ✅ **Mobile-Optimized Loading**
- [ ] ✅ **API Response Transformation**
- [ ] ✅ **Integration Testing Framework**

---

*This integration documentation provides a complete foundation for connecting the frontend wireframes with live backend data, ensuring reliable performance and excellent user experience.* 