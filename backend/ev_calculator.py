"""
🚨 Finalized Corrected EV Calculator (May 23, 2025)

Implements the exact 7-step No-Vig & +EV Logic as specified:

Step 1: Determine Sharp Sportsbook Base Line
Step 2: Calculate No-Vig (Fair Odds) for Each Sportsbook  
Step 3: Choose Best Available No-Vig Line
Step 4: Adjust for 2% P2P Exchange Fee
Step 5: Add EV Buffer (2% for Main, 3% for Alternate Lines)
Step 6: Compare to Current P2P Odds
Step 7: Highlight Significant Book-to-Book Opportunities

This replaces the previous overcomplicated approach with a clear, systematic methodology.
"""

from typing import Dict, List, Optional, Union
from sqlalchemy.orm import Session
from datetime import datetime
import json
import logging

from .database import (
    SessionLocal, EventModel, OddsSnapshotModel, BookmakerModel, EVCalculationModel
)

logger = logging.getLogger(__name__)


class EVCalculationError(Exception):
    """Custom exception for EV calculation errors"""
    pass


def american_to_probability(odds: Union[int, float]) -> float:
    """Convert American odds to implied probability"""
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)


def probability_to_american(probability: float) -> float:
    """Convert probability to American odds"""
    if probability >= 0.5:
        return -(probability / (1 - probability)) * 100
    else:
        return ((1 - probability) / probability) * 100


def remove_vig_from_two_sided_market(odds_a: Union[int, float], odds_b: Union[int, float]) -> Dict[str, float]:
    """
    Step 2: Calculate No-Vig (Fair Odds) for a two-sided market
    
    Convert two-sided odds to implied probabilities, remove vig, get fair odds.
    
    Args:
        odds_a: American odds for outcome A
        odds_b: American odds for outcome B
        
    Returns:
        dict: Fair odds and probabilities after vig removal
        {
            'fair_probability_a': float,
            'fair_probability_b': float, 
            'fair_odds_a': float,
            'fair_odds_b': float,
            'vig_percentage': float,
            'original_total_probability': float
        }
    """
    try:
        # Convert to implied probabilities
        prob_a = american_to_probability(odds_a)
        prob_b = american_to_probability(odds_b)
        
        # Total probability shows the vig
        total_prob = prob_a + prob_b
        vig_percentage = (total_prob - 1.0) * 100
        
        # Remove vig by normalizing probabilities to sum to 1.0
        fair_prob_a = prob_a / total_prob
        fair_prob_b = prob_b / total_prob
        
        # Convert back to American odds
        fair_odds_a = probability_to_american(fair_prob_a)
        fair_odds_b = probability_to_american(fair_prob_b)
        
        return {
            'fair_probability_a': fair_prob_a,
            'fair_probability_b': fair_prob_b,
            'fair_odds_a': fair_odds_a,
            'fair_odds_b': fair_odds_b,
            'vig_percentage': vig_percentage,
            'original_total_probability': total_prob
        }
        
    except Exception as e:
        raise EVCalculationError(f"Failed to remove vig: {e}")


def calculate_recommended_odds_with_buffers(fair_odds: Union[int, float], 
                                            is_alternate_line: bool = False) -> Dict[str, float]:
    """
    Steps 4-5: Adjust for 2% P2P Exchange Fee + Add EV Buffer
    
    Args:
        fair_odds: Fair odds after vig removal
        is_alternate_line: True for alternate/prop lines (3% buffer), False for main lines (2% buffer)
        
    Returns:
        dict: Recommended odds with P2P fee and EV buffer applied
        {
            'fair_probability': float,
            'probability_after_p2p_fee': float,
            'probability_after_ev_buffer': float,
            'recommended_minimum_odds': float,
            'p2p_fee_percentage': float,
            'ev_buffer_percentage': float,
            'is_alternate_line': bool
        }
    """
    try:
        # Convert fair odds to probability
        fair_probability = american_to_probability(fair_odds)
        
        # Step 4: Adjust for 2% P2P Exchange Fee
        p2p_fee = 0.02
        probability_after_fee = fair_probability / (1 - p2p_fee)
        
        # Step 5: Add EV Buffer (2% for main, 3% for alternate lines)
        ev_buffer = 0.03 if is_alternate_line else 0.02
        probability_after_buffer = probability_after_fee + ev_buffer
        
        # Ensure probability doesn't exceed 1.0
        if probability_after_buffer >= 1.0:
            probability_after_buffer = 0.99
            
        # Convert back to recommended minimum odds
        recommended_odds = probability_to_american(probability_after_buffer)
        
        return {
            'fair_probability': fair_probability,
            'probability_after_p2p_fee': probability_after_fee,
            'probability_after_ev_buffer': probability_after_buffer,
            'recommended_minimum_odds': recommended_odds,
            'p2p_fee_percentage': p2p_fee * 100,
            'ev_buffer_percentage': ev_buffer * 100,
            'is_alternate_line': is_alternate_line
        }
        
    except Exception as e:
        raise EVCalculationError(f"Failed to calculate recommended odds: {e}")


def calculate_ev_for_event_and_outcome(bookmaker_odds_data: Dict[str, Dict], 
                                       target_bookmaker: str,
                                       target_outcome: int,
                                       is_alternate_line: bool = False) -> Dict[str, any]:
    """
    Complete 7-Step EV Calculation for a specific bookmaker and outcome
    
    Args:
        bookmaker_odds_data: Dict of {bookmaker_key: {'odds_a': float, 'odds_b': float}}
        target_bookmaker: Which bookmaker we're evaluating 
        target_outcome: 0 for outcome A, 1 for outcome B
        is_alternate_line: True for alternate/prop lines
        
    Returns:
        dict: Complete EV analysis following the 7-step process
    """
    try:
        result = {
            'target_bookmaker': target_bookmaker,
            'target_outcome': target_outcome,
            'is_alternate_line': is_alternate_line,
            'success': False,
            'error': None
        }
        
        if target_bookmaker not in bookmaker_odds_data:
            result['error'] = f"Target bookmaker {target_bookmaker} not found in odds data"
            return result
            
        target_odds_data = bookmaker_odds_data[target_bookmaker]
        target_odds = target_odds_data['odds_a'] if target_outcome == 0 else target_odds_data['odds_b']
        
        # Step 1: Determine Sharp Sportsbook Base Line
        # Find the best (most favorable to bettor) odds available
        best_odds = target_odds
        sharp_bookmaker = target_bookmaker
        
        for bookmaker, odds_data in bookmaker_odds_data.items():
            comparison_odds = odds_data['odds_a'] if target_outcome == 0 else odds_data['odds_b']
            
            # Higher positive odds or less negative odds are better for the bettor
            if ((comparison_odds > 0 and best_odds > 0 and comparison_odds > best_odds) or
                    (comparison_odds < 0 and best_odds < 0 and comparison_odds > best_odds) or
                    (comparison_odds > 0 and best_odds < 0)):
                best_odds = comparison_odds
                sharp_bookmaker = bookmaker
        
        result['step1_sharp_baseline'] = {
            'best_odds': best_odds,
            'sharp_bookmaker': sharp_bookmaker
        }
        
        # Step 2: Calculate No-Vig (Fair Odds) for Each Sportsbook
        no_vig_results = {}
        for bookmaker, odds_data in bookmaker_odds_data.items():
            try:
                no_vig = remove_vig_from_two_sided_market(odds_data['odds_a'], odds_data['odds_b'])
                fair_odds_for_outcome = no_vig['fair_odds_a'] if target_outcome == 0 else no_vig['fair_odds_b']
                no_vig_results[bookmaker] = {
                    'fair_odds': fair_odds_for_outcome,
                    'vig_percentage': no_vig['vig_percentage'],
                    'full_calculation': no_vig
                }
            except Exception as e:
                logger.warning(f"Failed to calculate no-vig for {bookmaker}: {e}")
                continue
                
        result['step2_no_vig_calculations'] = no_vig_results
        
        # Step 3: Choose Best Available No-Vig Line
        if not no_vig_results:
            result['error'] = "No valid no-vig calculations available"
            return result
            
        best_no_vig_odds = None
        best_no_vig_bookmaker = None
        
        for bookmaker, no_vig_data in no_vig_results.items():
            fair_odds = no_vig_data['fair_odds']
            
            if best_no_vig_odds is None:
                best_no_vig_odds = fair_odds
                best_no_vig_bookmaker = bookmaker
            else:
                # Choose the most favorable no-vig odds for the bettor
                if ((fair_odds > 0 and best_no_vig_odds > 0 and fair_odds > best_no_vig_odds) or
                        (fair_odds < 0 and best_no_vig_odds < 0 and fair_odds > best_no_vig_odds) or
                        (fair_odds > 0 and best_no_vig_odds < 0)):
                    best_no_vig_odds = fair_odds
                    best_no_vig_bookmaker = bookmaker
        
        result['step3_best_no_vig'] = {
            'best_no_vig_odds': best_no_vig_odds,
            'best_no_vig_bookmaker': best_no_vig_bookmaker
        }
        
        # Steps 4-5: Adjust for P2P Fee + EV Buffer
        recommended_calc = calculate_recommended_odds_with_buffers(
            fair_odds=best_no_vig_odds,
            is_alternate_line=is_alternate_line
        )
        
        result['step4_5_recommended_odds'] = recommended_calc
        
        # Step 6: Compare to Current P2P Odds & Target Bookmaker Odds
        target_probability = american_to_probability(target_odds)
        recommended_probability = recommended_calc['probability_after_ev_buffer']
        
        # Calculate EV: Expected value based on fair probability vs offered odds
        # EV = (fair_probability * profit) - ((1 - fair_probability) * bet_amount) 
        # Express as percentage of bet amount
        
        fair_probability = recommended_calc['fair_probability']
        
        if target_odds > 0:
            # Positive odds: profit = odds value for $100 bet
            profit = target_odds
        else:
            # Negative odds: profit = $100 / (abs(odds)/100) for $100 bet
            profit = 100 / (abs(target_odds) / 100)
        
        # Calculate expected value for $100 bet
        expected_value_dollars = (fair_probability * profit) - ((1 - fair_probability) * 100)
        
        # Convert to percentage EV
        expected_value_percentage = expected_value_dollars / 100 * 100  # EV as percentage
        
        # Determine if it's +EV based on our conservative threshold
        has_positive_ev = target_probability < recommended_probability
        
        result['step6_ev_analysis'] = {
            'target_odds': target_odds,
            'target_implied_probability': target_probability,
            'recommended_minimum_odds': recommended_calc['recommended_minimum_odds'],
            'recommended_implied_probability': recommended_probability,
            'has_positive_ev': has_positive_ev,
            'expected_value_percentage': expected_value_percentage,
            'expected_value_per_100': expected_value_dollars,
            'fair_probability_estimate': fair_probability
        }
        
        # Step 7: Highlight Significant Book-to-Book Opportunities
        book_to_book_opportunities = []
        for bookmaker, odds_data in bookmaker_odds_data.items():
            if bookmaker == target_bookmaker:
                continue
                
            comparison_odds = odds_data['odds_a'] if target_outcome == 0 else odds_data['odds_b']
            comparison_prob = american_to_probability(comparison_odds)
            
            # Look for significant differences (>5% probability difference)
            prob_difference = abs(target_probability - comparison_prob)
            if prob_difference > 0.05:  # 5% threshold
                book_to_book_opportunities.append({
                    'comparison_bookmaker': bookmaker,
                    'comparison_odds': comparison_odds,
                    'comparison_probability': comparison_prob,
                    'probability_difference': prob_difference,
                    'target_better': target_probability < comparison_prob
                })
        
        result['step7_book_to_book_opportunities'] = book_to_book_opportunities
        
        result['success'] = True
        return result
        
    except Exception as e:
        result['error'] = f"EV calculation failed: {e}"
        return result


def calculate_comprehensive_ev(bookmaker_odds_data: Dict[str, Dict],
                               target_bookmaker: str,
                               is_alternate_line: bool = False) -> Dict[str, any]:
    """
    Calculate EV for both outcomes of an event using the 7-step methodology
    
    Args:
        bookmaker_odds_data: Dict of {bookmaker_key: {'odds_a': float, 'odds_b': float}}
        target_bookmaker: Bookmaker to evaluate
        is_alternate_line: True for alternate/prop lines (3% buffer vs 2%)
        
    Returns:
        dict: Complete EV analysis for both outcomes
    """
    try:
        return {
            'target_bookmaker': target_bookmaker,
            'outcome_a_analysis': calculate_ev_for_event_and_outcome(
                bookmaker_odds_data, target_bookmaker, 0, is_alternate_line
            ),
            'outcome_b_analysis': calculate_ev_for_event_and_outcome(
                bookmaker_odds_data, target_bookmaker, 1, is_alternate_line
            ),
            'calculation_method': '7_step_corrected_logic',
            'is_alternate_line': is_alternate_line
        }
        
    except Exception as e:
        return {
            'target_bookmaker': target_bookmaker,
            'error': "Comprehensive EV calculation failed: {}".format(e),
            'success': False
        }


def store_ev_calculations_to_db(db: Session, 
                                event_external_id: str, 
                                bookmaker_key: str,
                                market_key: str, 
                                ev_results: Dict[str, any],
                                odds_snapshot_time: Optional[datetime] = None) -> List[EVCalculationModel]:
    """
    Store the new 7-step EV calculation results to the database
    
    Args:
        db: Database session
        event_external_id: External ID of the event
        bookmaker_key: Key of the bookmaker
        market_key: Market key (e.g., 'h2h')
        ev_results: Results from calculate_comprehensive_ev
        odds_snapshot_time: When the odds were captured
        
    Returns:
        List of stored EV calculation records
    """
    try:
        # Get event and bookmaker
        event = db.query(EventModel).filter(EventModel.external_id == event_external_id).first()
        if not event:
            raise EVCalculationError("Event {} not found".format(event_external_id))
        
        bookmaker = db.query(BookmakerModel).filter(BookmakerModel.key == bookmaker_key).first()
        if not bookmaker:
            raise EVCalculationError("Bookmaker {} not found".format(bookmaker_key))
        
        ev_records = []
        
        # Store results for both outcomes
        for outcome_letter in ['a', 'b']:
            outcome_key = "outcome_{}_analysis".format(outcome_letter)
            outcome_index = 0 if outcome_letter == 'a' else 1
            
            if outcome_key not in ev_results:
                continue
                
            analysis = ev_results[outcome_key]
            
            if not analysis.get('success'):
                continue
                
            step6 = analysis.get('step6_ev_analysis', {})
            step4_5 = analysis.get('step4_5_recommended_odds', {})
            
            # Create database record with the new calculation method
            ev_record = EVCalculationModel(
                event_id=event.id,
                bookmaker_id=bookmaker.id,
                market_key=market_key,
                outcome_name="outcome_{}".format(outcome_letter.upper()),
                outcome_index=outcome_index,
                offered_odds=step6.get('target_odds', 0),
                
                # Store the main EV result - use percentage EV
                standard_ev=step6.get('expected_value_percentage', 0),
                no_vig_ev=step6.get('expected_value_percentage', 0),  # Same value for consistency
                weighted_fair_ev=None,  # Not using weighted calculation anymore
                
                # Store probabilities
                standard_implied_probability=step6.get('target_implied_probability', 0),
                no_vig_fair_probability=step4_5.get('fair_probability', 0),
                weighted_fair_probability=None,
                
                # Store reference odds
                no_vig_fair_odds=step4_5.get('recommended_minimum_odds', 0),
                weighted_fair_odds=None,
                
                # Store full calculation details
                calculation_method_details=json.dumps(analysis, default=str),
                books_used_in_weighted=None,
                vig_percentage=None,
                
                # Timestamps
                odds_snapshot_time=odds_snapshot_time,
                
                # Quality indicators
                has_positive_standard_ev=step6.get('has_positive_ev', False),
                has_positive_no_vig_ev=step6.get('has_positive_ev', False),
                has_positive_weighted_ev=False
            )
            
            db.add(ev_record)
            ev_records.append(ev_record)
        
        db.commit()
        return ev_records
        
    except Exception as e:
        db.rollback()
        raise EVCalculationError("Failed to store EV calculations: {}".format(e))


def get_ev_calculations_from_db(db: Session, 
                                event_external_id: str, 
                                bookmaker_key: Optional[str] = None,
                                market_key: str = 'h2h') -> List[Dict[str, any]]:
    """
    Retrieve EV calculations from database
    
    Args:
        db: Database session
        event_external_id: External ID of the event
        bookmaker_key: Optional specific bookmaker key
        market_key: Market key (default 'h2h')
        
    Returns:
        List of EV calculation dictionaries
    """
    try:
        query = db.query(EVCalculationModel).join(EventModel).filter(
            EventModel.external_id == event_external_id,
            EVCalculationModel.market_key == market_key
        )
        
        if bookmaker_key:
            query = query.join(BookmakerModel).filter(BookmakerModel.key == bookmaker_key)
        
        calculations = query.all()
        
        results = []
        for calc in calculations:
            bookmaker = db.query(BookmakerModel).filter(BookmakerModel.id == calc.bookmaker_id).first()
            
            results.append({
                'id': calc.id,
                'event_external_id': event_external_id,
                'bookmaker': {
                    'key': bookmaker.key if bookmaker else None,
                    'title': bookmaker.title if bookmaker else None
                },
                'market_key': calc.market_key,
                'outcome_name': calc.outcome_name,
                'outcome_index': calc.outcome_index,
                'offered_odds': calc.offered_odds,
                'standard_ev': calc.standard_ev,
                'no_vig_ev': calc.no_vig_ev,
                'weighted_fair_ev': calc.weighted_fair_ev,
                'standard_implied_probability': calc.standard_implied_probability,
                'no_vig_fair_probability': calc.no_vig_fair_probability,
                'weighted_fair_probability': calc.weighted_fair_probability,
                'no_vig_fair_odds': calc.no_vig_fair_odds,
                'weighted_fair_odds': calc.weighted_fair_odds,
                'vig_percentage': calc.vig_percentage,
                'books_used_in_weighted': calc.books_used_in_weighted,
                'has_positive_standard_ev': calc.has_positive_standard_ev,
                'has_positive_no_vig_ev': calc.has_positive_no_vig_ev,
                'has_positive_weighted_ev': calc.has_positive_weighted_ev,
                'calculated_at': calc.created_at,
                'calculation_method_details': (json.loads(calc.calculation_method_details) 
                                              if calc.calculation_method_details else None)
            })
        
        return results
        
    except Exception as e:
        logger.error("Failed to retrieve EV calculations: {}".format(e))
        return []


if __name__ == "__main__":
    # Example usage and testing with the new 7-step methodology
    print("=== 7-Step EV Calculator Testing ===")
    
    # User's example: Milwaukee Brewers @ Pittsburgh Pirates
    print("\nUser's Example: Milwaukee Brewers @ Pittsburgh Pirates")
    
    bookmaker_odds_data = {
        'pinnacle': {'odds_a': +113, 'odds_b': -123},  # Brewers, Pirates
        'draftkings': {'odds_a': +110, 'odds_b': -125},
        'fanduel': {'odds_a': +108, 'odds_b': -120}
    }
    
    # Test calculation for Brewers (outcome A)
    results = calculate_comprehensive_ev(
        bookmaker_odds_data=bookmaker_odds_data,
        target_bookmaker='pinnacle',
        is_alternate_line=False
    )
    
    if 'outcome_a_analysis' in results and results['outcome_a_analysis'].get('success'):
        step6 = results['outcome_a_analysis']['step6_ev_analysis']
        print(f"\nBrewers (+113 at Pinnacle):")
        print(f"  Expected Value: {step6['expected_value_percentage']:.2f}%")
        print(f"  Recommended Minimum: {step6['recommended_minimum_odds']:+.0f}")
        print(f"  Has +EV: {step6['has_positive_ev']}")
        print(f"  Fair Probability: {step6['fair_probability_estimate']:.4f}")
    
    print("\n" + "="*50) 