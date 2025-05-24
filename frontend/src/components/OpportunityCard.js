import React, { useState } from 'react';

const OpportunityCard = ({ event, formatOdds, formatTime, getEVClass, getEVIndicator }) => {
  const [showDetails, setShowDetails] = useState(false);
  
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
    const feeAdjustedDecimal = decimalOdds - (decimalOdds - 1) * 0.02;
    const feeAdjustedOdds = decimalToAmerican(feeAdjustedDecimal);
    const evAdjustment = -2;
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
    if (bookmaker.bookmaker.is_p2p) {
      return true;
    }
    
    const p2pBookmakers = [
      'BetOpenly', 'betopenly', 'Novig', 'novig', 'ProphetX', 'prophetx'
    ];
    
    return p2pBookmakers.includes(bookmaker.bookmaker.title) || 
           p2pBookmakers.includes(bookmaker.bookmaker.key);
  };

  // Get P2P recommendations using Pinnacle as source of truth
  const getP2PRecommendations = () => {
    if (!event.bookmaker_analysis) return [];
    
    const outcomeMap = new Map(); // For P2P calculations based on Pinnacle
    const bestOddsMap = new Map(); // For display - best odds from any bookmaker
    const targetEV = 2.5; // Target 2.5% EV buffer
    const p2pFee = 2; // 2% P2P commission
    const totalBuffer = p2pFee + targetEV; // 4.5% total buffer needed
    
    // Find the best odds across ALL bookmakers for display
    Object.entries(event.bookmaker_analysis).forEach(([key, bookmaker]) => {
      Object.entries(bookmaker.outcomes || {}).forEach(([outcomeKey, bets]) => {
        bets.forEach(bet => {
          if (bet.offered_odds) {
            const outcomeLabel = getOutcomeLabel(outcomeKey, event);
            
            // Keep track of best odds for display
            if (!bestOddsMap.has(outcomeLabel) || bestOddsMap.get(outcomeLabel).currentEV < bet.ev_percentage) {
              bestOddsMap.set(outcomeLabel, {
                outcome: outcomeLabel,
                currentOdds: bet.offered_odds,
                currentEV: bet.ev_percentage,
                bookmaker: bookmaker.bookmaker.title
              });
            }
          }
        });
      });
    });
    
    // First, try to find Pinnacle as our source of truth for P2P calculations
    let pinnacleBookmaker = null;
    Object.entries(event.bookmaker_analysis).forEach(([key, bookmaker]) => {
      if (bookmaker.bookmaker.title === 'Pinnacle' && !isP2PBookmaker(bookmaker)) {
        pinnacleBookmaker = bookmaker;
      }
    });
    
    if (pinnacleBookmaker) {
      console.log('Using Pinnacle as source of truth for P2P calculations');
      
      // Use Pinnacle's odds as baseline for P2P calculations
      Object.entries(pinnacleBookmaker.outcomes || {}).forEach(([outcomeKey, bets]) => {
        bets.forEach(bet => {
          if (bet.offered_odds) {
            const outcomeLabel = getOutcomeLabel(outcomeKey, event);
            
            outcomeMap.set(outcomeLabel, {
              outcome: outcomeLabel,
              pinnacleOdds: bet.offered_odds,
              pinnacleEV: bet.ev_percentage,
              isFromPinnacle: true
            });
          }
        });
      });
    } else {
      console.log('Pinnacle not available, using best non-P2P bookmaker as fallback for P2P calculations');
      
      // Fallback: Find best non-P2P bookmaker for P2P calculations
      Object.entries(event.bookmaker_analysis).forEach(([key, bookmaker]) => {
        if (!isP2PBookmaker(bookmaker)) {
          Object.entries(bookmaker.outcomes || {}).forEach(([outcomeKey, bets]) => {
            bets.forEach(bet => {
              if (bet.offered_odds) {
                const outcomeLabel = getOutcomeLabel(outcomeKey, event);
                
                if (!outcomeMap.has(outcomeLabel) || outcomeMap.get(outcomeLabel).pinnacleEV < bet.ev_percentage) {
                  outcomeMap.set(outcomeLabel, {
                    outcome: outcomeLabel,
                    pinnacleOdds: bet.offered_odds,
                    pinnacleEV: bet.ev_percentage,
                    fallbackBookmaker: bookmaker.bookmaker.title,
                    isFromPinnacle: false
                  });
                }
              }
            });
          });
        }
      });
    }
    
    // Now calculate P2P target odds and combine with best odds for display
    const recommendations = [];
    
    outcomeMap.forEach((p2pBase) => {
      const bestOdds = bestOddsMap.get(p2pBase.outcome);
      if (!bestOdds) return;
      
      // Target is always +4.5% EV (to get +2.5% after 2% P2P fees)
      const targetEVBeforeFees = 4.5; // Always target +4.5% EV
      const pinnacleEV = p2pBase.pinnacleEV;
      
      // Calculate total EV improvement needed from Pinnacle to reach +4.5%
      const totalEVImprovement = targetEVBeforeFees - pinnacleEV;
      
      // Calculate what odds would provide +4.5% EV
      const currentDecimalOdds = oddsToDecimal(p2pBase.pinnacleOdds);
      
      // CORRECTED APPROACH: Use proper EV formula to derive true probability and calculate exact odds
      // Step 1: Calculate true probability from Pinnacle's odds and EV
      const trueProb = (1 + pinnacleEV / 100) / currentDecimalOdds;
      
      // Step 2: Calculate exact odds needed for +4.5% EV using true probability
      const targetDecimalOdds = (1 + targetEVBeforeFees / 100) / trueProb;
      
      // Step 3: Convert to American odds
      const targetP2POdds = decimalToAmerican(targetDecimalOdds);
      
      // Calculate EV improvement from best odds to P2P target
      const evImprovementNeeded = targetEVBeforeFees - bestOdds.currentEV;
      
      console.log(`DEBUG - ${p2pBase.outcome}:`);
      console.log(`  Pinnacle: ${p2pBase.pinnacleOdds} (${pinnacleEV.toFixed(1)}% EV) [calculation base]`);
      console.log(`  Best Available: ${bestOdds.currentOdds} (${bestOdds.currentEV.toFixed(1)}% EV) [display]`);
      console.log(`  Decimal odds: ${currentDecimalOdds.toFixed(4)}`);
      console.log(`  True probability: ${(trueProb * 100).toFixed(2)}%`);
      console.log(`  Target decimal odds: ${targetDecimalOdds.toFixed(4)}`);
      console.log(`  Target P2P odds: ${targetP2POdds}`);
      console.log(`  EV improvement needed (best→target): ${evImprovementNeeded.toFixed(1)}%`);
      
      recommendations.push({
        outcome: bestOdds.outcome,
        currentOdds: bestOdds.currentOdds, // Best odds for display
        currentEV: bestOdds.currentEV, // Best EV for display
        currentBookmaker: bestOdds.bookmaker,
        targetP2POdds: targetP2POdds, // Calculated from Pinnacle to reach +4.5% EV
        finalEV: targetEV,
        isViable: true,
        evImprovementNeeded: evImprovementNeeded, // From best odds to target
        needsImprovement: true,
        isFromPinnacle: p2pBase.isFromPinnacle,
        p2pSource: p2pBase.isFromPinnacle ? 'Pinnacle' : p2pBase.fallbackBookmaker,
        pinnacleEV: pinnacleEV, // For debugging
        targetEVBeforeFees: targetEVBeforeFees // For debugging
      });
    });
    
    // Sort by current EV and return all recommendations
    return recommendations
      .sort((a, b) => b.currentEV - a.currentEV);
  };

  // Get compact recommended bets for display
  const getCompactRecommendations = () => {
    return getP2PRecommendations();
  };

  // Sort bookmakers by best available EV (for details section)
  const getSortedBookmakers = () => {
    if (!event.bookmaker_analysis) return [];
    
    return Object.entries(event.bookmaker_analysis)
      .map(([key, bookmaker]) => {
        let bestEV = Math.max(
          ...Object.values(bookmaker.outcomes || {}).flat().map(bet => bet.ev_percentage || -100)
        );
        
        if (isP2PBookmaker(bookmaker)) {
          bestEV = bestEV - 2;
        }
        
        return { key, bookmaker, bestEV, originalBestEV: Math.max(
          ...Object.values(bookmaker.outcomes || {}).flat().map(bet => bet.ev_percentage || -100)
        ) };
      })
      .sort((a, b) => b.bestEV - a.bestEV);
  };

  // Determine the best P2P exchange based on current odds
  const getBestP2PExchange = () => {
    if (!event.bookmaker_analysis) return 'Novig';
    
    const p2pExchanges = ['BetOpenly', 'ProphetX', 'Novig'];
    let bestExchange = 'Novig'; // Default fallback
    let bestP2PEV = -999;
    
    console.log('=== P2P Exchange Selection Debug ===');
    
    // Look through P2P bookmakers to find the one with best current odds
    Object.entries(event.bookmaker_analysis).forEach(([key, bookmaker]) => {
      console.log(`Checking bookmaker: ${bookmaker.bookmaker.title}, isP2P: ${isP2PBookmaker(bookmaker)}`);
      
      if (isP2PBookmaker(bookmaker)) {
        const exchangeName = bookmaker.bookmaker.title;
        
        // Find this exchange's best EV (already fee-adjusted by API)
        let exchangeBestEV = Math.max(
          ...Object.values(bookmaker.outcomes || {}).flat().map(bet => bet.ev_percentage || -100)
        );
        
        // Debug: Log the comparison
        console.log(`P2P Exchange: "${exchangeName}", Best EV: ${exchangeBestEV}%, Included in list: ${p2pExchanges.includes(exchangeName)}`);
        console.log(`Current Best: ${bestExchange} (${bestP2PEV}%)`);
        
        // If this exchange has better odds than current best, make it recommended
        // For ties, prefer Novig, then BetOpenly, then ProphetX
        if (exchangeBestEV > bestP2PEV && p2pExchanges.includes(exchangeName)) {
          console.log(`✅ New best: ${exchangeName} with ${exchangeBestEV}%`);
          bestP2PEV = exchangeBestEV;
          bestExchange = exchangeName;
        } else if (Math.abs(exchangeBestEV - bestP2PEV) < 0.1 && p2pExchanges.includes(exchangeName)) {
          // Handle near-ties (within 0.1%) - prefer Novig first
          const priorityOrder = { 'Novig': 0, 'BetOpenly': 1, 'ProphetX': 2 };
          
          if (priorityOrder[exchangeName] < priorityOrder[bestExchange]) {
            console.log(`🏆 Tie-breaker: ${exchangeName} wins over ${bestExchange}`);
            bestExchange = exchangeName;
          }
        } else {
          console.log(`❌ ${exchangeName} not selected: EV=${exchangeBestEV}% vs best=${bestP2PEV}%`);
        }
      }
    });
    
    console.log(`🎯 Final P2P recommendation: ${bestExchange}`);
    console.log('=== End P2P Selection Debug ===');
    return bestExchange;
  };

  // Get the other two exchanges (non-recommended)
  const getSecondaryExchanges = () => {
    const allExchanges = ['BetOpenly', 'ProphetX', 'Novig'];
    return allExchanges.filter(exchange => exchange !== recommendedExchange);
  };

  const recommendations = getCompactRecommendations();
  const sortedBookmakers = getSortedBookmakers();
  const bestEV = recommendations.length > 0 ? recommendations[0].currentEV : (event.summary?.best_available_ev || 0);
  const recommendedExchange = getBestP2PExchange();
  const secondaryExchanges = getSecondaryExchanges();
  
  // Determine card color scheme based on best EV - ALL GOLD
  const getCardColorScheme = () => {
    return 'warning'; // Always use warning (gold/yellow) color scheme
  };

  const colorScheme = getCardColorScheme();

  // Only show EV badge for truly positive EV (live opportunities)
  const shouldShowEVBadge = bestEV > 0;

  return (
    <div className={`card h-100 card-hover border-${colorScheme} position-relative`} 
         style={{ minHeight: 'auto' }}>
      
      {/* EV Indicator Badge - Only for positive EV */}
      {shouldShowEVBadge && event.summary && (
        <div className="position-absolute top-0 end-0 mt-2 me-2">
          <span className={`badge ${getEVIndicator(event.summary.best_available_ev).class} fs-6`}>
            {getEVIndicator(event.summary.best_available_ev).text}
          </span>
        </div>
      )}

      <div className="card-body py-3 px-3">
        {/* Compact Header */}
        <div className="mb-3">
          <h6 className="card-title fw-bold mb-1">
            {event.sport?.includes('baseball') ? '⚾' : '🏈'} {event.home_team} vs {event.away_team}
          </h6>
          <small className="text-muted">
            {event.sport?.replace(/_/g, ' ').toUpperCase()} • {formatTime(event.commence_time)}
          </small>
        </div>

        {/* P2P Recommendations Section - More Prominent */}
        {recommendations.length > 0 ? (
          <div className={`border border-${colorScheme} rounded p-3 mb-3 bg-${colorScheme} bg-opacity-10`}>
            <div className="mb-3">
              <h6 className={`fw-bold text-dark mb-0`}>
                🎯 Calculated P2P Opportunities
              </h6>
            </div>
            
            {recommendations.map((rec, index) => (
              <div key={index} className={`${index > 0 ? 'border-top pt-3 mt-3' : ''}`}>
                <div className="mb-2">
                  <span className="fw-bold text-dark">
                    {rec.outcome}
                  </span>
                </div>
                
                <div className="row mb-2">
                  <div className="col-6">
                    <small className="text-muted d-block">Current Best Odds:</small>
                    <span className="fw-bold">{formatOdds(rec.currentOdds)}</span>
                    <small className={`ms-1 ${rec.currentEV >= 0 ? 'text-success' : 'text-danger'}`}>
                      ({rec.currentEV >= 0 ? '+' : ''}{rec.currentEV.toFixed(1)}% EV)
                    </small>
                    <div className="small text-muted">
                      <i className="fas fa-store me-1"></i>
                      {rec.currentBookmaker}
                    </div>
                  </div>
                  <div className="col-6">
                    <small className="text-muted d-block">P2P Odds to Offer:</small>
                    <span className={`fw-bold text-${colorScheme === 'warning' ? 'dark' : colorScheme} fs-5`}>
                      {formatOdds(rec.targetP2POdds)}
                    </span>
                  </div>
                </div>
                
                {rec.needsImprovement && (
                  <div className="alert alert-info py-1 px-2 mb-2">
                    <small>
                      <i className="fas fa-info-circle me-1"></i>
                      EV improvement needed: {rec.evImprovementNeeded.toFixed(1)}%
                    </small>
                  </div>
                )}
              </div>
            ))}
            
            {/* 3 Affiliate Link Options */}
            <div className="mt-3 pt-3 border-top">
              <div className="small text-muted mb-2 fw-bold">
                <i className="fas fa-handshake me-1"></i>
                Choose your preferred P2P exchange to place these bets:
              </div>
              
              <div className="d-grid gap-2">
                <button className="btn btn-dark fw-bold">
                  <i className="fas fa-external-link-alt me-2"></i>
                  🥇 Place on {recommendedExchange} (Recommended)
                </button>
                
                <div className="row">
                  <div className="col-6">
                    <button className="btn btn-outline-dark btn-sm w-100">
                      <i className="fas fa-external-link-alt me-1"></i>
                      {secondaryExchanges[0]}
                    </button>
                  </div>
                  <div className="col-6">
                    <button className="btn btn-outline-dark btn-sm w-100">
                      <i className="fas fa-external-link-alt me-1"></i>
                      {secondaryExchanges[1]}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="border border-warning rounded p-3 mb-3 bg-warning bg-opacity-10">
            <h6 className="text-dark fw-bold mb-2">
              <i className="fas fa-exclamation-triangle me-2"></i>
              No Viable P2P Opportunities
            </h6>
            <p className="small text-muted mb-0">
              Current market conditions don't support profitable P2P opportunities with reasonable odds improvements.
            </p>
          </div>
        )}

        {/* Clear Expandable Details Toggle */}
        <div className="text-center border-top pt-3">
          <button 
            className="btn btn-outline-dark btn-sm w-100 d-flex align-items-center justify-content-center"
            onClick={() => setShowDetails(!showDetails)}
          >
            <i className={`fas fa-chart-line me-2`}></i>
            <span className="fw-bold">
              {showDetails ? 'Hide Detailed Analysis' : 'View Detailed Analysis'}
            </span>
            <i className={`fas fa-chevron-${showDetails ? 'up' : 'down'} ms-2`}></i>
          </button>
        </div>

        {/* Expandable Detailed Analysis Section */}
        {showDetails && (
          <div className="border-top pt-3 mt-3">
            <h6 className="fw-bold text-dark mb-3">
              <i className="fas fa-chart-bar me-2"></i>
              Complete Bookmaker Analysis
            </h6>
            
            {sortedBookmakers.length > 0 ? (
              <div className="row g-2">
                {sortedBookmakers.map((bookmaker, index) => (
                  <div key={index} className="col-12">
                    <div className={`card border-${isP2PBookmaker(bookmaker.bookmaker) ? 'info' : 'secondary'} h-100`}>
                      <div className="card-body py-2 px-3">
                        <div className="d-flex justify-content-between align-items-center mb-2">
                          <h6 className="mb-0 fw-bold">
                            {isP2PBookmaker(bookmaker.bookmaker) ? '🔄 ' : '📊 '}
                            {bookmaker.bookmaker.bookmaker.title}
                          </h6>
                          <span className={`badge ${bookmaker.bestEV >= 0 ? 'bg-success' : 'bg-danger'} text-white`}>
                            {bookmaker.bestEV >= 0 ? '+' : ''}{bookmaker.bestEV.toFixed(1)}% EV
                          </span>
                        </div>
                        
                        {/* Show outcomes for this bookmaker */}
                        <div className="row g-1">
                          {Object.entries(bookmaker.bookmaker.outcomes || {}).map(([outcomeKey, bets]) => 
                            bets.map((bet, betIndex) => (
                              <div key={`${outcomeKey}-${betIndex}`} className="col-md-6">
                                <div className="small border rounded p-2 bg-light">
                                  <div className="fw-bold text-dark">
                                    {getOutcomeLabel(outcomeKey, event)}
                                  </div>
                                  <div className="d-flex justify-content-between">
                                    <span className="fw-bold">{formatOdds(bet.offered_odds)}</span>
                                    <span className={`${bet.ev_percentage >= 0 ? 'text-success' : 'text-danger'}`}>
                                      {bet.ev_percentage >= 0 ? '+' : ''}{bet.ev_percentage.toFixed(1)}%
                                    </span>
                                  </div>
                                  {isP2PBookmaker(bookmaker.bookmaker) && (
                                    <div className="text-muted small">
                                      <i className="fas fa-info-circle me-1"></i>
                                      After 2% P2P fee
                                    </div>
                                  )}
                                </div>
                              </div>
                            ))
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-3">
                <div className="text-muted">
                  <i className="fas fa-info-circle me-2"></i>
                  No detailed bookmaker data available
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default OpportunityCard;