"""
Odds conversion utilities for the betting intelligence platform
Converts between different odds formats and calculates implied probabilities
"""

from typing import Union
import logging

logger = logging.getLogger(__name__)


class OddsConversionError(Exception):
    """Custom exception for odds conversion errors"""
    pass


def american_to_implied_probability(odds: Union[int, float]) -> float:
    """
    Convert American odds to implied probability.
    
    American odds format:
    - Positive odds (e.g., +150): Represent how much profit you make on a $100 bet
    - Negative odds (e.g., -150): Represent how much you need to bet to make $100 profit
    
    Formula:
    - For positive odds: probability = 100 / (odds + 100)
    - For negative odds: probability = |odds| / (|odds| + 100)
    
    Args:
        odds: American odds (positive or negative number)
        
    Returns:
        float: Implied probability as a decimal (0.0 to 1.0)
        
    Raises:
        OddsConversionError: If odds are invalid (zero or non-numeric)
        
    Examples:
        >>> american_to_implied_probability(150)   # +150 odds
        0.4
        >>> american_to_implied_probability(-150)  # -150 odds  
        0.6
        >>> american_to_implied_probability(100)   # +100 odds (even money)
        0.5
        >>> american_to_implied_probability(-100)  # -100 odds (even money)
        0.5
    """
    # Validate input
    if not isinstance(odds, (int, float)):
        raise OddsConversionError(f"Odds must be a number, got {type(odds)}")
    
    if odds == 0:
        raise OddsConversionError("Odds cannot be zero")
    
    try:
        if odds > 0:
            # Positive American odds: +150 means $100 bet wins $150
            # Implied probability = 100 / (odds + 100)
            probability = 100 / (odds + 100)
        else:
            # Negative American odds: -150 means $150 bet wins $100
            # Implied probability = |odds| / (|odds| + 100)
            abs_odds = abs(odds)
            probability = abs_odds / (abs_odds + 100)
        
        return probability
    
    except ZeroDivisionError:
        raise OddsConversionError(f"Invalid odds calculation for odds: {odds}")
    except Exception as e:
        raise OddsConversionError(f"Failed to convert odds {odds}: {str(e)}")


def implied_probability_to_american(probability: float) -> float:
    """
    Convert implied probability to American odds.
    
    Args:
        probability: Implied probability as a decimal (0.0 to 1.0)
        
    Returns:
        float: American odds (positive or negative)
        
    Raises:
        OddsConversionError: If probability is invalid (not between 0 and 1)
        
    Examples:
        >>> implied_probability_to_american(0.4)   # 40% probability
        150.0
        >>> implied_probability_to_american(0.6)   # 60% probability  
        -150.0
        >>> implied_probability_to_american(0.5)   # 50% probability (even money)
        100.0
    """
    # Validate input
    if not isinstance(probability, (int, float)):
        raise OddsConversionError(f"Probability must be a number, got {type(probability)}")
    
    if probability <= 0 or probability >= 1:
        raise OddsConversionError(f"Probability must be between 0 and 1, got {probability}")
    
    try:
        if probability == 0.5:
            # Even money can be represented as +100
            return 100.0
        elif probability < 0.5:
            # Underdog (positive odds)
            # odds = (100 / probability) - 100
            odds = (100 / probability) - 100
            return odds
        else:
            # Favorite (negative odds)  
            # odds = -(100 / (1 - probability)) + 100
            odds = -((100 / (1 - probability)) - 100)
            return odds
    
    except ZeroDivisionError:
        raise OddsConversionError(f"Invalid probability calculation for probability: {probability}")
    except Exception as e:
        raise OddsConversionError(f"Failed to convert probability {probability}: {str(e)}")


def calculate_expected_value(probability: float, odds: Union[int, float], bet_amount: float = 100.0) -> float:
    """
    Calculate expected value of a bet given true probability and offered odds.
    
    Expected Value = (probability × potential_profit) - ((1 - probability) × bet_amount)
    
    Args:
        probability: True probability of the outcome (0.0 to 1.0)
        odds: American odds offered by bookmaker
        bet_amount: Amount to bet (default $100)
        
    Returns:
        float: Expected value in dollars
        
    Examples:
        >>> calculate_expected_value(0.55, 120, 100)  # 55% chance, +120 odds, $100 bet
        21.0
        >>> calculate_expected_value(0.45, -110, 100)  # 45% chance, -110 odds, $100 bet
        -9.090909090909092
    """
    if not isinstance(probability, (int, float)) or probability <= 0 or probability >= 1:
        raise OddsConversionError(f"Probability must be between 0 and 1, got {probability}")
    
    if bet_amount <= 0:
        raise OddsConversionError(f"Bet amount must be positive, got {bet_amount}")
    
    # Calculate potential profit based on American odds
    if odds > 0:
        # Positive odds: profit = bet_amount * (odds / 100)
        potential_profit = bet_amount * (odds / 100)
    else:
        # Negative odds: profit = bet_amount * (100 / |odds|)
        potential_profit = bet_amount * (100 / abs(odds))
    
    # Expected Value = (win_probability × profit) - (lose_probability × loss)
    expected_value = (probability * potential_profit) - ((1 - probability) * bet_amount)
    
    return expected_value


def calculate_fair_odds(probability: float) -> float:
    """
    Calculate fair American odds based on true probability (no vig/juice).
    
    Args:
        probability: True probability of outcome (0.0 to 1.0)
        
    Returns:
        float: Fair American odds
        
    Examples:
        >>> calculate_fair_odds(0.6)   # 60% probability
        -150.0
        >>> calculate_fair_odds(0.4)   # 40% probability  
        150.0
    """
    return implied_probability_to_american(probability)


def detect_positive_ev_opportunity(true_probability: float, offered_odds: Union[int, float]) -> dict:
    """
    Detect if a betting opportunity has positive expected value.
    
    Args:
        true_probability: Estimated true probability of outcome
        offered_odds: Odds offered by bookmaker
        
    Returns:
        dict: Analysis containing EV, fair odds, and opportunity status
        
    Examples:
        >>> detect_positive_ev_opportunity(0.55, 120)
        {
            'has_positive_ev': True,
            'expected_value': 21.0,
            'fair_odds': -122.22,
            'offered_odds': 120,
            'edge_percentage': 0.1263
        }
    """
    try:
        # Calculate expected value for $100 bet
        ev = calculate_expected_value(true_probability, offered_odds, 100.0)
        
        # Calculate fair odds based on true probability
        fair_odds = calculate_fair_odds(true_probability)
        
        # Calculate implied probability of offered odds
        offered_probability = american_to_implied_probability(offered_odds)
        
        # Calculate edge (difference between true and implied probability)
        edge_percentage = true_probability - offered_probability
        
        return {
            'has_positive_ev': ev > 0,
            'expected_value': ev,
            'fair_odds': fair_odds,
            'offered_odds': offered_odds,
            'true_probability': true_probability,
            'implied_probability': offered_probability,
            'edge_percentage': edge_percentage,
            'ev_per_dollar': ev / 100.0  # EV per $1 bet
        }
    
    except Exception as e:
        logger.error(f"Error detecting opportunity: {e}")
        return {
            'has_positive_ev': False,
            'error': str(e)
        }


if __name__ == "__main__":
    # Example usage and testing
    print("=== Odds Conversion Examples ===")
    
    # Test American odds to implied probability
    test_odds = [150, -150, 100, -100, 200, -200, 110, -110]
    
    print("\nAmerican Odds → Implied Probability:")
    for odds in test_odds:
        try:
            prob = american_to_implied_probability(odds)
            print(f"{odds:4d} → {prob:.4f} ({prob*100:.2f}%)")
        except Exception as e:
            print(f"{odds:4d} → Error: {e}")
    
    # Test opportunity detection
    print("\n=== Opportunity Detection Examples ===")
    scenarios = [
        (0.55, 120),   # Good bet: 55% chance at +120 odds
        (0.45, -110),  # Bad bet: 45% chance at -110 odds  
        (0.6, -140),   # Marginal: 60% chance at -140 odds
    ]
    
    for true_prob, odds in scenarios:
        result = detect_positive_ev_opportunity(true_prob, odds)
        print(f"True prob: {true_prob:.0%}, Odds: {odds:+d}")
        print(f"  EV: ${result.get('expected_value', 0):.2f}")
        print(f"  Positive EV: {result.get('has_positive_ev', False)}")
        print(f"  Edge: {result.get('edge_percentage', 0):.2%}")
        print() 