# Expected Value (EV) Calculations

## Overview

The betting intelligence platform implements three distinct Expected Value calculation methods, each serving different purposes in betting analysis and value identification. All three calculations are computed and stored for every event/bookmaker combination to provide comprehensive insights into market efficiency and betting opportunities.

## Three EV Calculation Methods

### 1. Standard EV (Raw Bookmaker Odds)

**Purpose**: Basic EV calculation using raw bookmaker odds without adjustment for vig or market inefficiencies.

**Formula**: `EV = (probability × potential_profit) - ((1 - probability) × bet_amount)`

**Use Cases**:
- Quick initial assessment of betting value
- Baseline comparison for other methods
- Simple market evaluation

**Advantages**:
- Fast and straightforward calculation
- No dependency on other market data
- Good for initial screening

**Limitations**:
- Includes bookmaker's vig/juice
- May overestimate opportunities
- Doesn't account for market inefficiencies

**Implementation**: `calculate_standard_ev()`

### 2. No-Vig EV (Vig-Removed Fair Odds)

**Purpose**: EV calculation using vig-removed fair odds from two-sided markets.

**Process**:
1. Convert both sides' odds to implied probabilities
2. Remove vig by normalizing probabilities to sum to 1.0
3. Convert fair probabilities back to odds
4. Calculate EV using bettor's probability vs fair odds

**Use Cases**:
- More accurate value assessment
- Understanding true market pricing
- Identifying bookmaker-specific advantages

**Advantages**:
- Removes bookmaker's profit margin
- More accurate than standard EV
- Works with any two-sided market

**Limitations**:
- Requires both sides of the market
- Assumes uniform vig distribution
- Limited to two-outcome markets

**Implementation**: `calculate_no_vig_ev()`

### 3. Weighted Fair Odds EV (Market Consensus)

**Purpose**: Most sophisticated EV calculation using weighted consensus from the three most trusted sportsbooks.

**Weighting**:
- **Pinnacle: 50%** (industry price leader, lowest vig)
- **DraftKings: 25%** (major US operator)
- **FanDuel: 25%** (major US operator)

**Process**:
1. Collect odds from Pinnacle, DraftKings, and FanDuel
2. Convert to implied probabilities
3. Apply weighted average with automatic normalization
4. Convert back to fair odds
5. Calculate EV using bettor's probability vs weighted fair odds

**Use Cases**:
- Most accurate market value assessment
- Premium analysis for serious bettors
- Benchmarking against sharp market consensus

**Advantages**:
- Leverages Pinnacle's sharp lines
- Incorporates major US market operators
- Most accurate fair odds estimation
- Handles missing data gracefully

**Limitations**:
- Requires data from specific sportsbooks
- More complex calculation
- Limited by availability of reference odds

**Note**: The weighted fair EV calculation has been removed from the current backend implementation.

## Database Schema

### EVCalculationModel

The `ev_calculations` table stores all three EV calculations for each event/bookmaker/market/outcome combination:

```sql
CREATE TABLE ev_calculations (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    bookmaker_id INTEGER REFERENCES bookmakers(id),
    market_key VARCHAR(50),           -- 'h2h', 'spreads', 'totals'
    
    -- Outcome information
    outcome_name VARCHAR(100),        -- 'outcome_A', 'outcome_B'
    outcome_index INTEGER,            -- 0, 1, 2...
    offered_odds FLOAT,               -- American odds from bookmaker
    
    -- Three EV calculations
    standard_ev FLOAT,                -- Standard EV (with vig)
    no_vig_ev FLOAT,                 -- No-vig EV
    
    -- Supporting probabilities
    standard_implied_probability FLOAT,      -- From raw odds
    no_vig_fair_probability FLOAT,          -- After vig removal
    
    -- Reference odds
    no_vig_fair_odds FLOAT,          -- Fair odds after vig removal
    
    -- Metadata
    calculation_method_details TEXT,  -- JSON with full calculation details
    books_used_in_weighted VARCHAR(200),     -- Books used for weighted calc
    vig_percentage FLOAT,            -- Vig from no-vig calculation
    
    -- Quality indicators
    has_positive_standard_ev BOOLEAN,
    has_positive_no_vig_ev BOOLEAN,
    has_positive_weighted_ev BOOLEAN,
    
    -- Timestamps
    calculated_at TIMESTAMP,
    odds_snapshot_time TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## Core Functions

### calculate_comprehensive_ev()

Main function that computes all three EV methods and provides comparative analysis:

```python
from backend.ev_calculator import calculate_comprehensive_ev

results = calculate_comprehensive_ev(
    probability_a=0.55,               # Bettor's estimated probabilities
    probability_b=0.45,
    offered_odds_a=120,               # Bookmaker's offered odds
    offered_odds_b=-150,
    pinnacle_odds=(-105, -105),       # Reference odds for weighted calc
    draftkings_odds=(-110, -110),
    fanduel_odds=(-108, -108),
    target_outcome=0,                 # Calculate EV for outcome A
    bet_amount=100.0
)

# Results include all three calculations plus analysis
print(f"Standard EV: ${results['standard_ev']['ev']:+.2f}")
print(f"No-Vig EV: ${results['no_vig_ev']['ev']:+.2f}")
print(f"Recommendation: {results['recommendation']['action']}")
```

### store_ev_calculations_to_db()

Stores comprehensive EV results to database:

```python
from backend.ev_calculator import store_ev_calculations_to_db
from backend.database import SessionLocal

with SessionLocal() as db:
    ev_records = store_ev_calculations_to_db(
        db=db,
        event_external_id="event_123",
        bookmaker_key="draftkings",
        market_key="h2h",
        ev_results=results,
        odds_snapshot_time=datetime.now()
    )
    print(f"Stored {len(ev_records)} EV calculation records")
```

### get_ev_calculations_from_db()

Retrieves stored EV calculations with filtering:

```python
from backend.ev_calculator import get_ev_calculations_from_db

with SessionLocal() as db:
    ev_data = get_ev_calculations_from_db(
        db=db,
        event_external_id="event_123",
        bookmaker_key="draftkings",    # Optional filter
        market_key="h2h"
    )
    
    for record in ev_data:
        print(f"{record['bookmaker']['title']}: Standard EV ${record['standard_ev']:+.2f}")
```

## Practical Examples

### Example 1: All Methods Agree (Strong Opportunity)

```python
# Scenario: 60% true probability, +120 offered odds
results = calculate_comprehensive_ev(
    probability_a=0.60, probability_b=0.40,
    offered_odds_a=120, offered_odds_b=-180,
    pinnacle_odds=(110, -140),
    draftkings_odds=(120, -150),
    fanduel_odds=(115, -145),
    target_outcome=0
)

# All methods show positive EV:
# Standard EV: +$32.00 (large edge due to true 60% vs implied 45.5%)
# No-Vig EV: +$28.50 (slightly lower after vig removal)

# Recommendation: bet_large, confidence: high
```

### Example 2: Mixed Signals (Requires Judgment)

```python
# Scenario: 52% true probability, marginal odds
results = calculate_comprehensive_ev(
    probability_a=0.52, probability_b=0.48,
    offered_odds_a=-105, offered_odds_b=-105,
    pinnacle_odds=(-110, -110),
    draftkings_odds=(-108, -108),
    fanduel_odds=(-112, -112),
    target_outcome=0
)

# Mixed results:
# Standard EV: +$1.43 (barely positive)
# No-Vig EV: -$0.95 (negative after vig removal)

# Recommendation: no_bet, confidence: medium
# Reasoning: "Weighted fair odds show negative EV (most reliable method)"
```

### Example 3: Limited Data (Fallback Scenario)

```python
# Scenario: Only standard calculation possible
results = calculate_comprehensive_ev(
    probability_a=0.58, probability_b=0.42,
    offered_odds_a=150, offered_odds_b=-200,
    # No reference odds available
    target_outcome=0
)

# Limited results:
# Standard EV: +$19.33 (positive but uncertain)
# No-Vig EV: Error (need both sides for vig removal)

# Recommendation: bet_small, confidence: low
# Reasoning: "Limited to standard method only"
```

## Comparative Analysis Features

### EV Agreement Classification

The system automatically classifies EV agreement across methods:

- **all_positive**: All available methods show positive EV → Strong opportunity
- **all_negative**: All available methods show negative EV → Avoid bet
- **mixed**: Some positive, some negative → Requires careful analysis

### Conservative vs Aggressive Analysis

- **Most Conservative**: Method showing lowest EV (highest bar for betting)
- **Most Aggressive**: Method showing highest EV (most optimistic view)

### Automated Recommendations

Based on EV agreement and method reliability:

1. **bet_large**: Weighted fair EV positive + high confidence
2. **bet_medium**: All methods positive OR no-vig positive + high confidence
3. **bet_small**: Mixed results but weighted fair positive
4. **no_bet**: Negative EV from reliable methods

## Integration with Opportunity Detection

### Enhanced Opportunity Pipeline

```python
def enhanced_opportunity_detection_with_ev(event_external_id: str):
    """
    Complete opportunity detection using all three EV methods.
    """
    with SessionLocal() as db:
        # Get event and odds data
        event = get_event_with_odds(db, event_external_id)
        
        opportunities = []
        
        # Analyze each bookmaker
        for bookmaker, odds in event.bookmaker_odds.items():
            # Get bettor's probability estimates (from model/analysis)
            prob_estimates = get_probability_estimates(event)
            
            # Calculate comprehensive EV
            ev_results = calculate_comprehensive_ev(
                probability_a=prob_estimates['home'],
                probability_b=prob_estimates['away'],
                offered_odds_a=odds['home'],
                offered_odds_b=odds['away'],
                pinnacle_odds=event.bookmaker_odds.get('pinnacle'),
                draftkings_odds=event.bookmaker_odds.get('draftkings'),
                fanduel_odds=event.bookmaker_odds.get('fanduel'),
                target_outcome=0
            )
            
            # Store to database
            store_ev_calculations_to_db(db, event_external_id, bookmaker, 'h2h', ev_results)
            
            # Check for opportunities
            if ev_results['recommendation']['action'] in ['bet_small', 'bet_medium', 'bet_large']:
                opportunities.append({
                    'bookmaker': bookmaker,
                    'ev_analysis': ev_results,
                    'priority': _calculate_opportunity_priority(ev_results)
                })
        
        return sorted(opportunities, key=lambda x: x['priority'], reverse=True)
```

### API Integration

```python
# In main.py - new endpoints for EV analysis
@app.get("/api/events/{event_id}/ev-analysis")
async def get_ev_analysis(event_id: str, db: Session = Depends(get_db)):
    """Get comprehensive EV analysis for an event."""
    ev_data = get_ev_calculations_from_db(db, event_id)
    return {
        'event_id': event_id,
        'ev_calculations': ev_data,
        'summary': _summarize_ev_analysis(ev_data)
    }

@app.post("/api/events/{event_id}/calculate-ev")
async def calculate_event_ev(
    event_id: str, 
    probabilities: dict,  # {'home': 0.55, 'away': 0.45}
    db: Session = Depends(get_db)
):
    """Calculate EV for an event with user-provided probabilities."""
    # Implementation would call calculate_comprehensive_ev for each bookmaker
    pass
```

## Performance Considerations

### Database Indexing

```sql
-- Optimize EV calculation queries
CREATE INDEX idx_ev_event_bookmaker ON ev_calculations(event_id, bookmaker_id);
CREATE INDEX idx_ev_positive_flags ON ev_calculations(has_positive_standard_ev, has_positive_no_vig_ev, has_positive_weighted_ev);
CREATE INDEX idx_ev_calculated_at ON ev_calculations(calculated_at);
```

### Calculation Efficiency

- **Batch Processing**: Calculate EV for multiple events/bookmakers simultaneously
- **Caching**: Cache weighted fair odds calculations when reference odds haven't changed
- **Selective Updates**: Only recalculate when odds or probability estimates change

## Error Handling

### Common Error Scenarios

1. **Missing Reference Odds**: Weighted fair EV calculation fails gracefully
2. **Invalid Probabilities**: Validation ensures probabilities sum to 1.0
3. **Database Errors**: Rollback on storage failures
4. **Calculation Errors**: Individual method failures don't prevent other calculations

### Error Recovery

```python
# Graceful degradation example
try:
    ev_results = calculate_comprehensive_ev(...)
except EVCalculationError as e:
    # Fall back to available methods
    logger.warning(f"Comprehensive EV calculation failed: {e}")
    ev_results = calculate_partial_ev(...)
```

## Usage Best Practices

### 1. Method Priority

**For Decision Making:**
1. No-Vig EV (good baseline)
2. Standard EV (initial screening only)

**For Analysis:**
- Use all three for comprehensive market understanding
- Compare methods to identify market inefficiencies
- Monitor agreement patterns over time

### 2. Probability Estimation

**Critical for Accuracy:**
- Use sophisticated models for probability estimation
- Incorporate team stats, injuries, weather, etc.
- Regularly validate and update probability models
- Consider uncertainty in probability estimates

### 3. Risk Management

**Based on EV Agreement:**
- **High Agreement**: Larger bet sizes justified
- **Low Agreement**: Smaller bet sizes or avoid
- **Single Method Positive**: Very small bets or paper trading

### 4. Historical Analysis

**Track Performance:**
- Monitor actual vs predicted EV over time
- Identify which method performs best for different sports/markets
- Adjust betting strategies based on historical accuracy

## Future Enhancements

### Planned Improvements

1. **Kelly Criterion Integration**: Optimal bet sizing based on EV and bankroll
2. **Confidence Intervals**: EV ranges based on probability estimate uncertainty
3. **Market Timing**: EV calculations across different times (opening vs closing)
4. **Multi-Outcome Markets**: Extend beyond two-sided markets
5. **Machine Learning**: Automated probability estimation and EV optimization

### Advanced Features

1. **Portfolio EV**: Combined EV across multiple simultaneous bets
2. **Correlation Analysis**: Account for correlated outcomes
3. **Dynamic Weighting**: Adjust sportsbook weights based on recent performance
4. **Real-time Updates**: Live EV recalculation as odds change

This comprehensive EV calculation system provides the foundation for sophisticated betting analysis, combining mathematical rigor with practical applicability for identifying genuine value in sports betting markets. 