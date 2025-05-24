"""
Odds conversion utilities for the betting intelligence platform
Converts between different odds formats and calculates implied probabilities
"""

from typing import Union, Tuple, Dict
from sqlalchemy.orm import Session
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


def remove_vig_two_sided(odds_a: Union[int, float], odds_b: Union[int, float]) -> Dict[str, float]:
    """
    Remove vig (vigorish) from a two-sided market to calculate fair odds.
    
    The vig is the sportsbook's built-in profit margin. In a fair market, the implied 
    probabilities of all outcomes should sum to exactly 1.0 (100%). However, sportsbooks 
    set odds so the probabilities sum to more than 1.0, creating their profit margin.
    
    This function:
    1. Converts both odds to implied probabilities
    2. Calculates the total probability (should be > 1.0 due to vig)
    3. Normalizes probabilities to sum to 1.0 (removes vig)
    4. Converts fair probabilities back to American odds
    
    Args:
        odds_a: American odds for outcome A (e.g., favorite)
        odds_b: American odds for outcome B (e.g., underdog)
        
    Returns:
        dict: Contains fair odds, probabilities, and vig information
        {
            'fair_odds_a': float,          # Fair American odds for outcome A
            'fair_odds_b': float,          # Fair American odds for outcome B
            'fair_probability_a': float,   # Fair probability for outcome A
            'fair_probability_b': float,   # Fair probability for outcome B
            'original_probability_a': float, # Original implied probability A
            'original_probability_b': float, # Original implied probability B
            'vig_percentage': float,       # Vig as a percentage (e.g., 0.05 = 5%)
            'total_implied_probability': float  # Sum of original probabilities
        }
        
    Raises:
        OddsConversionError: If odds are invalid or probabilities don't make sense
        
    Examples:
        >>> remove_vig_two_sided(-110, -110)  # Standard -110 both sides
        {
            'fair_odds_a': 100.0,
            'fair_odds_b': 100.0,
            'fair_probability_a': 0.5,
            'fair_probability_b': 0.5,
            'vig_percentage': 0.0476,  # ~4.76% vig
            ...
        }
        
        >>> remove_vig_two_sided(-150, 120)  # Favorite vs underdog
        {
            'fair_odds_a': -136.36,
            'fair_odds_b': 136.36,
            'fair_probability_a': 0.577,
            'fair_probability_b': 0.423,
            'vig_percentage': 0.0345,  # ~3.45% vig
            ...
        }
    """
    try:
        # Convert odds to implied probabilities
        prob_a = american_to_implied_probability(odds_a)
        prob_b = american_to_implied_probability(odds_b)
        
        # Calculate total implied probability (should be > 1.0 due to vig)
        total_prob = prob_a + prob_b
        
        if total_prob <= 1.0:
            raise OddsConversionError(
                f"Total implied probability ({total_prob:.4f}) is not greater than 1.0. "
                "This suggests no vig or arbitrage opportunity exists."
            )
        
        # Calculate vig percentage
        vig_percentage = total_prob - 1.0
        
        # Remove vig by normalizing probabilities to sum to 1.0
        fair_prob_a = prob_a / total_prob
        fair_prob_b = prob_b / total_prob
        
        # Verify fair probabilities sum to 1.0 (within floating point precision)
        if abs((fair_prob_a + fair_prob_b) - 1.0) > 1e-10:
            raise OddsConversionError(
                f"Fair probabilities don't sum to 1.0: {fair_prob_a + fair_prob_b:.10f}"
            )
        
        # Convert fair probabilities back to American odds
        fair_odds_a = implied_probability_to_american(fair_prob_a)
        fair_odds_b = implied_probability_to_american(fair_prob_b)
        
        return {
            'fair_odds_a': fair_odds_a,
            'fair_odds_b': fair_odds_b,
            'fair_probability_a': fair_prob_a,
            'fair_probability_b': fair_prob_b,
            'original_probability_a': prob_a,
            'original_probability_b': prob_b,
            'vig_percentage': vig_percentage,
            'total_implied_probability': total_prob,
            'original_odds_a': odds_a,
            'original_odds_b': odds_b
        }
        
    except OddsConversionError:
        # Re-raise our custom errors
        raise
    except Exception as e:
        raise OddsConversionError(f"Failed to remove vig from odds {odds_a}, {odds_b}: {str(e)}")


def calculate_vig_percentage(odds_a: Union[int, float], odds_b: Union[int, float]) -> float:
    """
    Calculate the vig percentage from a two-sided market.
    
    Args:
        odds_a: American odds for outcome A
        odds_b: American odds for outcome B
        
    Returns:
        float: Vig percentage as decimal (e.g., 0.05 = 5% vig)
        
    Examples:
        >>> calculate_vig_percentage(-110, -110)  # Standard juice
        0.047619047619047616  # ~4.76% vig
        
        >>> calculate_vig_percentage(-105, -105)  # Lower juice
        0.02380952380952381   # ~2.38% vig
    """
    prob_a = american_to_implied_probability(odds_a)
    prob_b = american_to_implied_probability(odds_b)
    return (prob_a + prob_b) - 1.0


def find_fair_value_opportunities(market_odds: Tuple[float, float], fair_odds: Tuple[float, float],
                                  threshold: float = 0.02) -> Dict[str, any]:
    """
    Compare market odds against fair odds to identify value betting opportunities.

    NOTE: This helper is kept for reference but is no longer used after
    removing the fair odds workflow from the application.
    
    Args:
        market_odds: Tuple of (odds_a, odds_b) from sportsbook
        fair_odds: Tuple of (fair_odds_a, fair_odds_b) after vig removal
        threshold: Minimum edge required to flag as opportunity (default 2%)
        
    Returns:
        dict: Analysis of value opportunities for both sides
        
    Examples:
        >>> market_odds = (-110, -110)
        >>> fair_odds = (100, 100)  # True fair odds are even money
        >>> find_fair_value_opportunities(market_odds, fair_odds)
        {
            'opportunity_a': True,
            'opportunity_b': True,
            'edge_a': 0.0476,  # 4.76% edge on side A
            'edge_b': 0.0476,  # 4.76% edge on side B
            ...
        }
    """
    try:
        # Convert all odds to probabilities
        market_prob_a = american_to_implied_probability(market_odds[0])
        market_prob_b = american_to_implied_probability(market_odds[1])
        fair_prob_a = american_to_implied_probability(fair_odds[0])
        fair_prob_b = american_to_implied_probability(fair_odds[1])
        
        # Calculate edges (fair probability - market implied probability)
        edge_a = fair_prob_a - market_prob_a
        edge_b = fair_prob_b - market_prob_b
        
        return {
            'opportunity_a': edge_a > threshold,
            'opportunity_b': edge_b > threshold,
            'edge_a': edge_a,
            'edge_b': edge_b,
            'market_odds_a': market_odds[0],
            'market_odds_b': market_odds[1],
            'fair_odds_a': fair_odds[0],
            'fair_odds_b': fair_odds[1],
            'threshold': threshold
        }
        
    except Exception as e:
        logger.error(f"Error finding fair value opportunities: {e}")
        return {'error': str(e)}


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

    NOTE: This utility is unused in the latest backend but kept for completeness.
    
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
    
    # Test vig removal
    print("=== Vig Removal Examples ===")
    vig_scenarios = [
        (-110, -110),  # Standard juice
        (-105, -105),  # Lower juice
        (-150, 120),   # Favorite vs underdog
        (-200, 170),   # Heavy favorite
    ]
    
    for odds_a, odds_b in vig_scenarios:
        result = remove_vig_two_sided(odds_a, odds_b)
        print(f"Market: {odds_a:+d} / {odds_b:+d}")
        print(f"  Fair: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")
        print(f"  Vig: {result['vig_percentage']:.2%}")
        print(f"  Total Implied Prob: {result['total_implied_probability']:.3f}")
        print()
    
