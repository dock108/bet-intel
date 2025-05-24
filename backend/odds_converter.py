"""
Odds conversion utilities for the betting intelligence platform
Converts between different odds formats and calculates implied probabilities
"""

from typing import Union, Tuple, Dict
from sqlalchemy.orm import Session
import logging
import sys
import os

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import settings
except ImportError:
    from .config import settings

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


def calculate_weighted_fair_odds(pinnacle_odds: Tuple[float, float] = None,
                                draftkings_odds: Tuple[float, float] = None, 
                                fanduel_odds: Tuple[float, float] = None) -> Dict[str, any]:
    """
    Calculate fair odds using weighted average from Pinnacle (50%), DraftKings (25%), and FanDuel (25%).
    
    This function creates more accurate fair odds by using the three most respected sportsbooks
    with specific weighting that reflects their market influence and sharpness:
    - Pinnacle: 50% (known for lowest vig and sharpest lines)
    - DraftKings: 25% (major US operator with competitive odds)
    - FanDuel: 25% (major US operator with competitive odds)
    
    Process:
    1. Convert all available odds to implied probabilities
    2. Calculate weighted average probabilities using specified weights
    3. Normalize final probabilities to sum to 1.0 (removes any remaining vig)
    4. Convert back to American odds
    
    Args:
        pinnacle_odds: Tuple of (odds_a, odds_b) from Pinnacle (optional)
        draftkings_odds: Tuple of (odds_a, odds_b) from DraftKings (optional)
        fanduel_odds: Tuple of (odds_a, odds_b) from FanDuel (optional)
        
    Returns:
        dict: Comprehensive fair odds analysis
        {
            'fair_odds_a': float,           # Weighted fair American odds for outcome A
            'fair_odds_b': float,           # Weighted fair American odds for outcome B
            'fair_probability_a': float,    # Final fair probability for outcome A
            'fair_probability_b': float,    # Final fair probability for outcome B
            'weighted_probability_a': float, # Weighted average probability A (before normalization)
            'weighted_probability_b': float, # Weighted average probability B (before normalization)
            'books_used': List[str],        # List of books that had odds available
            'weights_applied': Dict[str, float], # Actual weights used for each book
            'total_weight': float,          # Total weight of available books
            'residual_vig': float,          # Any remaining vig after weighting
            'individual_vigs': Dict[str, float], # Vig from each individual book
            'book_count': int               # Number of books with available odds
        }
        
    Raises:
        OddsConversionError: If no odds are provided or all odds are invalid
        
    Examples:
        >>> # All three books available
        >>> result = calculate_weighted_fair_odds(
        ...     pinnacle_odds=(-105, -105),
        ...     draftkings_odds=(-110, -110),
        ...     fanduel_odds=(-108, -108)
        ... )
        >>> print(f"Fair odds: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")
        
        >>> # Only Pinnacle and DraftKings available
        >>> result = calculate_weighted_fair_odds(
        ...     pinnacle_odds=(-102, -102),
        ...     draftkings_odds=(-112, -112)
        ... )
        >>> # Will use 66.67% Pinnacle, 33.33% DraftKings (normalized weights)
    """
    
    # Define standard weights
    STANDARD_WEIGHTS = {
        'pinnacle': 0.50,
        'draftkings': 0.25,
        'fanduel': 0.25
    }
    
    available_books = {}
    individual_vigs = {}
    
    # Collect available odds and calculate individual vigs
    if pinnacle_odds is not None:
        try:
            prob_a = american_to_implied_probability(pinnacle_odds[0])
            prob_b = american_to_implied_probability(pinnacle_odds[1])
            available_books['pinnacle'] = (prob_a, prob_b)
            individual_vigs['pinnacle'] = (prob_a + prob_b) - 1.0
        except Exception as e:
            logger.warning(f"Invalid Pinnacle odds {pinnacle_odds}: {e}")
    
    if draftkings_odds is not None:
        try:
            prob_a = american_to_implied_probability(draftkings_odds[0])
            prob_b = american_to_implied_probability(draftkings_odds[1])
            available_books['draftkings'] = (prob_a, prob_b)
            individual_vigs['draftkings'] = (prob_a + prob_b) - 1.0
        except Exception as e:
            logger.warning(f"Invalid DraftKings odds {draftkings_odds}: {e}")
    
    if fanduel_odds is not None:
        try:
            prob_a = american_to_implied_probability(fanduel_odds[0])
            prob_b = american_to_implied_probability(fanduel_odds[1])
            available_books['fanduel'] = (prob_a, prob_b)
            individual_vigs['fanduel'] = (prob_a + prob_b) - 1.0
        except Exception as e:
            logger.warning(f"Invalid FanDuel odds {fanduel_odds}: {e}")
    
    # Check if we have any valid odds
    if not available_books:
        raise OddsConversionError("No valid odds provided from Pinnacle, DraftKings, or FanDuel")
    
    # Calculate normalized weights based on available books
    total_available_weight = sum(STANDARD_WEIGHTS[book] for book in available_books.keys())
    weights_applied = {
        book: STANDARD_WEIGHTS[book] / total_available_weight 
        for book in available_books.keys()
    }
    
    # Calculate weighted average probabilities
    weighted_prob_a = 0.0
    weighted_prob_b = 0.0
    
    for book, (prob_a, prob_b) in available_books.items():
        weight = weights_applied[book]
        weighted_prob_a += prob_a * weight
        weighted_prob_b += prob_b * weight
    
    # Store pre-normalization values
    pre_norm_total = weighted_prob_a + weighted_prob_b
    residual_vig = pre_norm_total - 1.0
    
    # Normalize to ensure probabilities sum to 1.0 (removes any residual vig)
    if pre_norm_total > 0:
        fair_prob_a = weighted_prob_a / pre_norm_total
        fair_prob_b = weighted_prob_b / pre_norm_total
    else:
        raise OddsConversionError("Invalid probability calculation in weighted average")
    
    # Convert fair probabilities back to American odds
    try:
        fair_odds_a = implied_probability_to_american(fair_prob_a)
        fair_odds_b = implied_probability_to_american(fair_prob_b)
    except Exception as e:
        raise OddsConversionError(f"Failed to convert fair probabilities to American odds: {e}")
    
    return {
        'fair_odds_a': fair_odds_a,
        'fair_odds_b': fair_odds_b,
        'fair_probability_a': fair_prob_a,
        'fair_probability_b': fair_prob_b,
        'weighted_probability_a': weighted_prob_a,
        'weighted_probability_b': weighted_prob_b,
        'books_used': list(available_books.keys()),
        'weights_applied': weights_applied,
        'total_weight': total_available_weight,
        'residual_vig': residual_vig,
        'individual_vigs': individual_vigs,
        'book_count': len(available_books),
        'original_odds': {
            'pinnacle': pinnacle_odds,
            'draftkings': draftkings_odds,
            'fanduel': fanduel_odds
        }
    }


def calculate_weighted_fair_odds_from_db(db: Session, event_external_id: str, market_key: str = 'h2h') -> Dict[str, any]:
    """
    Calculate weighted fair odds using database odds from Pinnacle, DraftKings, and FanDuel.
    
    This function queries the database for the latest odds from the three target sportsbooks
    and calculates fair odds using the weighted average method.
    
    Args:
        db: Database session
        event_external_id: External ID of the event to analyze
        market_key: Market type to analyze (default 'h2h' for moneyline)
        
    Returns:
        dict: Same structure as calculate_weighted_fair_odds() plus database metadata
        
    Raises:
        OddsConversionError: If event not found or no valid odds from target books
        
    Examples:
        >>> from backend.database import SessionLocal
        >>> with SessionLocal() as db:
        ...     result = calculate_weighted_fair_odds_from_db(db, "event_123", "h2h")
        ...     print(f"Fair odds from DB: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")
    """
    
    # Import here to avoid circular imports
    from backend.database import EventModel, OddsSnapshotModel, BookmakerModel
    
    # Target bookmaker keys (as they appear in database)
    TARGET_BOOKMAKERS = {
        'pinnacle': 'pinnacle',
        'draftkings': 'draftkings', 
        'fanduel': 'fanduel'
    }
    
    # Find the event
    event = db.query(EventModel).filter(EventModel.external_id == event_external_id).first()
    if not event:
        raise OddsConversionError(f"Event with external_id '{event_external_id}' not found")
    
    # Get latest odds from target bookmakers
    bookmaker_odds = {}
    
    for book_name, book_key in TARGET_BOOKMAKERS.items():
        # Find bookmaker
        bookmaker = db.query(BookmakerModel).filter(BookmakerModel.key == book_key).first()
        if not bookmaker:
            logger.warning(f"Bookmaker '{book_key}' not found in database")
            continue
        
        # Get latest odds snapshot for this bookmaker and market
        latest_snapshot = (
            db.query(OddsSnapshotModel)
            .filter(
                OddsSnapshotModel.event_id == event.id,
                OddsSnapshotModel.bookmaker_id == bookmaker.id,
                OddsSnapshotModel.market_key == market_key
            )
            .order_by(OddsSnapshotModel.last_update.desc())
            .first()
        )
        
        if latest_snapshot:
            try:
                # Parse outcomes data
                import json
                outcomes = json.loads(latest_snapshot.outcomes_data)
                
                # Extract two-sided odds (assuming first two outcomes)
                if len(outcomes) >= 2:
                    odds_a = float(outcomes[0]['price'])
                    odds_b = float(outcomes[1]['price'])
                    bookmaker_odds[book_name] = (odds_a, odds_b)
                    logger.debug(f"Found {book_name} odds: {odds_a:+.0f} / {odds_b:+.0f}")
                else:
                    logger.warning(f"Insufficient outcomes for {book_name} (found {len(outcomes)})")
                    
            except Exception as e:
                logger.error(f"Error parsing odds for {book_name}: {e}")
    
    # Calculate weighted fair odds
    result = calculate_weighted_fair_odds(
        pinnacle_odds=bookmaker_odds.get('pinnacle'),
        draftkings_odds=bookmaker_odds.get('draftkings'),
        fanduel_odds=bookmaker_odds.get('fanduel')
    )
    
    # Add database metadata
    result.update({
        'event_external_id': event_external_id,
        'market_key': market_key,
        'event_info': {
            'home_team': event.home_team,
            'away_team': event.away_team,
            'commence_time': event.commence_time,
            'sport_key': event.sport_key
        },
        'odds_timestamps': {}
    })
    
    # Add timestamp info for each book used
    for book_name in result['books_used']:
        book_key = TARGET_BOOKMAKERS[book_name]
        bookmaker = db.query(BookmakerModel).filter(BookmakerModel.key == book_key).first()
        if bookmaker:
            latest_snapshot = (
                db.query(OddsSnapshotModel)
                .filter(
                    OddsSnapshotModel.event_id == event.id,
                    OddsSnapshotModel.bookmaker_id == bookmaker.id,
                    OddsSnapshotModel.market_key == market_key
                )
                .order_by(OddsSnapshotModel.last_update.desc())
                .first()
            )
            if latest_snapshot:
                result['odds_timestamps'][book_name] = latest_snapshot.last_update
    
    return result


def find_weighted_fair_value_opportunities(market_odds_dict: Dict[str, Tuple[float, float]], 
                                         threshold: float = 0.02) -> Dict[str, any]:
    """
    Find value opportunities by comparing individual sportsbook odds against weighted fair odds.
    
    Args:
        market_odds_dict: Dictionary with bookmaker odds
                         {'pinnacle': (odds_a, odds_b), 'draftkings': (odds_a, odds_b), etc.}
        threshold: Minimum edge required to flag as opportunity (default 2%)
        
    Returns:
        dict: Analysis of value opportunities across all provided sportsbooks
        
    Examples:
        >>> market_odds = {
        ...     'pinnacle': (-105, -105),
        ...     'draftkings': (-110, -110),
        ...     'fanduel': (-108, -108),
        ...     'caesars': (-115, -115)  # Will be included in comparison but not fair calc
        ... }
        >>> opportunities = find_weighted_fair_value_opportunities(market_odds, 0.015)
    """
    
    # Extract odds for weighted fair odds calculation (only Pinnacle, DK, FD)
    pinnacle_odds = market_odds_dict.get('pinnacle')
    draftkings_odds = market_odds_dict.get('draftkings') 
    fanduel_odds = market_odds_dict.get('fanduel')
    
    try:
        # Calculate weighted fair odds using our three target books
        fair_result = calculate_weighted_fair_odds(
            pinnacle_odds=pinnacle_odds,
            draftkings_odds=draftkings_odds,
            fanduel_odds=fanduel_odds
        )
        
        fair_odds = (fair_result['fair_odds_a'], fair_result['fair_odds_b'])
        
    except OddsConversionError as e:
        return {'error': f"Could not calculate fair odds: {e}"}
    
    # Compare all provided sportsbooks against fair odds
    opportunities = {}
    
    for bookmaker, odds in market_odds_dict.items():
        if odds is None:
            continue
            
        try:
            opportunity = find_fair_value_opportunities(odds, fair_odds, threshold)
            opportunities[bookmaker] = opportunity
        except Exception as e:
            logger.error(f"Error analyzing {bookmaker} odds {odds}: {e}")
            opportunities[bookmaker] = {'error': str(e)}
    
    return {
        'fair_odds_calculation': fair_result,
        'opportunities_by_book': opportunities,
        'fair_odds': fair_odds,
        'threshold_used': threshold,
        'books_in_fair_calc': fair_result['books_used'],
        'books_analyzed': list(market_odds_dict.keys())
    }


if __name__ == "__main__":
    logging.basicConfig(level=getattr(logging, settings.log_level.upper()))

    # Example usage and testing
    logger.info("=== Odds Conversion Examples ===")
    
    # Test American odds to implied probability
    test_odds = [150, -150, 100, -100, 200, -200, 110, -110]
    
    logger.info("\nAmerican Odds → Implied Probability:")
    for odds in test_odds:
        try:
            prob = american_to_implied_probability(odds)
            logger.info(f"{odds:4d} → {prob:.4f} ({prob*100:.2f}%)")
        except Exception as e:
            logger.error(f"{odds:4d} → Error: {e}")
    
    # Test opportunity detection
    logger.info("\n=== Opportunity Detection Examples ===")
    scenarios = [
        (0.55, 120),   # Good bet: 55% chance at +120 odds
        (0.45, -110),  # Bad bet: 45% chance at -110 odds  
        (0.6, -140),   # Marginal: 60% chance at -140 odds
    ]
    
    for true_prob, odds in scenarios:
        result = detect_positive_ev_opportunity(true_prob, odds)
        logger.info(f"True prob: {true_prob:.0%}, Odds: {odds:+d}")
        logger.info(f"  EV: ${result.get('expected_value', 0):.2f}")
        logger.info(f"  Positive EV: {result.get('has_positive_ev', False)}")
        logger.info(f"  Edge: {result.get('edge_percentage', 0):.2%}")
        logger.info("")
    
    # Test vig removal
    logger.info("=== Vig Removal Examples ===")
    vig_scenarios = [
        (-110, -110),  # Standard juice
        (-105, -105),  # Lower juice
        (-150, 120),   # Favorite vs underdog
        (-200, 170),   # Heavy favorite
    ]
    
    for odds_a, odds_b in vig_scenarios:
        result = remove_vig_two_sided(odds_a, odds_b)
        logger.info(f"Market: {odds_a:+d} / {odds_b:+d}")
        logger.info(f"  Fair: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")
        logger.info(f"  Vig: {result['vig_percentage']:.2%}")
        logger.info(f"  Total Implied Prob: {result['total_implied_probability']:.3f}")
        logger.info("")
    
    # Test weighted fair odds
    logger.info("=== Weighted Fair Odds Examples ===")
    weighted_scenarios = [
        # All three books
        {
            'pinnacle_odds': (-105, -105),
            'draftkings_odds': (-110, -110),
            'fanduel_odds': (-108, -108),
            'description': 'All 3 books available'
        },
        # Only Pinnacle and DraftKings
        {
            'pinnacle_odds': (-102, -102),
            'draftkings_odds': (-112, -112),
            'fanduel_odds': None,
            'description': 'Pinnacle + DraftKings only'
        },
        # Only Pinnacle
        {
            'pinnacle_odds': (-103, -103),
            'draftkings_odds': None,
            'fanduel_odds': None,
            'description': 'Pinnacle only (fallback)'
        }
    ]
    
    for scenario in weighted_scenarios:
        result = calculate_weighted_fair_odds(
            pinnacle_odds=scenario['pinnacle_odds'],
            draftkings_odds=scenario['draftkings_odds'],
            fanduel_odds=scenario['fanduel_odds']
        )
        logger.info(f"{scenario['description']}:")
        logger.info(f"  Fair: {result['fair_odds_a']:+.1f} / {result['fair_odds_b']:+.1f}")
        logger.info(f"  Books: {result['books_used']}")
        logger.info(f"  Weights: {result['weights_applied']}")
        logger.info(f"  Residual vig: {result['residual_vig']:.3%}")
        logger.info("")
