import React from 'react';

const OpportunityCard = ({ event, formatOdds, formatTime, getEVClass, getEVIndicator }) => {
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
            {event.home_team} vs {event.away_team}
          </h5>
          <p className="card-text text-muted small">
            <i className="fas fa-calendar me-1"></i>
            Sport: {event.sport} • {formatTime(event.commence_time)}
          </p>
        </div>

        {/* Best EV Summary */}
        {event.summary && (
          <div className="bg-light rounded p-3 mb-3">
            <div className="d-flex justify-content-between align-items-center">
              <small className="text-muted">Best Available EV:</small>
              <span className={`fw-bold ${getEVClass(event.summary.best_available_ev)}`}>
                {event.summary.best_available_ev.toFixed(2)}%
              </span>
            </div>
            <div className="d-flex justify-content-between align-items-center mt-1">
              <small className="text-muted">EV in Dollars (per $100):</small>
              <span className={`fw-bold ${getEVClass(event.summary.best_available_ev)}`}>
                ${event.summary.best_available_ev.toFixed(2)}
              </span>
            </div>
            <div className="d-flex justify-content-between align-items-center mt-1">
              <small className="text-muted">Positive EV Count:</small>
              <span className="fw-bold text-success">
                {event.summary.positive_ev_count}
              </span>
            </div>
          </div>
        )}

        {/* Recommended Odds Section */}
        <div className="mb-3">
          <h6 className="text-muted mb-2">
            <i className="fas fa-star me-1"></i>
            Recommended Opportunities:
          </h6>
          <div className="border-start border-3 border-warning ps-3">
            <div className="small">
              <div className="d-flex justify-content-between">
                <span className="text-muted">Best Line:</span>
                <span className="fw-semibold text-primary">
                  {event.bookmaker_analysis && Object.keys(event.bookmaker_analysis).length > 0 
                    ? Object.keys(event.bookmaker_analysis)[0] 
                    : 'N/A'}
                </span>
              </div>
              <div className="d-flex justify-content-between mt-1">
                <span className="text-muted">Recommended Stake:</span>
                <span className="fw-semibold text-success">2-5% of bankroll</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bookmaker Analysis */}
        <div>
          <h6 className="text-muted mb-2">
            <i className="fas fa-chart-line me-1"></i>
            Bookmaker Analysis:
          </h6>
          {Object.entries(event.bookmaker_analysis || {}).slice(0, 3).map(([bookmakerKey, bookmaker]) => (
            <div key={bookmakerKey} className="border-start border-3 border-secondary ps-3 mb-2">
              <div className="d-flex justify-content-between align-items-center">
                <small className={`fw-semibold ${bookmaker.bookmaker.is_p2p ? 'text-p2p' : 'text-primary'}`}>
                  {bookmaker.bookmaker.title}
                  {bookmaker.bookmaker.is_p2p && <span className="badge bg-secondary ms-1">P2P</span>}
                </small>
              </div>
              {Object.entries(bookmaker.outcomes || {}).map(([outcome, data]) => (
                data.slice(0, 2).map((bet, betIndex) => (
                  <div key={`${outcome}-${betIndex}`} className="d-flex justify-content-between small mt-1">
                    <span className="text-muted">{outcome}: {formatOdds(bet.offered_odds)}</span>
                    <span className={getEVClass(bet.ev_percentage)}>
                      {bet.ev_percentage.toFixed(2)}%
                    </span>
                  </div>
                ))
              ))}
            </div>
          ))}
          
          {Object.keys(event.bookmaker_analysis || {}).length > 3 && (
            <div className="text-center text-muted small pt-2">
              <i className="fas fa-plus me-1"></i>
              {Object.keys(event.bookmaker_analysis).length - 3} more bookmakers
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OpportunityCard; 