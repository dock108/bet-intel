"""
Comprehensive Expected Value (EV) Calculator for Betting Intelligence Platform

This module provides three distinct EV calculation methods:
1. Standard EV: Using raw bookmaker odds (includes vig)
2. No-Vig EV: Using vig-removed fair odds from two-sided markets
3. Weighted Fair Odds EV: Using weighted fair odds from Pinnacle (50%), DraftKings (25%), FanDuel (25%)

Each method serves different purposes in betting analysis and value identification.
"""

from typing import Dict, List, Tuple, Optional, Union
from sqlalchemy.orm import Session
from datetime import datetime
import json
import logging

from backend.odds_converter import (
    american_to_implied_probability,
    remove_vig_two_sided,
    calculate_weighted_fair_odds,
    calculate_expected_value,
    OddsConversionError
)
from backend.database import (
    EVCalculationModel, 
    EventModel, 
    BookmakerModel
)

logger = logging.getLogger(__name__)


class EVCalculationError(Exception):
    """Custom exception for EV calculation errors"""
    pass


def calculate_standard_ev(probability: float, odds: Union[int, float], bet_amount: float = 100.0) -> Dict[str, float]:
    """
    Calculate standard Expected Value using raw bookmaker odds (includes vig).
    
    This is the most basic EV calculation that assumes the bettor's estimated probability
    is correct and compares it against the bookmaker's offered odds without any adjustment
    for vig or market inefficiencies.
    
    Args:
        probability: Bettor's estimated true probability of outcome (0.0 to 1.0)
        odds: American odds offered by bookmaker
        bet_amount: Amount to bet (default $100)
        
    Returns:
        dict: Standard EV calculation results
        {
            'ev': float,                    # Expected value in dollars
            'ev_per_dollar': float,         # EV per $1 bet
            'implied_probability': float,   # Bookmaker's implied probability
            'probability_edge': float,      # Difference between true and implied probability
            'has_positive_ev': bool,        # Whether EV is positive
            'method': str                   # 'standard'
        }
        
    Examples:
        >>> calculate_standard_ev(0.55, 120)  # 55% chance at +120 odds
        {
            'ev': 21.0,
            'ev_per_dollar': 0.21,
            'implied_probability': 0.4545,
            'probability_edge': 0.0955,
            'has_positive_ev': True,
            'method': 'standard'
        }
    """
    try:
        # Calculate basic EV
        ev = calculate_expected_value(probability, odds, bet_amount)
        
        # Get implied probability from bookmaker odds
        implied_prob = american_to_implied_probability(odds)
        
        # Calculate probability edge
        prob_edge = probability - implied_prob
        
        return {
            'ev': ev,
            'ev_per_dollar': ev / bet_amount,
            'implied_probability': implied_prob,
            'probability_edge': prob_edge,
            'has_positive_ev': ev > 0,
            'method': 'standard',
            'bet_amount': bet_amount,
            'true_probability': probability,
            'offered_odds': odds
        }
        
    except Exception as e:
        raise EVCalculationError(f"Failed to calculate standard EV: {e}")


def calculate_no_vig_ev(probability_a: float, probability_b: float, 
                        odds_a: Union[int, float], odds_b: Union[int, float],
                        target_outcome: int = 0, bet_amount: float = 100.0) -> Dict[str, any]:
    """
    Calculate No-Vig Expected Value using vig-removed fair odds.
    
    This method removes the bookmaker's built-in profit margin (vig) from a two-sided
    market to calculate truly fair odds, then computes EV against these fair odds.
    More accurate than standard EV as it accounts for the bookmaker's edge.
    
    Args:
        probability_a: Bettor's estimated probability for outcome A
        probability_b: Bettor's estimated probability for outcome B  
        odds_a: Bookmaker's odds for outcome A
        odds_b: Bookmaker's odds for outcome B
        target_outcome: Which outcome to calculate EV for (0 for A, 1 for B)
        bet_amount: Amount to bet (default $100)
        
    Returns:
        dict: No-vig EV calculation results
        {
            'ev': float,                    # Expected value in dollars
            'ev_per_dollar': float,         # EV per $1 bet
            'fair_probability': float,      # Fair probability after vig removal
            'fair_odds': float,             # Fair odds after vig removal
            'probability_edge': float,      # Edge vs fair probability
            'has_positive_ev': bool,        # Whether EV is positive
            'vig_percentage': float,        # Vig removed from market
            'method': str,                  # 'no_vig'
            'vig_removal_details': dict     # Full vig removal calculation
        }
        
    Examples:
        >>> calculate_no_vig_ev(0.55, 0.45, -110, -110, target_outcome=0)
        # 55% vs 45% probabilities, both sides -110, calculate EV for outcome A
    """
    try:
        # Validate probabilities sum to 1.0
        if abs((probability_a + probability_b) - 1.0) > 1e-6:
            raise EVCalculationError(
                f"Probabilities must sum to 1.0, got {probability_a + probability_b:.6f}"
            )
        
        # Remove vig to get fair odds
        vig_result = remove_vig_two_sided(odds_a, odds_b)
        
        # Select target outcome data
        if target_outcome == 0:
            true_prob = probability_a
            offered_odds = odds_a
            fair_prob = vig_result['fair_probability_a']
            fair_odds = vig_result['fair_odds_a']
        elif target_outcome == 1:
            true_prob = probability_b
            offered_odds = odds_b
            fair_prob = vig_result['fair_probability_b']
            fair_odds = vig_result['fair_odds_b']
        else:
            raise EVCalculationError(f"Invalid target_outcome: {target_outcome}. Must be 0 or 1.")
        
        # Calculate EV using offered odds but true probability
        ev = calculate_expected_value(true_prob, offered_odds, bet_amount)
        
        # Calculate probability edge vs fair odds
        prob_edge = true_prob - fair_prob
        
        return {
            'ev': ev,
            'ev_per_dollar': ev / bet_amount,
            'fair_probability': fair_prob,
            'fair_odds': fair_odds,
            'probability_edge': prob_edge,
            'has_positive_ev': ev > 0,
            'vig_percentage': vig_result['vig_percentage'],
            'method': 'no_vig',
            'bet_amount': bet_amount,
            'true_probability': true_prob,
            'offered_odds': offered_odds,
            'target_outcome': target_outcome,
            'vig_removal_details': vig_result
        }
        
    except OddsConversionError:
        # Re-raise odds conversion errors
        raise
    except Exception as e:
        raise EVCalculationError(f"Failed to calculate no-vig EV: {e}")


def calculate_weighted_fair_ev(probability_a: float, probability_b: float,
                               pinnacle_odds: Optional[Tuple[float, float]] = None,
                               draftkings_odds: Optional[Tuple[float, float]] = None,
                               fanduel_odds: Optional[Tuple[float, float]] = None,
                               target_outcome: int = 0, bet_amount: float = 100.0) -> Dict[str, any]:
    """
    Calculate Weighted Fair Odds Expected Value using Pinnacle (50%), DraftKings (25%), FanDuel (25%).
    
    This is the most sophisticated EV calculation method, using weighted fair odds from
    the three most trusted sportsbooks. Provides the most accurate assessment of true
    market value by leveraging Pinnacle's sharp lines and major US operators.
    
    Args:
        probability_a: Bettor's estimated probability for outcome A
        probability_b: Bettor's estimated probability for outcome B
        pinnacle_odds: Tuple of (odds_a, odds_b) from Pinnacle (optional)
        draftkings_odds: Tuple of (odds_a, odds_b) from DraftKings (optional)
        fanduel_odds: Tuple of (odds_a, odds_b) from FanDuel (optional)
        target_outcome: Which outcome to calculate EV for (0 for A, 1 for B)
        bet_amount: Amount to bet (default $100)
        
    Returns:
        dict: Weighted fair odds EV calculation results
        {
            'ev': float,                      # Expected value in dollars
            'ev_per_dollar': float,           # EV per $1 bet
            'fair_probability': float,        # Weighted fair probability
            'fair_odds': float,               # Weighted fair odds
            'probability_edge': float,        # Edge vs weighted fair probability
            'has_positive_ev': bool,          # Whether EV is positive
            'books_used': List[str],          # Books used in calculation
            'weights_applied': Dict[str, float], # Actual weights used
            'method': str,                    # 'weighted_fair'
            'weighted_calculation_details': dict  # Full weighted calculation
        }
        
    Examples:
        >>> calculate_weighted_fair_ev(
        ...     0.55, 0.45,
        ...     pinnacle_odds=(-105, -105),
        ...     draftkings_odds=(-110, -110),
        ...     fanduel_odds=(-108, -108),
        ...     target_outcome=0
        ... )
    """
    try:
        # Validate probabilities sum to 1.0
        if abs((probability_a + probability_b) - 1.0) > 1e-6:
            raise EVCalculationError(
                f"Probabilities must sum to 1.0, got {probability_a + probability_b:.6f}"
            )
        
        # Calculate weighted fair odds
        weighted_result = calculate_weighted_fair_odds(
            pinnacle_odds=pinnacle_odds,
            draftkings_odds=draftkings_odds,
            fanduel_odds=fanduel_odds
        )
        
        # Select target outcome data
        if target_outcome == 0:
            true_prob = probability_a
            fair_prob = weighted_result['fair_probability_a']
            fair_odds = weighted_result['fair_odds_a']
        elif target_outcome == 1:
            true_prob = probability_b
            fair_prob = weighted_result['fair_probability_b']
            fair_odds = weighted_result['fair_odds_b']
        else:
            raise EVCalculationError(f"Invalid target_outcome: {target_outcome}. Must be 0 or 1.")
        
        # Calculate EV using fair odds as the "offered" odds
        # This shows the value vs the market consensus
        ev = calculate_expected_value(true_prob, fair_odds, bet_amount)
        
        # Calculate probability edge vs weighted fair odds
        prob_edge = true_prob - fair_prob
        
        return {
            'ev': ev,
            'ev_per_dollar': ev / bet_amount,
            'fair_probability': fair_prob,
            'fair_odds': fair_odds,
            'probability_edge': prob_edge,
            'has_positive_ev': ev > 0,
            'books_used': weighted_result['books_used'],
            'weights_applied': weighted_result['weights_applied'],
            'method': 'weighted_fair',
            'bet_amount': bet_amount,
            'true_probability': true_prob,
            'target_outcome': target_outcome,
            'weighted_calculation_details': weighted_result
        }
        
    except OddsConversionError:
        # Re-raise odds conversion errors
        raise
    except Exception as e:
        raise EVCalculationError(f"Failed to calculate weighted fair EV: {e}")


def calculate_comprehensive_ev(probability_a: float, probability_b: float,
                               offered_odds_a: Union[int, float], offered_odds_b: Union[int, float],
                               pinnacle_odds: Optional[Tuple[float, float]] = None,
                               draftkings_odds: Optional[Tuple[float, float]] = None,
                               fanduel_odds: Optional[Tuple[float, float]] = None,
                               target_outcome: int = 0, bet_amount: float = 100.0) -> Dict[str, any]:
    """
    Calculate all three EV methods for comprehensive analysis.
    
    This function combines all three EV calculation methods to provide a complete
    picture of betting value from different perspectives. Each method offers unique
    insights into market efficiency and betting opportunities.
    
    Args:
        probability_a: Bettor's estimated probability for outcome A
        probability_b: Bettor's estimated probability for outcome B
        offered_odds_a: Bookmaker's offered odds for outcome A
        offered_odds_b: Bookmaker's offered odds for outcome B
        pinnacle_odds: Tuple of (odds_a, odds_b) from Pinnacle (optional)
        draftkings_odds: Tuple of (odds_a, odds_b) from DraftKings (optional)
        fanduel_odds: Tuple of (odds_a, odds_b) from FanDuel (optional)
        target_outcome: Which outcome to calculate EV for (0 for A, 1 for B)
        bet_amount: Amount to bet (default $100)
        
    Returns:
        dict: All three EV calculations plus comparison analysis
        {
            'standard_ev': dict,      # Standard EV calculation
            'no_vig_ev': dict,        # No-vig EV calculation
            'weighted_fair_ev': dict, # Weighted fair EV calculation
            'comparison': dict,       # Comparison between methods
            'target_outcome': int,    # Which outcome was analyzed
            'recommendation': dict    # Betting recommendation based on all methods
        }
    """
    try:
        results = {
            'target_outcome': target_outcome,
            'bet_amount': bet_amount,
            'true_probabilities': {
                'outcome_a': probability_a,
                'outcome_b': probability_b
            },
            'offered_odds': {
                'outcome_a': offered_odds_a,
                'outcome_b': offered_odds_b
            }
        }
        
        # Select target offered odds
        target_offered_odds = offered_odds_a if target_outcome == 0 else offered_odds_b
        target_probability = probability_a if target_outcome == 0 else probability_b
        
        # Calculate Standard EV
        try:
            results['standard_ev'] = calculate_standard_ev(
                target_probability, target_offered_odds, bet_amount
            )
        except Exception as e:
            logger.error(f"Standard EV calculation failed: {e}")
            results['standard_ev'] = {'error': str(e)}
        
        # Calculate No-Vig EV
        try:
            results['no_vig_ev'] = calculate_no_vig_ev(
                probability_a, probability_b, 
                offered_odds_a, offered_odds_b,
                target_outcome, bet_amount
            )
        except Exception as e:
            logger.error(f"No-vig EV calculation failed: {e}")
            results['no_vig_ev'] = {'error': str(e)}
        
        # Calculate Weighted Fair EV (if reference odds available)
        if pinnacle_odds or draftkings_odds or fanduel_odds:
            try:
                results['weighted_fair_ev'] = calculate_weighted_fair_ev(
                    probability_a, probability_b,
                    pinnacle_odds, draftkings_odds, fanduel_odds,
                    target_outcome, bet_amount
                )
            except Exception as e:
                logger.error(f"Weighted fair EV calculation failed: {e}")
                results['weighted_fair_ev'] = {'error': str(e)}
        else:
            results['weighted_fair_ev'] = {
                'error': 'No reference odds available from Pinnacle, DraftKings, or FanDuel'
            }
        
        # Create comparison analysis
        results['comparison'] = _create_ev_comparison(results)
        
        # Generate betting recommendation
        results['recommendation'] = _generate_betting_recommendation(results)
        
        return results
        
    except Exception as e:
        raise EVCalculationError(f"Failed to calculate comprehensive EV: {e}")


def _create_ev_comparison(results: Dict[str, any]) -> Dict[str, any]:
    """Create comparison analysis between different EV methods."""
    comparison = {
        'methods_available': [],
        'positive_ev_methods': [],
        'ev_values': {},
        'ev_agreement': None,
        'most_conservative': None,
        'most_aggressive': None
    }
    
    # Collect EV values from successful calculations
    ev_values = {}
    
    if 'error' not in results.get('standard_ev', {}):
        comparison['methods_available'].append('standard')
        ev_values['standard'] = results['standard_ev']['ev']
        if results['standard_ev']['has_positive_ev']:
            comparison['positive_ev_methods'].append('standard')
    
    if 'error' not in results.get('no_vig_ev', {}):
        comparison['methods_available'].append('no_vig')
        ev_values['no_vig'] = results['no_vig_ev']['ev']
        if results['no_vig_ev']['has_positive_ev']:
            comparison['positive_ev_methods'].append('no_vig')
    
    if 'error' not in results.get('weighted_fair_ev', {}):
        comparison['methods_available'].append('weighted_fair')
        ev_values['weighted_fair'] = results['weighted_fair_ev']['ev']
        if results['weighted_fair_ev']['has_positive_ev']:
            comparison['positive_ev_methods'].append('weighted_fair')
    
    comparison['ev_values'] = ev_values
    
    # Determine agreement
    if len(comparison['positive_ev_methods']) == len(comparison['methods_available']):
        comparison['ev_agreement'] = 'all_positive'
    elif len(comparison['positive_ev_methods']) == 0:
        comparison['ev_agreement'] = 'all_negative'
    else:
        comparison['ev_agreement'] = 'mixed'
    
    # Find most conservative (lowest EV) and aggressive (highest EV)
    if ev_values:
        min_ev_method = min(ev_values.keys(), key=lambda k: ev_values[k])
        max_ev_method = max(ev_values.keys(), key=lambda k: ev_values[k])
        comparison['most_conservative'] = {
            'method': min_ev_method,
            'ev': ev_values[min_ev_method]
        }
        comparison['most_aggressive'] = {
            'method': max_ev_method,
            'ev': ev_values[max_ev_method]
        }
    
    return comparison


def _generate_betting_recommendation(results: Dict[str, any]) -> Dict[str, any]:
    """Generate betting recommendation based on all EV calculations."""
    comparison = results['comparison']
    
    recommendation = {
        'action': 'no_bet',  # no_bet, bet_small, bet_medium, bet_large
        'confidence': 'low', # low, medium, high
        'reasoning': [],
        'priority_method': None,
        'risk_assessment': 'unknown'
    }
    
    # Determine recommendation based on EV agreement
    if comparison['ev_agreement'] == 'all_positive':
        recommendation['action'] = 'bet_medium'
        recommendation['confidence'] = 'high'
        recommendation['reasoning'].append('All EV methods show positive value')
        recommendation['risk_assessment'] = 'favorable'
        
        # Use weighted fair as priority if available
        if 'weighted_fair' in comparison['methods_available']:
            recommendation['priority_method'] = 'weighted_fair'
            recommendation['action'] = 'bet_large'
        else:
            recommendation['priority_method'] = 'no_vig'
            
    elif comparison['ev_agreement'] == 'all_negative':
        recommendation['action'] = 'no_bet'
        recommendation['confidence'] = 'high'
        recommendation['reasoning'].append('All EV methods show negative value')
        recommendation['risk_assessment'] = 'unfavorable'
        
    elif comparison['ev_agreement'] == 'mixed':
        # Mixed results require more nuanced analysis
        positive_methods = comparison['positive_ev_methods']
        
        if 'weighted_fair' in positive_methods:
            recommendation['action'] = 'bet_small'
            recommendation['confidence'] = 'medium'
            recommendation['priority_method'] = 'weighted_fair'
            recommendation['reasoning'].append('Weighted fair odds show positive EV (most reliable method)')
            recommendation['risk_assessment'] = 'cautiously_favorable'
            
        elif 'no_vig' in positive_methods:
            recommendation['action'] = 'bet_small'
            recommendation['confidence'] = 'low'
            recommendation['priority_method'] = 'no_vig'
            recommendation['reasoning'].append('No-vig calculation shows positive EV')
            recommendation['risk_assessment'] = 'uncertain'
            
        elif 'standard' in positive_methods:
            recommendation['action'] = 'no_bet'
            recommendation['confidence'] = 'low'
            recommendation['reasoning'].append('Only standard EV positive (least reliable due to vig)')
            recommendation['risk_assessment'] = 'questionable'
    
    # Add method availability context
    if len(comparison['methods_available']) == 1:
        recommendation['reasoning'].append(f"Limited to {comparison['methods_available'][0]} method only")
        if recommendation['confidence'] == 'high':
            recommendation['confidence'] = 'medium'
    
    return recommendation


def store_ev_calculations_to_db(db: Session, event_external_id: str, bookmaker_key: str,
                                market_key: str, ev_results: Dict[str, any],
                                odds_snapshot_time: Optional[datetime] = None) -> List[EVCalculationModel]:
    """
    Store comprehensive EV calculation results to database.
    
    Args:
        db: Database session
        event_external_id: External ID of the event
        bookmaker_key: Key of the bookmaker
        market_key: Market type (h2h, spreads, totals)
        ev_results: Results from calculate_comprehensive_ev()
        odds_snapshot_time: When the odds were captured
        
    Returns:
        List[EVCalculationModel]: Created EV calculation records
    """
    try:
        # Get event and bookmaker from database
        event = db.query(EventModel).filter(EventModel.external_id == event_external_id).first()
        if not event:
            raise EVCalculationError(f"Event with external_id '{event_external_id}' not found")
        
        bookmaker = db.query(BookmakerModel).filter(BookmakerModel.key == bookmaker_key).first()
        if not bookmaker:
            raise EVCalculationError(f"Bookmaker with key '{bookmaker_key}' not found")
        
        ev_records = []
        
        # Create records for both outcomes
        for outcome_index in [0, 1]:
            outcome_name = f"outcome_{chr(65 + outcome_index)}"  # outcome_A, outcome_B
            
            # Get offered odds for this outcome
            if outcome_index == 0:
                offered_odds = ev_results['offered_odds']['outcome_a']
            else:
                offered_odds = ev_results['offered_odds']['outcome_b']
            
            # Extract EV values for this outcome
            standard_ev = None
            no_vig_ev = None
            weighted_fair_ev = None
            
            # Standard EV
            if outcome_index == ev_results['target_outcome'] and 'error' not in ev_results.get('standard_ev', {}):
                standard_ev = ev_results['standard_ev']['ev']
                standard_implied_prob = ev_results['standard_ev']['implied_probability']
            else:
                # Calculate for non-target outcome
                prob = ev_results['true_probabilities'][f'outcome_{chr(65 + outcome_index).lower()}']
                try:
                    calc = calculate_standard_ev(prob, offered_odds)
                    standard_ev = calc['ev']
                    standard_implied_prob = calc['implied_probability']
                except Exception:
                    standard_implied_prob = None
            
            # No-vig EV
            if outcome_index == ev_results['target_outcome'] and 'error' not in ev_results.get('no_vig_ev', {}):
                no_vig_ev = ev_results['no_vig_ev']['ev']
                no_vig_fair_prob = ev_results['no_vig_ev']['fair_probability']
                no_vig_fair_odds_val = ev_results['no_vig_ev']['fair_odds']
                vig_percentage = ev_results['no_vig_ev']['vig_percentage']
            else:
                # Calculate for non-target outcome
                prob_a = ev_results['true_probabilities']['outcome_a']
                prob_b = ev_results['true_probabilities']['outcome_b']
                odds_a = ev_results['offered_odds']['outcome_a']
                odds_b = ev_results['offered_odds']['outcome_b']
                try:
                    calc = calculate_no_vig_ev(prob_a, prob_b, odds_a, odds_b, outcome_index)
                    no_vig_ev = calc['ev']
                    no_vig_fair_prob = calc['fair_probability']
                    no_vig_fair_odds_val = calc['fair_odds']
                    vig_percentage = calc['vig_percentage']
                except Exception:
                    no_vig_fair_prob = None
                    no_vig_fair_odds_val = None
                    vig_percentage = None
            
            # Weighted fair EV
            if outcome_index == ev_results['target_outcome'] and 'error' not in ev_results.get('weighted_fair_ev', {}):
                weighted_fair_ev = ev_results['weighted_fair_ev']['ev']
                weighted_fair_prob = ev_results['weighted_fair_ev']['fair_probability']
                weighted_fair_odds_val = ev_results['weighted_fair_ev']['fair_odds']
                books_used = ','.join(ev_results['weighted_fair_ev']['books_used'])
            else:
                # Would need to recalculate for non-target outcome
                weighted_fair_prob = None
                weighted_fair_odds_val = None
                books_used = None
            
            # Create database record
            ev_record = EVCalculationModel(
                event_id=event.id,
                bookmaker_id=bookmaker.id,
                market_key=market_key,
                outcome_name=outcome_name,
                outcome_index=outcome_index,
                offered_odds=offered_odds,
                
                # EV calculations
                standard_ev=standard_ev,
                no_vig_ev=no_vig_ev,
                weighted_fair_ev=weighted_fair_ev,
                
                # Supporting probabilities
                standard_implied_probability=standard_implied_prob,
                no_vig_fair_probability=no_vig_fair_prob,
                weighted_fair_probability=weighted_fair_prob,
                
                # Reference odds
                no_vig_fair_odds=no_vig_fair_odds_val,
                weighted_fair_odds=weighted_fair_odds_val,
                
                # Metadata
                calculation_method_details=json.dumps(ev_results, default=str),
                books_used_in_weighted=books_used,
                vig_percentage=vig_percentage,
                odds_snapshot_time=odds_snapshot_time,
                
                # Quality indicators
                has_positive_standard_ev=(standard_ev or 0) > 0,
                has_positive_no_vig_ev=(no_vig_ev or 0) > 0,
                has_positive_weighted_ev=(weighted_fair_ev or 0) > 0
            )
            
            db.add(ev_record)
            ev_records.append(ev_record)
        
        db.commit()
        return ev_records
        
    except Exception as e:
        db.rollback()
        raise EVCalculationError(f"Failed to store EV calculations: {e}")


def get_ev_calculations_from_db(db: Session, event_external_id: str, 
                                bookmaker_key: Optional[str] = None,
                                market_key: str = 'h2h') -> List[Dict[str, any]]:
    """
    Retrieve EV calculations from database with optional filtering.
    
    Args:
        db: Database session
        event_external_id: External ID of the event
        bookmaker_key: Optional bookmaker filter
        market_key: Market type filter (default 'h2h')
        
    Returns:
        List[Dict]: EV calculation records with event and bookmaker details
    """
    query = (
        db.query(EVCalculationModel)
        .join(EventModel, EVCalculationModel.event_id == EventModel.id)
        .join(BookmakerModel, EVCalculationModel.bookmaker_id == BookmakerModel.id)
        .filter(EventModel.external_id == event_external_id)
        .filter(EVCalculationModel.market_key == market_key)
    )
    
    if bookmaker_key:
        query = query.filter(BookmakerModel.key == bookmaker_key)
    
    records = query.all()
    
    results = []
    for record in records:
        results.append({
            'id': record.id,
            'event': {
                'external_id': record.event.external_id,
                'home_team': record.event.home_team,
                'away_team': record.event.away_team,
                'commence_time': record.event.commence_time
            },
            'bookmaker': {
                'key': record.bookmaker.key,
                'title': record.bookmaker.title
            },
            'market_key': record.market_key,
            'outcome_name': record.outcome_name,
            'outcome_index': record.outcome_index,
            'offered_odds': record.offered_odds,
            
            # EV calculations
            'standard_ev': record.standard_ev,
            'no_vig_ev': record.no_vig_ev,
            'weighted_fair_ev': record.weighted_fair_ev,
            
            # Supporting data
            'standard_implied_probability': record.standard_implied_probability,
            'no_vig_fair_probability': record.no_vig_fair_probability,
            'weighted_fair_probability': record.weighted_fair_probability,
            'no_vig_fair_odds': record.no_vig_fair_odds,
            'weighted_fair_odds': record.weighted_fair_odds,
            'vig_percentage': record.vig_percentage,
            'books_used_in_weighted': record.books_used_in_weighted,
            
            # Quality indicators
            'has_positive_standard_ev': record.has_positive_standard_ev,
            'has_positive_no_vig_ev': record.has_positive_no_vig_ev,
            'has_positive_weighted_ev': record.has_positive_weighted_ev,
            
            # Timestamps
            'calculated_at': record.calculated_at,
            'odds_snapshot_time': record.odds_snapshot_time
        })
    
    return results


if __name__ == "__main__":
    # Example usage and testing
    print("=== Comprehensive EV Calculator Examples ===")
    
    # Test scenario: 55% vs 45% probabilities
    prob_a, prob_b = 0.55, 0.45
    offered_a, offered_b = 120, -150  # Underdog vs favorite
    
    print(f"\nScenario: {prob_a:.0%} vs {prob_b:.0%} true probabilities")
    print(f"Offered odds: {offered_a:+d} vs {offered_b:+d}")
    
    # Calculate comprehensive EV for outcome A (underdog)
    try:
        results = calculate_comprehensive_ev(
            probability_a=prob_a,
            probability_b=prob_b,
            offered_odds_a=offered_a,
            offered_odds_b=offered_b,
            pinnacle_odds=(-105, -105),
            draftkings_odds=(-110, -110),
            fanduel_odds=(-108, -108),
            target_outcome=0  # Calculate for outcome A
        )
        
        print("\n=== EV Results for Outcome A ===")
        
        if 'error' not in results['standard_ev']:
            std_ev = results['standard_ev']
            print(f"Standard EV: ${std_ev['ev']:+.2f} (Edge: {std_ev['probability_edge']:+.2%})")
        
        if 'error' not in results['no_vig_ev']:
            no_vig = results['no_vig_ev']
            print(f"No-Vig EV: ${no_vig['ev']:+.2f} (Vig removed: {no_vig['vig_percentage']:.2%})")
        
        if 'error' not in results['weighted_fair_ev']:
            weighted = results['weighted_fair_ev']
            print(f"Weighted Fair EV: ${weighted['ev']:+.2f} (Books: {weighted['books_used']})")
        
        print("\n=== Recommendation ===")
        rec = results['recommendation']
        print(f"Action: {rec['action']}")
        print(f"Confidence: {rec['confidence']}")
        print(f"Risk Assessment: {rec['risk_assessment']}")
        if rec['reasoning']:
            print(f"Reasoning: {'; '.join(rec['reasoning'])}")
        
    except Exception as e:
        print(f"Error in comprehensive calculation: {e}") 