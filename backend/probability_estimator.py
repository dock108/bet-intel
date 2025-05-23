"""
Market Consensus Probability Estimation for Betting Intelligence Platform

This module provides sophisticated probability estimation methods that use market consensus
instead of naive assumptions. The primary method uses weighted fair odds from 
Pinnacle (50%), DraftKings (25%), and FanDuel (25%) to estimate true probabilities.
"""

from typing import Dict, Tuple, Optional, List
from sqlalchemy.orm import Session
import logging
import json

from .odds_converter import (
    american_to_implied_probability,
    calculate_weighted_fair_odds,
    calculate_weighted_fair_odds_from_db,
    OddsConversionError
)
from .database import EventModel, OddsSnapshotModel, BookmakerModel

logger = logging.getLogger(__name__)


class ProbabilityEstimationError(Exception):
    """Custom exception for probability estimation errors"""
    pass


def estimate_probabilities_from_market_consensus(
    db: Session, 
    event_external_id: str, 
    market_key: str = 'h2h'
) -> Dict[str, float]:
    """
    Estimate true probabilities for an event using market consensus from top sportsbooks.
    
    Uses weighted fair odds calculation with:
    - Pinnacle: 50% weight (sharp, low-vig lines)
    - DraftKings: 25% weight (major US operator)
    - FanDuel: 25% weight (major US operator)
    
    This approach assumes that the market consensus from these three books
    represents the best available estimate of true probabilities.
    
    Args:
        db: Database session
        event_external_id: External ID of the event
        market_key: Market type (default 'h2h' for moneyline)
        
    Returns:
        dict: Estimated probabilities for each outcome
        {
            'probability_a': float,  # Probability for outcome A (away team)
            'probability_b': float,  # Probability for outcome B (home team)
            'estimation_method': str,
            'books_used': List[str],
            'confidence_score': float,  # 0.0-1.0 based on data quality
            'metadata': dict
        }
        
    Raises:
        ProbabilityEstimationError: If unable to estimate probabilities
    """
    try:
        # Use weighted fair odds calculation from database
        fair_odds_result = calculate_weighted_fair_odds_from_db(
            db=db,
            event_external_id=event_external_id,
            market_key=market_key
        )
        
        # Extract fair probabilities (these ARE our estimated true probabilities)
        probability_a = fair_odds_result['fair_probability_a']
        probability_b = fair_odds_result['fair_probability_b']
        
        # Calculate confidence score based on data quality
        confidence_score = _calculate_confidence_score(fair_odds_result)
        
        return {
            'probability_a': probability_a,
            'probability_b': probability_b,
            'estimation_method': 'weighted_market_consensus',
            'books_used': fair_odds_result['books_used'],
            'confidence_score': confidence_score,
            'metadata': {
                'weights_applied': fair_odds_result['weights_applied'],
                'total_weight': fair_odds_result['total_weight'],
                'book_count': fair_odds_result['book_count'],
                'residual_vig': fair_odds_result['residual_vig'],
                'individual_vigs': fair_odds_result['individual_vigs'],
                'fair_odds_a': fair_odds_result['fair_odds_a'],
                'fair_odds_b': fair_odds_result['fair_odds_b']
            }
        }
        
    except OddsConversionError as e:
        # Try fallback method if weighted calculation fails
        logger.warning(f"Weighted consensus failed for {event_external_id}: {e}")
        return estimate_probabilities_fallback(db, event_external_id, market_key)
        
    except Exception as e:
        raise ProbabilityEstimationError(f"Failed to estimate probabilities for {event_external_id}: {e}")


def estimate_probabilities_fallback(
    db: Session, 
    event_external_id: str, 
    market_key: str = 'h2h'
) -> Dict[str, float]:
    """
    Fallback probability estimation using simple market average when weighted method fails.
    
    This method:
    1. Gets odds from all available bookmakers
    2. Calculates simple average of implied probabilities
    3. Normalizes to sum to 1.0
    
    Args:
        db: Database session
        event_external_id: External ID of the event
        market_key: Market type
        
    Returns:
        dict: Estimated probabilities with lower confidence score
    """
    try:
        # Find the event
        event = db.query(EventModel).filter(EventModel.external_id == event_external_id).first()
        if not event:
            raise ProbabilityEstimationError(f"Event {event_external_id} not found")
        
        # Get all odds snapshots for this event
        snapshots = db.query(OddsSnapshotModel).filter(
            OddsSnapshotModel.event_id == event.id,
            OddsSnapshotModel.market_key == market_key
        ).all()
        
        if not snapshots:
            raise ProbabilityEstimationError(f"No odds snapshots found for {event_external_id}")
        
        # Collect implied probabilities from all bookmakers
        prob_a_list = []
        prob_b_list = []
        bookmakers_used = []
        
        for snapshot in snapshots:
            try:
                outcomes = json.loads(snapshot.outcomes_data)
                if len(outcomes) >= 2:
                    odds_a = float(outcomes[0]['price'])
                    odds_b = float(outcomes[1]['price'])
                    
                    prob_a = american_to_implied_probability(odds_a)
                    prob_b = american_to_implied_probability(odds_b)
                    
                    prob_a_list.append(prob_a)
                    prob_b_list.append(prob_b)
                    
                    # Get bookmaker name
                    bookmaker = db.query(BookmakerModel).filter(BookmakerModel.id == snapshot.bookmaker_id).first()
                    if bookmaker:
                        bookmakers_used.append(bookmaker.key)
                        
            except Exception as e:
                logger.warning(f"Error processing snapshot {snapshot.id}: {e}")
                continue
        
        if not prob_a_list:
            raise ProbabilityEstimationError(f"No valid odds found for {event_external_id}")
        
        # Calculate simple averages
        avg_prob_a = sum(prob_a_list) / len(prob_a_list)
        avg_prob_b = sum(prob_b_list) / len(prob_b_list)
        
        # Normalize to sum to 1.0 (remove average vig)
        total_prob = avg_prob_a + avg_prob_b
        fair_prob_a = avg_prob_a / total_prob
        fair_prob_b = avg_prob_b / total_prob
        
        # Lower confidence since this is fallback method
        confidence_score = min(0.6, len(bookmakers_used) * 0.1)
        
        return {
            'probability_a': fair_prob_a,
            'probability_b': fair_prob_b,
            'estimation_method': 'simple_market_average',
            'books_used': bookmakers_used,
            'confidence_score': confidence_score,
            'metadata': {
                'bookmaker_count': len(bookmakers_used),
                'average_vig': total_prob - 1.0,
                'raw_prob_a': avg_prob_a,
                'raw_prob_b': avg_prob_b
            }
        }
        
    except Exception as e:
        raise ProbabilityEstimationError(f"Fallback estimation failed for {event_external_id}: {e}")


def estimate_probabilities_naive(
    probability_a: float = 0.5, 
    probability_b: float = 0.5
) -> Dict[str, float]:
    """
    Naive probability estimation (50/50 split).
    
    This is the least accurate method but serves as a last resort.
    Should only be used when market data is completely unavailable.
    
    Args:
        probability_a: Probability for outcome A (default 0.5)
        probability_b: Probability for outcome B (default 0.5)
        
    Returns:
        dict: Naive probability estimates with very low confidence
    """
    return {
        'probability_a': probability_a,
        'probability_b': probability_b,
        'estimation_method': 'naive_equal_split',
        'books_used': [],
        'confidence_score': 0.1,  # Very low confidence
        'metadata': {
            'warning': 'Using naive 50/50 split - market data unavailable'
        }
    }


def _calculate_confidence_score(fair_odds_result: Dict) -> float:
    """
    Calculate confidence score for probability estimation based on data quality.
    
    Factors considered:
    - Number of books used (more is better)
    - Which specific books are available (Pinnacle is most important)
    - Total weight coverage (higher is better)
    - Consistency across books (lower residual vig is better)
    
    Args:
        fair_odds_result: Result from weighted fair odds calculation
        
    Returns:
        float: Confidence score from 0.0 to 1.0
    """
    score = 0.0
    
    books_used = fair_odds_result.get('books_used', [])
    book_count = len(books_used)
    total_weight = fair_odds_result.get('total_weight', 0.0)
    residual_vig = abs(fair_odds_result.get('residual_vig', 0.1))
    
    # Base score from number of books (max 0.4)
    if book_count >= 3:
        score += 0.4
    elif book_count == 2:
        score += 0.3
    elif book_count == 1:
        score += 0.2
    
    # Bonus for having Pinnacle (max 0.3)
    if 'pinnacle' in books_used:
        score += 0.3
    elif 'draftkings' in books_used or 'fanduel' in books_used:
        score += 0.15
    
    # Weight coverage bonus (max 0.2)
    weight_coverage = min(1.0, total_weight)
    score += 0.2 * weight_coverage
    
    # Consistency bonus - lower residual vig is better (max 0.1)
    if residual_vig < 0.01:  # Less than 1% residual vig
        score += 0.1
    elif residual_vig < 0.02:  # Less than 2% residual vig
        score += 0.05
    
    return min(1.0, score)


if __name__ == "__main__":
    # Test probability estimation methods
    print("=== Probability Estimation Testing ===")
    
    # This would normally use database session
    print("Note: Database testing requires active session")
    
    # Test naive estimation
    naive_probs = estimate_probabilities_naive()
    print(f"\nNaive estimation: {naive_probs}")
    
    # Test confidence scoring
    mock_fair_odds = {
        'books_used': ['pinnacle', 'draftkings', 'fanduel'],
        'total_weight': 1.0,
        'residual_vig': 0.005
    }
    confidence = _calculate_confidence_score(mock_fair_odds)
    print(f"Mock confidence score: {confidence:.3f}") 