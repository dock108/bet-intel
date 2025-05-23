# Weighted Fair Odds Calculation

## Overview

The weighted fair odds calculation creates highly accurate fair odds by using a specific weighting scheme that focuses on the three most respected sportsbooks in the market. This approach provides superior fair odds compared to simple averaging or general vig removal methods.

## Weighting Strategy

### Target Sportsbooks & Weights

**Pinnacle: 50%**
- Industry leader in sharp, low-vig odds
- Serves as the primary price discovery mechanism
- Accepts high-limit bets from sharp bettors
- Typically has the lowest vig in the market

**DraftKings: 25%**
- Major US operator with competitive odds
- Large market share and liquidity
- Represents mainstream US betting market

**FanDuel: 25%**
- Major US operator with competitive odds
- Large market share and liquidity  
- Represents mainstream US betting market

### Why This Weighting?

This weighting scheme reflects the **relative importance and accuracy** of each sportsbook:

1. **Pinnacle's 50% weight** acknowledges its role as the industry's price leader
2. **DraftKings + FanDuel's 25% each** represents the major US market while preventing over-reliance on any single domestic operator
3. **No other books included** ensures the fair odds calculation uses only the most trusted and competitive sources

## Core Functions

### `calculate_weighted_fair_odds(pinnacle_odds, draftkings_odds, fanduel_odds) -> Dict`

The main function that calculates weighted fair odds from the three target sportsbooks.

**Process:**
1. Convert all available odds to implied probabilities
2. Apply the weighting scheme (50% / 25% / 25%)
3. Calculate weighted average probabilities
4. Normalize probabilities to sum to 1.0 (removes residual vig)
5. Convert back to American odds

**Parameters:**
- `pinnacle_odds`: Tuple of (odds_a, odds_b) from Pinnacle (optional)
- `draftkings_odds`: Tuple of (odds_a, odds_b) from DraftKings (optional)
- `fanduel_odds`: Tuple of (odds_a, odds_b) from FanDuel (optional)

**Returns:**
```python
{
    'fair_odds_a': float,              # Weighted fair American odds for outcome A
    'fair_odds_b': float,              # Weighted fair American odds for outcome B
    'fair_probability_a': float,       # Final fair probability for outcome A
    'fair_probability_b': float,       # Final fair probability for outcome B
    'weighted_probability_a': float,   # Weighted avg probability A (pre-normalization)
    'weighted_probability_b': float,   # Weighted avg probability B (pre-normalization)
    'books_used': List[str],           # List of books that had odds available
    'weights_applied': Dict[str, float], # Actual weights used for each book
    'total_weight': float,             # Total weight of available books
    'residual_vig': float,             # Any remaining vig after weighting
    'individual_vigs': Dict[str, float], # Vig from each individual book
    'book_count': int,                 # Number of books with available odds
    'original_odds': Dict[str, Tuple]  # Original odds from each book
}
```

**Examples:**

```python
from backend.odds_converter import calculate_weighted_fair_odds

# All three books available (ideal scenario)
result = calculate_weighted_fair_odds(
    pinnacle_odds=(-105, -105),    # 2.44% vig
    draftkings_odds=(-110, -110),  # 4.76% vig
    fanduel_odds=(-108, -108)      # 3.57% vig
)
print(f"Fair odds: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")
print(f"Books used: {result['books_used']}")
print(f"Final weights: {result['weights_applied']}")
# Output: Fair odds +100.0 / +100.0, all three books with standard weights

# Only Pinnacle and DraftKings available
result = calculate_weighted_fair_odds(
    pinnacle_odds=(-102, -102),
    draftkings_odds=(-112, -112)
)
print(f"Fair odds: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")
print(f"Normalized weights: {result['weights_applied']}")
# Output: Pinnacle 66.67%, DraftKings 33.33% (normalized from 50%/25%)

# Only Pinnacle available (fallback scenario)
result = calculate_weighted_fair_odds(
    pinnacle_odds=(-103, -103)
)
print(f"Fair odds: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")
print(f"Weight: {result['weights_applied']}")
# Output: 100% Pinnacle weight
```

### Weight Normalization Logic

When not all three sportsbooks have odds available, the weights are **automatically normalized**:

**All Available (Standard):**
- Pinnacle: 50% 
- DraftKings: 25%
- FanDuel: 25%

**Pinnacle + DraftKings Only:**
- Pinnacle: 66.67% (50% ÷ 75% total)
- DraftKings: 33.33% (25% ÷ 75% total)

**Pinnacle + FanDuel Only:**
- Pinnacle: 66.67% (50% ÷ 75% total)
- FanDuel: 33.33% (25% ÷ 75% total)

**DraftKings + FanDuel Only:**
- DraftKings: 50% (25% ÷ 50% total)
- FanDuel: 50% (25% ÷ 50% total)

**Single Book Available:**
- That book: 100%

### `calculate_weighted_fair_odds_from_db(db, event_external_id, market_key) -> Dict`

Database integration function that retrieves odds from the database and calculates weighted fair odds.

**Parameters:**
- `db`: SQLAlchemy database session
- `event_external_id`: External ID of the event to analyze
- `market_key`: Market type (default 'h2h' for moneyline)

**Returns:**
Same structure as `calculate_weighted_fair_odds()` plus database metadata

**Example:**
```python
from backend.database import SessionLocal
from backend.odds_converter import calculate_weighted_fair_odds_from_db

with SessionLocal() as db:
    result = calculate_weighted_fair_odds_from_db(
        db=db, 
        event_external_id="12345", 
        market_key="h2h"
    )
    print(f"Fair odds from DB: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")
    print(f"Event: {result['event_info']['home_team']} vs {result['event_info']['away_team']}")
    print(f"Books used: {result['books_used']}")
```

### `find_weighted_fair_value_opportunities(market_odds_dict, threshold) -> Dict`

Compare multiple sportsbooks against the weighted fair odds to identify value opportunities.

**Parameters:**
- `market_odds_dict`: Dictionary with bookmaker odds `{'pinnacle': (odds_a, odds_b), 'caesars': (odds_a, odds_b), ...}`
- `threshold`: Minimum edge required to flag as opportunity (default 2%)

**Returns:**
```python
{
    'fair_odds_calculation': Dict,        # Full weighted fair odds calculation
    'opportunities_by_book': Dict,        # Value analysis for each book
    'fair_odds': Tuple[float, float],     # Final fair odds tuple
    'threshold_used': float,              # Threshold applied
    'books_in_fair_calc': List[str],      # Books used in fair odds calc (Pinnacle/DK/FD only)
    'books_analyzed': List[str]           # All books analyzed for value
}
```

**Example:**
```python
from backend.odds_converter import find_weighted_fair_value_opportunities

# Market odds from multiple sportsbooks
market_odds = {
    'pinnacle': (-105, -105),      # Used in fair odds calculation
    'draftkings': (-110, -110),    # Used in fair odds calculation  
    'fanduel': (-108, -108),       # Used in fair odds calculation
    'caesars': (-115, -115),       # Analyzed against fair odds
    'betmgm': (-112, -112),        # Analyzed against fair odds
    'pointsbet': (-109, -109)      # Analyzed against fair odds
}

opportunities = find_weighted_fair_value_opportunities(market_odds, threshold=0.015)

# Fair odds calculated using only Pinnacle, DraftKings, FanDuel
print(f"Fair odds: {opportunities['fair_odds']}")
print(f"Books in fair calc: {opportunities['books_in_fair_calc']}")

# Value opportunities found across all books
for book, opportunity in opportunities['opportunities_by_book'].items():
    if opportunity.get('opportunity_a') or opportunity.get('opportunity_b'):
        print(f"{book}: Side A edge {opportunity['edge_a']:.2%}, Side B edge {opportunity['edge_b']:.2%}")
```

## Mathematical Foundation

### Weighted Average Calculation

Given odds from available sportsbooks, the weighted fair odds calculation:

1. **Convert to probabilities:**
   ```
   P_pinnacle_a = implied_probability(pinnacle_odds_a)
   P_draftkings_a = implied_probability(draftkings_odds_a) 
   P_fanduel_a = implied_probability(fanduel_odds_a)
   ```

2. **Apply weights (normalize if books missing):**
   ```
   total_weight = sum(weights for available books)
   normalized_weight_pinnacle = 0.50 / total_weight
   normalized_weight_draftkings = 0.25 / total_weight
   normalized_weight_fanduel = 0.25 / total_weight
   ```

3. **Calculate weighted averages:**
   ```
   weighted_prob_a = (P_pinnacle_a × w_pinnacle) + 
                     (P_draftkings_a × w_draftkings) + 
                     (P_fanduel_a × w_fanduel)
   ```

4. **Normalize to remove residual vig:**
   ```
   total_weighted_prob = weighted_prob_a + weighted_prob_b
   fair_prob_a = weighted_prob_a / total_weighted_prob
   fair_prob_b = weighted_prob_b / total_weighted_prob
   ```

5. **Convert to American odds:**
   ```
   fair_odds_a = probability_to_american(fair_prob_a)
   fair_odds_b = probability_to_american(fair_prob_b)
   ```

### Example Calculation

**Scenario:** All three books available with different odds:
- Pinnacle: -105 / -105 (2.44% vig)
- DraftKings: -110 / -110 (4.76% vig)  
- FanDuel: -108 / -108 (3.57% vig)

**Step 1: Convert to probabilities**
- Pinnacle A: 0.5122, B: 0.5122 (total: 1.0244)
- DraftKings A: 0.5238, B: 0.5238 (total: 1.0476)
- FanDuel A: 0.5189, B: 0.5189 (total: 1.0378)

**Step 2: Apply weights** 
- Pinnacle: 50%, DraftKings: 25%, FanDuel: 25%

**Step 3: Calculate weighted averages**
- Weighted A: (0.5122 × 0.50) + (0.5238 × 0.25) + (0.5189 × 0.25) = 0.5168
- Weighted B: (0.5122 × 0.50) + (0.5238 × 0.25) + (0.5189 × 0.25) = 0.5168
- Total: 1.0337 (3.37% residual vig)

**Step 4: Normalize**
- Fair A: 0.5168 ÷ 1.0337 = 0.5000
- Fair B: 0.5168 ÷ 1.0337 = 0.5000

**Step 5: Convert to odds**
- Fair odds: +100 / +100

## Integration with Existing System

### Enhanced Opportunity Detection Pipeline

```python
from backend.odds_converter import calculate_weighted_fair_odds_from_db
from backend.database import SessionLocal

def enhanced_opportunity_detection_weighted(event_external_id: str):
    """
    Enhanced opportunity detection using weighted fair odds from Pinnacle/DK/FD.
    """
    with SessionLocal() as db:
        # Calculate weighted fair odds from database
        fair_result = calculate_weighted_fair_odds_from_db(
            db=db,
            event_external_id=event_external_id,
            market_key='h2h'
        )
        
        if fair_result['book_count'] == 0:
            return {'error': 'No odds available from target sportsbooks'}
        
        # Get all bookmaker odds for comparison
        all_bookmaker_odds = get_all_bookmaker_odds(db, event_external_id)
        
        # Find opportunities across all books using weighted fair odds
        opportunities = find_weighted_fair_value_opportunities(
            all_bookmaker_odds,
            threshold=0.02
        )
        
        return {
            'event_id': event_external_id,
            'fair_odds_source': fair_result['books_used'],
            'fair_odds': (fair_result['fair_odds_a'], fair_result['fair_odds_b']),
            'opportunities': opportunities,
            'methodology': 'weighted_pinnacle_dk_fd'
        }
```

### API Integration

Add endpoints to expose weighted fair odds:

```python
# In main.py
@app.get("/api/events/{event_id}/weighted-fair-odds")
async def get_weighted_fair_odds(event_id: str, db: Session = Depends(get_db)):
    """Get weighted fair odds for a specific event using Pinnacle/DK/FD."""
    try:
        result = calculate_weighted_fair_odds_from_db(db, event_id)
        return result
    except OddsConversionError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/events/{event_id}/weighted-opportunities")
async def get_weighted_opportunities(event_id: str, threshold: float = 0.02, db: Session = Depends(get_db)):
    """Find value opportunities using weighted fair odds."""
    try:
        opportunities = enhanced_opportunity_detection_weighted(event_id)
        return opportunities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Advantages Over Simple Methods

### vs. Simple Averaging
- **Weighted approach** gives more importance to Pinnacle's sharp lines
- **Selective books** uses only the most trusted sources
- **Quality over quantity** focuses on accuracy rather than including all books

### vs. General Vig Removal  
- **Curated sources** uses only premier sportsbooks
- **Market expertise** leverages Pinnacle's price discovery role
- **US market representation** includes major domestic operators

### vs. Single-Book Reference
- **Diversification** reduces reliance on any single source
- **Market consensus** incorporates multiple perspectives
- **Availability resilience** works even if one book is missing

## Error Handling

The weighted fair odds functions include comprehensive error handling:

```python
from backend.odds_converter import calculate_weighted_fair_odds, OddsConversionError

try:
    # No odds provided
    result = calculate_weighted_fair_odds()
except OddsConversionError as e:
    print(f"Error: {e}")  # "No valid odds provided from Pinnacle, DraftKings, or FanDuel"

try:
    # Invalid odds format
    result = calculate_weighted_fair_odds(pinnacle_odds=(0, -110))
except OddsConversionError as e:
    print(f"Error: {e}")  # "Odds cannot be zero"

# Graceful handling of missing books
result = calculate_weighted_fair_odds(
    pinnacle_odds=(-105, -105),
    # draftkings_odds missing
    # fanduel_odds missing  
)
# Works with just Pinnacle (100% weight)
```

## Testing the Implementation

Run the test script to verify functionality:

```bash
cd backend
python test_weighted_fair_odds.py
```

This displays:
- All three books scenario with standard weights
- Two books scenario with normalized weights  
- Single book fallback scenario
- Verification of weight calculations and residual vig

## Usage Best Practices

### 1. Prioritize Data Quality
```python
# Always check which books were actually used
result = calculate_weighted_fair_odds(pinnacle_odds, draftkings_odds, fanduel_odds)
if result['book_count'] < 2:
    print(f"Warning: Only {result['book_count']} book(s) available: {result['books_used']}")
```

### 2. Monitor Vig Levels
```python
# Check individual book vigs for anomalies
for book, vig in result['individual_vigs'].items():
    if vig > 0.06:  # > 6% vig
        print(f"Warning: High vig from {book}: {vig:.2%}")
```

### 3. Validate Results
```python
# Ensure fair probabilities sum to 1.0
total_prob = result['fair_probability_a'] + result['fair_probability_b']
assert abs(total_prob - 1.0) < 1e-10, f"Fair probabilities don't sum to 1.0: {total_prob}"
```

This weighted fair odds system provides the most accurate and reliable fair odds calculation available, specifically tailored to use the industry's most trusted and competitive sportsbooks. 