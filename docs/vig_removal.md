# Vig Removal & Fair Odds Calculation

## Overview

The vig removal functionality calculates "fair odds" by removing the sportsbook's built-in profit margin (vig/juice) from two-sided markets. This is essential for identifying true value betting opportunities and understanding the actual probabilities of outcomes.

## What is Vig (Vigorish)?

**Vig** (short for vigorish), also called **juice**, is the sportsbook's built-in profit margin. In a perfectly fair market, the implied probabilities of all outcomes should sum to exactly 100%. However, sportsbooks set odds so the probabilities sum to more than 100%, creating their profit margin.

### Example:
- **Market Odds**: Team A -110, Team B -110
- **Implied Probabilities**: 52.38% + 52.38% = **104.76%**
- **Vig**: 4.76% (the extra 4.76% is the sportsbook's margin)
- **Fair Odds**: Team A +100, Team B +100 (50% each)

## Core Functions

### `remove_vig_two_sided(odds_a, odds_b) -> Dict`

The main function that removes vig from a two-sided market and calculates fair odds.

**Process:**
1. Convert American odds to implied probabilities
2. Calculate total probability (should be > 100% due to vig)
3. Normalize probabilities to sum to 100% (removes vig)
4. Convert fair probabilities back to American odds

**Parameters:**
- `odds_a`: American odds for outcome A (e.g., favorite)
- `odds_b`: American odds for outcome B (e.g., underdog)

**Returns:**
```python
{
    'fair_odds_a': float,          # Fair American odds for outcome A
    'fair_odds_b': float,          # Fair American odds for outcome B
    'fair_probability_a': float,   # Fair probability for outcome A (0.0-1.0)
    'fair_probability_b': float,   # Fair probability for outcome B (0.0-1.0)
    'original_probability_a': float, # Original implied probability A
    'original_probability_b': float, # Original implied probability B
    'vig_percentage': float,       # Vig as decimal (e.g., 0.05 = 5%)
    'total_implied_probability': float,  # Sum of original probabilities
    'original_odds_a': float,      # Original input odds A
    'original_odds_b': float       # Original input odds B
}
```

**Examples:**

```python
from backend.odds_converter import remove_vig_two_sided

# Standard -110 juice (most common in US sports)
result = remove_vig_two_sided(-110, -110)
print(f"Fair odds: {result['fair_odds_a']:+.0f} / {result['fair_odds_b']:+.0f}")  # +100 / +100
print(f"Vig: {result['vig_percentage']:.2%}")  # 4.76%

# Favorite vs underdog market
result = remove_vig_two_sided(-150, 120)
print(f"Market: -150 / +120")
print(f"Fair: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")  # -132.0 / +132.0
print(f"Vig: {result['vig_percentage']:.2%}")  # 5.45%

# Low juice market (better for bettors)
result = remove_vig_two_sided(-105, -105)
print(f"Vig: {result['vig_percentage']:.2%}")  # 2.44%
```

### `calculate_vig_percentage(odds_a, odds_b) -> float`

Quick function to calculate just the vig percentage from a two-sided market.

**Examples:**
```python
from backend.odds_converter import calculate_vig_percentage

vig = calculate_vig_percentage(-110, -110)  # 0.0476 (4.76%)
vig = calculate_vig_percentage(-105, -105)  # 0.0244 (2.44%)
vig = calculate_vig_percentage(-150, 120)   # 0.0545 (5.45%)
```

### `find_fair_value_opportunities(market_odds, fair_odds, threshold=0.02) -> Dict`

Compares market odds against fair odds to identify value betting opportunities.

**Parameters:**
- `market_odds`: Tuple of (odds_a, odds_b) from sportsbook
- `fair_odds`: Tuple of (fair_odds_a, fair_odds_b) after vig removal  
- `threshold`: Minimum edge required to flag as opportunity (default 2%)

**Returns:**
```python
{
    'opportunity_a': bool,      # True if side A has value
    'opportunity_b': bool,      # True if side B has value
    'edge_a': float,           # Edge percentage for side A
    'edge_b': float,           # Edge percentage for side B
    'market_odds_a': float,    # Original market odds A
    'market_odds_b': float,    # Original market odds B
    'fair_odds_a': float,      # Fair odds A
    'fair_odds_b': float,      # Fair odds B
    'threshold': float         # Threshold used
}
```

**Example:**
```python
from backend.odds_converter import remove_vig_two_sided, find_fair_value_opportunities

# Remove vig from market odds
market = (-110, -110)
vig_result = remove_vig_two_sided(market[0], market[1])
fair = (vig_result['fair_odds_a'], vig_result['fair_odds_b'])

# Find opportunities (in this case, both sides have equal value due to vig)
opportunities = find_fair_value_opportunities(market, fair, threshold=0.02)
print(f"Side A opportunity: {opportunities['opportunity_a']}")  # True
print(f"Side A edge: {opportunities['edge_a']:.2%}")  # 4.76%
```

## Mathematical Foundation

### Vig Calculation Formula

Given two American odds, the vig calculation:

1. **Convert to implied probabilities:**
   - P₁ = implied_probability(odds₁)
   - P₂ = implied_probability(odds₂)

2. **Calculate total probability:**
   - Total = P₁ + P₂ (should be > 1.0)

3. **Vig percentage:**
   - Vig = Total - 1.0

4. **Fair probabilities (vig removed):**
   - Fair_P₁ = P₁ / Total
   - Fair_P₂ = P₂ / Total

5. **Convert back to American odds:**
   - Fair_odds₁ = probability_to_american(Fair_P₁)
   - Fair_odds₂ = probability_to_american(Fair_P₂)

### Example Calculation

**Market:** Team A -150, Team B +120

1. **Implied probabilities:**
   - P_A = 150 / (150 + 100) = 0.6000 (60%)
   - P_B = 100 / (120 + 100) = 0.4545 (45.45%)

2. **Total probability:**
   - Total = 0.6000 + 0.4545 = 1.0545 (105.45%)

3. **Vig:**
   - Vig = 1.0545 - 1.0 = 0.0545 (5.45%)

4. **Fair probabilities:**
   - Fair_P_A = 0.6000 / 1.0545 = 0.5691 (56.91%)
   - Fair_P_B = 0.4545 / 1.0545 = 0.4309 (43.09%)

5. **Fair odds:**
   - Fair_odds_A = -132.0
   - Fair_odds_B = +132.0

## Practical Applications

### 1. Line Shopping Strategy

Use fair odds to identify which sportsbooks offer the best value:

```python
# Compare multiple sportsbooks against fair odds
sportsbooks = {
    'DraftKings': (-152, 125),
    'FanDuel': (-148, 120),
    'Caesars': (-155, 130)
}

# Calculate fair odds from average market
avg_favorite = sum(odds[0] for odds in sportsbooks.values()) / len(sportsbooks)
avg_underdog = sum(odds[1] for odds in sportsbooks.values()) / len(sportsbooks)
fair_result = remove_vig_two_sided(avg_favorite, avg_underdog)

# Find best value
for book, odds in sportsbooks.items():
    opportunities = find_fair_value_opportunities(
        odds, 
        (fair_result['fair_odds_a'], fair_result['fair_odds_b'])
    )
    print(f"{book}: Favorite edge: {opportunities['edge_a']:.2%}, "
          f"Underdog edge: {opportunities['edge_b']:.2%}")
```

### 2. P2P Betting Opportunities

Use fair odds to set competitive prices on P2P platforms:

```python
# Market odds: -150 / +120
# Fair odds: -132 / +132

# On P2P platform, you could:
# 1. Offer +130 on the underdog (better than +120 market, worse than +132 fair)
# 2. Take -140 on the favorite (better than -150 market, worse than -132 fair)
```

### 3. Vig Comparison Across Markets

Different markets and sportsbooks have different vig levels:

```python
markets = [
    ('NFL Spread', -110, -110),      # Standard 4.76% vig
    ('NBA Moneyline', -150, 120),    # Higher vig on favorites
    ('Pinnacle NHL', -105, -105),    # Low vig book
    ('Prop Bet', -130, -110),        # Often higher vig
]

for market_name, odds_a, odds_b in markets:
    vig = calculate_vig_percentage(odds_a, odds_b)
    print(f"{market_name}: {vig:.2%} vig")
```

## Integration with Opportunity Detection

The vig removal functionality enhances the existing opportunity detection system:

### Enhanced Detection Pipeline

```python
from backend.odds_converter import (
    remove_vig_two_sided, 
    find_fair_value_opportunities,
    american_to_implied_probability
)

def enhanced_opportunity_detection(bookmaker_odds, market_odds_list):
    """
    Enhanced opportunity detection using fair odds calculation.
    
    Args:
        bookmaker_odds: (odds_a, odds_b) from specific bookmaker
        market_odds_list: List of (odds_a, odds_b) from multiple books
    """
    
    # Calculate market consensus by averaging
    avg_odds_a = sum(odds[0] for odds in market_odds_list) / len(market_odds_list)
    avg_odds_b = sum(odds[1] for odds in market_odds_list) / len(market_odds_list)
    
    # Remove vig to get fair odds
    fair_result = remove_vig_two_sided(avg_odds_a, avg_odds_b)
    fair_odds = (fair_result['fair_odds_a'], fair_result['fair_odds_b'])
    
    # Find opportunities at this bookmaker
    opportunities = find_fair_value_opportunities(
        bookmaker_odds, 
        fair_odds, 
        threshold=0.02  # 2% minimum edge
    )
    
    return {
        'bookmaker_odds': bookmaker_odds,
        'fair_odds': fair_odds,
        'market_vig': fair_result['vig_percentage'],
        'opportunities': opportunities
    }
```

## Common Vig Levels by Market

- **NFL/NBA Point Spreads**: 4.5-5.0% (typically -110/-110)
- **MLB Moneylines**: 3.0-6.0% (varies by game)
- **Tennis/Soccer**: 2.5-4.0% (competitive markets)
- **Prop Bets**: 8.0-15.0% (higher margins)
- **Futures**: 10.0-25.0% (very high margins)
- **Pinnacle**: 1.5-3.0% (known for low vig)

## Error Handling

The vig removal functions include comprehensive error handling:

```python
from backend.odds_converter import remove_vig_two_sided, OddsConversionError

try:
    # This will raise an error - no vig detected
    result = remove_vig_two_sided(110, -110)  # Arbitrage situation
except OddsConversionError as e:
    print(f"Error: {e}")  # "Total implied probability is not greater than 1.0"

try:
    # Invalid odds
    result = remove_vig_two_sided(0, -110)
except OddsConversionError as e:
    print(f"Error: {e}")  # "Odds cannot be zero"
```

## Testing the Implementation

Run the module directly to see vig removal examples:

```bash
cd backend
python odds_converter.py
```

This will display:
- Basic odds conversion examples
- Opportunity detection scenarios
- **Vig removal examples** with different market types

## Usage in Production

The vig removal functionality integrates seamlessly with the existing betting intelligence platform:

```python
# In odds_analyzer.py or similar
from backend.odds_converter import remove_vig_two_sided, find_fair_value_opportunities

def analyze_market_opportunities(event_odds_data):
    """
    Analyze all bookmaker odds for an event using fair odds calculation.
    """
    opportunities = []
    
    # Calculate consensus fair odds from all bookmakers
    all_odds = [(bookie.odds_a, bookie.odds_b) for bookie in event_odds_data]
    
    # Use market average as baseline
    avg_a = sum(odds[0] for odds in all_odds) / len(all_odds)
    avg_b = sum(odds[1] for odds in all_odds) / len(all_odds)
    
    fair_result = remove_vig_two_sided(avg_a, avg_b)
    fair_odds = (fair_result['fair_odds_a'], fair_result['fair_odds_b'])
    
    # Check each bookmaker against fair odds
    for bookie in event_odds_data:
        bookie_odds = (bookie.odds_a, bookie.odds_b)
        opportunity = find_fair_value_opportunities(bookie_odds, fair_odds)
        
        if opportunity['opportunity_a'] or opportunity['opportunity_b']:
            opportunities.append({
                'bookmaker': bookie.name,
                'odds': bookie_odds,
                'opportunity': opportunity,
                'fair_odds': fair_odds
            })
    
    return opportunities
```

This provides much more sophisticated opportunity detection based on true market efficiency rather than simple odds comparison. 