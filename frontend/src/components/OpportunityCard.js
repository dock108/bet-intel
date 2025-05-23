import React from 'react';

const OpportunityCard = ({ event, formatOdds, formatTime, getEVClass, getEVIndicator }) => {
  
  // Helper function to get descriptive outcome labels - simplified approach
  const getOutcomeLabel = (outcomeKey, event) => {
    // Map the API's outcome keys to descriptive labels
    if (outcomeKey === 'outcome_A') {
      return `${event.home_team} Win`;
    } else if (outcomeKey === 'outcome_B') {
      return `${event.away_team} Win`;
    } else if (outcomeKey === 'outcome_C') {
      return 'Draw';
    }
    
    // For other outcome types (spreads, totals, etc.)
    if (outcomeKey === 'spreads') {
      return 'Spreads';
    } else if (outcomeKey === 'totals') {
      return 'Totals';
    }
    
    // Fallback
    return outcomeKey.replace(/_/g, ' ').toUpperCase();
  };

  // Convert American odds to decimal for calculations
  const oddsToDecimal = (americanOdds) => {
    if (americanOdds > 0) {
      return (americanOdds / 100) + 1;
    } else {
      return (100 / Math.abs(americanOdds)) + 1;
    }
  };

  // Convert decimal odds back to American
  const decimalToAmerican = (decimal) => {
    if (decimal >= 2) {
      return Math.round((decimal - 1) * 100);
    } else {
      return Math.round(-100 / (decimal - 1));
    }
  };

  // Helper function to calculate P2P fee-adjusted odds and EV
  const calculateP2PFeeAdjustment = (originalOdds, originalEV) => {
    const decimalOdds = oddsToDecimal(originalOdds);
    
    // Apply 2% fee by reducing the effective payout
    // For positive odds: reduce the profit by 2%
    // For negative odds: increase the required stake by 2%
    const feeAdjustedDecimal = decimalOdds - (decimalOdds - 1) * 0.02;
    const feeAdjustedOdds = decimalToAmerican(feeAdjustedDecimal);
    
    // Recalculate EV - simplified approach (would need more complex calculation for precise EV)
    // This is an approximation - the backend would have the precise calculation
    const evAdjustment = -2; // Rough 2% EV reduction from fees
    const feeAdjustedEV = originalEV + evAdjustment;
    
    return {
      originalOdds,
      feeAdjustedOdds,
      originalEV,
      feeAdjustedEV,
      isActuallyPositive: feeAdjustedEV > 0
    };
  };

  // Helper function to determine if a bookmaker should be treated as P2P
  const isP2PBookmaker = (bookmaker) => {
    // Check the backend flag first
    if (bookmaker.bookmaker.is_p2p) {
      return true;
    }
    
    // Manual override for bookmakers that should be treated as P2P
    const p2pBookmakers = [
      'BetOpenly',
      'betopenly', 
      'NoVig',
      'novig',
      'ProphetX',
      'prophetx'
    ];
    
    return p2pBookmakers.includes(bookmaker.bookmaker.title) || 
           p2pBookmakers.includes(bookmaker.bookmaker.key);
  };

  // Sort bookmakers by best available EV (highest first), but calculate real EV for P2P
  const getSortedBookmakers = () => {
    if (!event.bookmaker_analysis) return [];
    
    return Object.entries(event.bookmaker_analysis)
      .map(([key, bookmaker]) => {
        // Find the best EV for this bookmaker
        let bestEV = Math.max(
          ...Object.values(bookmaker.outcomes || {}).flat().map(bet => bet.ev_percentage || -100)
        );
        
        // If this is a P2P bookmaker, adjust the EV for fees
        if (isP2PBookmaker(bookmaker)) {
          bestEV = bestEV - 2; // Subtract 2% fee from EV
        }
        
        return { key, bookmaker, bestEV, originalBestEV: Math.max(
          ...Object.values(bookmaker.outcomes || {}).flat().map(bet => bet.ev_percentage || -100)
        ) };
      })
      .sort((a, b) => b.bestEV - a.bestEV);
  };

  // Get the actual best line with positive EV
  const getBestLine = () => {
    const sortedBookmakers = getSortedBookmakers();
    const bestBookmaker = sortedBookmakers.find(b => b.bestEV > 0);
    
    if (!bestBookmaker) {
      return { bookmaker: 'No Positive EV Available', ev: 0 };
    }
    
    return {
      bookmaker: bestBookmaker.bookmaker.bookmaker.title,
      ev: bestBookmaker.bestEV
    };
  };

  // Calculate P2P recommendations - either from positive EV or by finding best opportunities
  const getRecommendedP2POdds = () => {
    const sortedBookmakers = getSortedBookmakers();
    
    // First, try to find bookmakers with positive EV
    const positiveEVBookmakers = sortedBookmakers.filter(b => b.bestEV > 0);
    
    if (positiveEVBookmakers.length > 0) {
      // Found positive EV - calculate P2P odds from the best ones
      return calculateP2PFromPositiveEV(positiveEVBookmakers);
    } else {
      // No positive EV - find opportunities that could become positive with better P2P odds
      return calculateP2PFromNegativeEV(sortedBookmakers);
    }
  };

  const calculateP2PFromPositiveEV = (positiveBookmakers) => {
    const opportunities = [];
    
    // Take the best bookmaker and find all its profitable outcomes
    const bestBookmaker = positiveBookmakers[0];
    
    Object.entries(bestBookmaker.bookmaker.outcomes || {}).forEach(([outcomeKey, bets]) => {
      bets.forEach(bet => {
        // Only include bets that have reasonable positive EV
        if (bet.ev_percentage > 0) {
          const outcomeLabel = getOutcomeLabel(outcomeKey, event);
          
          // Apply P2P calculation: remove 2% commission and 2.5% EV buffer
          const adjustedEV = bet.ev_percentage - 2 - 2.5;
          const originalOdds = bet.offered_odds;
          
          // Calculate adjusted odds properly using decimal conversion
          const decimalOdds = oddsToDecimal(originalOdds);
          const adjustedDecimal = decimalOdds * (1 - 0.045); // Reduce by 4.5% total (2% + 2.5%)
          const adjustedOdds = decimalToAmerican(adjustedDecimal);

          if (adjustedEV > 0) { // Only show if still positive after fees
            opportunities.push({
              outcome: outcomeLabel,
              originalOdds: originalOdds,
              adjustedOdds: adjustedOdds,
              originalEV: bet.ev_percentage,
              adjustedEV: adjustedEV,
              type: 'positive'
            });
          }
        }
      });
    });

    return opportunities.length > 0 ? opportunities : null;
  };

  const calculateP2PFromNegativeEV = (sortedBookmakers) => {
    const opportunities = [];
    
    // Take the best bookmaker even if negative EV
    const bestBookmaker = sortedBookmakers[0];
    if (!bestBookmaker) return null;

    // Calculate what P2P odds we'd need to achieve 2.5% positive EV after fees and buffer
    const targetEV = 2.5; // 2.5% positive EV target (between 2% and 3%)
    const feesAndBuffer = 2 + 2.5; // 2% commission + 2.5% buffer
    const requiredBookmakerEV = targetEV + feesAndBuffer; // 7% total

    Object.entries(bestBookmaker.bookmaker.outcomes || {}).forEach(([outcomeKey, bets]) => {
      bets.forEach(bet => {
        const outcomeLabel = getOutcomeLabel(outcomeKey, event);
        const currentEV = bet.ev_percentage;
        const evDifference = requiredBookmakerEV - currentEV;
        
        // Only show if the required improvement is reasonable (less than 50% odds improvement needed)
        if (evDifference < 50) {
          // Estimate required odds improvement
          const originalOdds = bet.offered_odds;
          const decimalOdds = oddsToDecimal(originalOdds);
          const improvedDecimal = decimalOdds * (1 + (evDifference / 100));
          const requiredP2POdds = decimalToAmerican(improvedDecimal);

          opportunities.push({
            outcome: outcomeLabel,
            originalOdds: originalOdds,
            adjustedOdds: requiredP2POdds,
            originalEV: currentEV,
            adjustedEV: targetEV,
            type: 'needed',
            requiredImprovement: evDifference
          });
        }
      });
    });

    return opportunities.length > 0 ? opportunities : null;
  };

  const recommendedP2P = getRecommendedP2POdds();
  const bestLine = getBestLine();
  const sortedBookmakers = getSortedBookmakers();

  return (
    <div className="card h-100 card-hover position-relative">
      {/* EV Indicator Badge */}
      {event.summary && (
        <div className="position-absolute top-0 end-0 mt-2 me-2">
          <span className={`badge ${getEVIndicator(event.summary.best_available_ev).class} fs-6`}>
            {getEVIndicator(event.summary.best_available_ev).text}
          </span>
        </div>
      )}

      <div className="card-body">
        {/* Event Header */}
        <div className="mb-3">
          <h5 className="card-title fw-bold">
            {event.sport?.includes('baseball') ? '⚾' : '🏈'} {event.home_team} vs {event.away_team}
          </h5>
          <p className="card-text text-muted small">
            <i className="fas fa-calendar me-1"></i>
            Sport: {event.sport?.replace(/_/g, ' ').toUpperCase()} • {formatTime(event.commence_time)}
          </p>
        </div>

        {/* Recommended P2P Bet Section */}
        {recommendedP2P && recommendedP2P.length > 0 ? (
          <div className={`border rounded p-3 mb-3 ${
            recommendedP2P[0].type === 'positive' 
              ? 'border-success bg-success bg-opacity-10' 
              : 'border-info bg-info bg-opacity-10'
          }`}>
            <h6 className={`fw-bold mb-2 ${
              recommendedP2P[0].type === 'positive' ? 'text-success' : 'text-info'
            }`}>
              <i className="fas fa-trophy me-1"></i>
              {recommendedP2P[0].type === 'positive' ? '🥇 Recommended P2P Bets' : '💡 P2P Opportunities to Create'}
            </h6>
            
            {/* Display multiple outcomes */}
            {recommendedP2P.map((opportunity, index) => (
              <div key={index} className={`${index > 0 ? 'border-top pt-2 mt-2' : ''}`}>
                <div className="mb-2">
                  <strong>{opportunity.outcome}</strong>
                </div>
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <span className="small text-muted">
                    {opportunity.type === 'positive' ? 'Odds after fees & buffer:' : 'P2P odds needed:'}
                  </span>
                  <span className={`fw-bold fs-5 ${
                    opportunity.type === 'positive' ? 'text-success' : 'text-info'
                  }`}>
                    {formatOdds(opportunity.adjustedOdds)}
                  </span>
                </div>
                <div className="d-flex justify-content-between align-items-center">
                  <span className="small text-muted">Expected EV:</span>
                  <span className={`fw-bold ${
                    opportunity.type === 'positive' ? 'text-success' : 'text-info'
                  }`}>
                    {opportunity.adjustedEV.toFixed(1)}%
                  </span>
                </div>
                {opportunity.type === 'positive' && (
                  <div className="d-flex justify-content-between align-items-center mt-1">
                    <span className="small text-muted">Original odds:</span>
                    <span className="small text-muted">
                      {formatOdds(opportunity.originalOdds)} ({opportunity.originalEV.toFixed(1)}% EV)
                    </span>
                  </div>
                )}
              </div>
            ))}
            
            {recommendedP2P[0].type === 'needed' && (
              <div className="alert alert-info py-2 mb-3 mt-3">
                <small>
                  <i className="fas fa-lightbulb me-1"></i>
                  <strong>Create these opportunities:</strong> Post these bets on P2P exchanges to see if anyone accepts these improved odds.
                </small>
              </div>
            )}
            
            {/* Affiliate Link Placeholders */}
            <div className="d-grid gap-2 mt-3">
              <button className={`btn btn-sm ${
                recommendedP2P[0].type === 'positive' ? 'btn-success' : 'btn-info'
              }`}>
                <i className="fas fa-external-link-alt me-1"></i>
                {recommendedP2P[0].type === 'positive' 
                  ? 'Place Bets on [P2P Exchange Placeholder]'
                  : 'Create Bets on [P2P Exchange Placeholder]'
                }
              </button>
              <button className={`btn btn-outline-${
                recommendedP2P[0].type === 'positive' ? 'success' : 'info'
              } btn-sm`}>
                <i className="fas fa-handshake me-1"></i>
                View Alternative P2P Options
              </button>
            </div>
          </div>
        ) : (
          <div className="border border-warning rounded p-3 mb-3 bg-warning bg-opacity-10">
            <h6 className="text-warning fw-bold mb-2">
              <i className="fas fa-exclamation-triangle me-1"></i>
              No Opportunities Available
            </h6>
            <p className="small text-muted mb-0">
              Unable to calculate profitable P2P opportunities at this time.
            </p>
          </div>
        )}

        {/* Best Line Summary */}
        <div className="bg-light rounded p-3 mb-3">
          <div className="d-flex justify-content-between align-items-center">
            <small className="text-muted">Best Line Available:</small>
            <span className="fw-bold text-primary">
              {bestLine.bookmaker}
            </span>
          </div>
          <div className="d-flex justify-content-between align-items-center mt-1">
            <small className="text-muted">Best EV:</small>
            <span className={`fw-bold ${getEVClass(bestLine.ev)}`}>
              {bestLine.ev > 0 ? `+${bestLine.ev.toFixed(2)}%` : 'No Positive EV'}
            </span>
          </div>
          {event.summary && (
            <div className="d-flex justify-content-between align-items-center mt-1">
              <small className="text-muted">Positive Opportunities:</small>
              <span className="fw-bold text-success">
                {event.summary.positive_ev_count || 0}
              </span>
            </div>
          )}
        </div>

        {/* Sorted Bookmaker Analysis */}
        <div>
          <h6 className="text-muted mb-2">
            <i className="fas fa-chart-line me-1"></i>
            📊 Bookmaker Odds Analysis (sorted by EV):
          </h6>
          
          {sortedBookmakers.slice(0, 3).map(({ key, bookmaker, bestEV, originalBestEV }) => (
            <div key={key} className={`border-start border-3 ps-3 mb-3 ${bestEV > 0 ? 'border-success' : 'border-secondary'}`}>
              <div className="d-flex justify-content-between align-items-center mb-1">
                <span className={`fw-semibold ${isP2PBookmaker(bookmaker) ? 'text-p2p' : 'text-primary'}`}>
                  {bestEV > 0 ? '✅' : '❌'} {bookmaker.bookmaker.title}
                  {isP2PBookmaker(bookmaker) && <span className="badge bg-secondary ms-1">P2P</span>}
                </span>
                <span className={`badge ${bestEV > 0 ? 'bg-success' : 'bg-secondary'}`}>
                  {bestEV > 0 ? '+' : ''}{bestEV.toFixed(2)}% EV
                  {isP2PBookmaker(bookmaker) && (
                    <small className="ms-1">(after fees)</small>
                  )}
                </span>
              </div>
              
              {/* Show P2P fee explanation if this is a P2P bookmaker with originally positive EV */}
              {isP2PBookmaker(bookmaker) && originalBestEV > 0 && bestEV <= 0 && (
                <div className="alert alert-warning py-1 px-2 mb-2 small">
                  <i className="fas fa-exclamation-triangle me-1"></i>
                  <strong>P2P Fee Impact:</strong> Originally +{originalBestEV.toFixed(2)}% EV, but negative after 2% fees
                </div>
              )}
              
              {Object.entries(bookmaker.outcomes || {}).map(([outcomeKey, bets]) => {
                return bets.slice(0, 2).map((bet, betIndex) => {
                  const outcomeLabel = getOutcomeLabel(outcomeKey, event);
                  
                  // Calculate P2P adjustments if this is a P2P bookmaker
                  const isP2P = isP2PBookmaker(bookmaker);
                  const p2pAdjustment = isP2P ? calculateP2PFeeAdjustment(bet.offered_odds, bet.ev_percentage) : null;
                  
                  return (
                    <div key={`${outcomeKey}-${betIndex}`} className="small mt-1">
                      <div className="d-flex justify-content-between">
                        <span className="text-muted">
                          • {outcomeLabel}: {formatOdds(bet.offered_odds)}
                          {isP2P && (
                            <span className="text-warning ms-1">(before fees)</span>
                          )}
                        </span>
                        <span className={getEVClass(bet.ev_percentage)}>
                          {bet.ev_percentage > 0 ? '+' : ''}{bet.ev_percentage.toFixed(2)}%
                        </span>
                      </div>
                      
                      {/* Show P2P fee-adjusted information */}
                      {isP2P && p2pAdjustment && (
                        <div className="d-flex justify-content-between mt-1 ps-2">
                          <span className="text-muted small">
                            └ After 2% fees: {formatOdds(p2pAdjustment.feeAdjustedOdds)}
                          </span>
                          <span className={`small ${getEVClass(p2pAdjustment.feeAdjustedEV)}`}>
                            {p2pAdjustment.feeAdjustedEV > 0 ? '+' : ''}{p2pAdjustment.feeAdjustedEV.toFixed(2)}%
                          </span>
                        </div>
                      )}
                    </div>
                  );
                });
              })}
            </div>
          ))}
          
          {sortedBookmakers.length > 3 && (
            <div className="text-center">
              <button className="btn btn-outline-secondary btn-sm">
                <i className="fas fa-plus me-1"></i>
                Show {sortedBookmakers.length - 3} more bookmakers
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OpportunityCard;