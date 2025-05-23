# Odds Conversion Module

## Overview

The `odds_converter.py` module provides comprehensive utilities for converting between different odds formats and calculating betting probabilities and expected values. This is essential for accurate opportunity detection in the betting intelligence platform.

## Core Functions

### `american_to_implied_probability(odds: Union[int, float]) -> float`

Converts American odds to implied probability.

**American Odds Format:**
- **Positive odds** (e.g., +150): Represent how much profit you make on a $100 bet
- **Negative odds** (e.g., -150): Represent how much you need to bet to make $100 profit

**Formula:**
- For positive odds: `probability = 100 / (odds + 100)`
- For negative odds: `probability = |odds| / (|odds| + 100)`

**Examples:**
```python
from backend.odds_converter import american_to_implied_probability

# Positive odds examples
prob = american_to_implied_probability(150)   # Returns 0.4 (40%)
prob = american_to_implied_probability(200)   # Returns 0.333 (33.33%)

# Negative odds examples  
prob = american_to_implied_probability(-150)  # Returns 0.6 (60%)
prob = american_to_implied_probability(-200)  # Returns 0.667 (66.67%)

# Even money
prob = american_to_implied_probability(100)   # Returns 0.5 (50%)
prob = american_to_implied_probability(-100)  # Returns 0.5 (50%)
```

### `implied_probability_to_american(probability: float) -> float`

Converts implied probability back to American odds.

**Examples:**
```python
from backend.odds_converter import implied_probability_to_american

odds = implied_probability_to_american(0.4)   # Returns 150.0 (+150)
odds = implied_probability_to_american(0.6)   # Returns -150.0 (-150)
odds = implied_probability_to_american(0.5)   # Returns 100.0 (+100)
```

### `calculate_expected_value(probability: float, odds: Union[int, float], bet_amount: float = 100.0) -> float`

Calculates the expected value of a bet given true probability and offered odds.

**Formula:**
```
Expected Value = (probability × potential_profit) - ((1 - probability) × bet_amount)
```

**Examples:**
```python
from backend.odds_converter import calculate_expected_value

# Positive EV scenario: 55% chance at +120 odds
ev = calculate_expected_value(0.55, 120, 100)  # Returns 21.0

# Negative EV scenario: 45% chance at -110 odds  
ev = calculate_expected_value(0.45, -110, 100)  # Returns -14.09
```

### `detect_positive_ev_opportunity(true_probability: float, offered_odds: Union[int, float]) -> dict`

Comprehensive analysis of a betting opportunity to determine if it has positive expected value.

**Returns:**
```python
{
    'has_positive_ev': bool,        # True if EV > 0
    'expected_value': float,        # EV in dollars for $100 bet
    'fair_odds': float,            # Fair American odds based on true probability
    'offered_odds': float,         # Odds offered by bookmaker
    'true_probability': float,     # Your estimated true probability
    'implied_probability': float,  # Implied probability from offered odds
    'edge_percentage': float,      # Difference between true and implied probability
    'ev_per_dollar': float        # EV per $1 bet
}
```

**Example:**
```python
from backend.odds_converter import detect_positive_ev_opportunity

# Analyze a potentially good bet
result = detect_positive_ev_opportunity(0.55, 120)
print(f"Positive EV: {result['has_positive_ev']}")  # True
print(f"Expected Value: ${result['expected_value']:.2f}")  # $21.00
print(f"Edge: {result['edge_percentage']:.2%}")  # 9.55%
```

## Error Handling

The module includes a custom `OddsConversionError` exception for invalid inputs:

- **Zero odds**: Odds cannot be zero
- **Invalid probability**: Must be between 0 and 1
- **Non-numeric inputs**: All inputs must be numbers
- **Invalid bet amounts**: Must be positive

**Example:**
```python
from backend.odds_converter import american_to_implied_probability, OddsConversionError

try:
    prob = american_to_implied_probability(0)  # Will raise OddsConversionError
except OddsConversionError as e:
    print(f"Error: {e}")
```

## Integration with Opportunity Detection

This module enhances the accuracy of the opportunity detection system by:

1. **Converting odds to probabilities** for proper mathematical comparison
2. **Calculating true expected value** instead of simple odds comparison
3. **Providing edge percentage** to quantify the advantage
4. **Supporting fair odds calculation** for reference pricing

### Enhanced Opportunity Detection Logic

Instead of simple American odds comparison, the system can now:

```python
# Old approach (simplified)
if bookmaker_odds > reference_odds * (1 + threshold):
    # Opportunity detected

# New approach (probability-based)
implied_prob = american_to_implied_probability(bookmaker_odds)
reference_prob = american_to_implied_probability(reference_odds)
edge = reference_prob - implied_prob

if edge > threshold:
    ev_analysis = detect_positive_ev_opportunity(reference_prob, bookmaker_odds)
    # More accurate opportunity with EV calculation
```

## Mathematical Background

### American Odds to Probability Conversion

The conversion formulas are based on the definition of American odds:

**Positive odds (+X):**
- Represents profit on $100 bet
- If you bet $100 on +150 odds, you win $150 profit (total return $250)
- Implied probability = $100 / ($100 + $150) = 100 / 250 = 0.4

**Negative odds (-X):**
- Represents amount needed to bet to win $100 profit  
- If you bet $150 on -150 odds, you win $100 profit (total return $250)
- Implied probability = $150 / ($150 + $100) = 150 / 250 = 0.6

### Expected Value Calculation

Expected value determines the long-term profitability of a bet:

```
EV = (P_win × Profit) - (P_lose × Loss)
EV = (P_win × Profit) - ((1 - P_win) × Bet_Amount)
```

**Positive EV** means the bet is profitable long-term.
**Negative EV** means the bet loses money long-term.

## Testing

Run the module directly to see examples:

```bash
cd backend
python odds_converter.py
```

This will display conversion examples and opportunity detection scenarios to verify the functionality.

## Usage in Main Application

The odds converter integrates with the main betting intelligence system:

```python
from backend.odds_converter import american_to_implied_probability, detect_positive_ev_opportunity

# In odds_analyzer.py or similar
def enhanced_opportunity_detection(bookmaker_odds, reference_odds):
    # Convert to probabilities for accurate comparison
    bookmaker_prob = american_to_implied_probability(bookmaker_odds)
    reference_prob = american_to_implied_probability(reference_odds)
    
    # Use reference probability as "true" probability estimate
    opportunity = detect_positive_ev_opportunity(reference_prob, bookmaker_odds)
    
    return opportunity
```

This provides much more accurate and mathematically sound opportunity detection compared to simple odds comparison. 