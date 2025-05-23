import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [evData, setEvData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchEVData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('/api/future-games-with-ev?limit=10');
      setEvData(response.data);
      setLastUpdated(new Date());
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch data');
      console.error('Error fetching EV data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEVData();
    // Set up auto-refresh every 3 minutes
    const interval = setInterval(fetchEVData, 180000);
    return () => clearInterval(interval);
  }, []);

  const formatOdds = (odds) => {
    if (odds > 0) return `+${odds}`;
    return odds.toString();
  };

  const formatTime = (timeString) => {
    try {
      const date = new Date(timeString);
      return date.toLocaleString();
    } catch {
      return timeString;
    }
  };

  const getEVClass = (ev) => {
    if (ev > 0) return 'ev-positive';
    if (ev > -2) return 'ev-neutral';
    return 'ev-negative';
  };

  if (loading && !evData) {
    return (
      <div className="container-fluid py-4">
        <div className="text-center py-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3 text-muted">Loading EV opportunities...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container-fluid py-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error Loading Data</h4>
          <p className="mb-3">{error}</p>
          <button
            onClick={fetchEVData}
            className="btn btn-danger"
          >
            <i className="fas fa-redo me-2"></i>Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid py-4">
      {/* Header */}
      <div className="row mb-4">
        <div className="col-lg-8">
          <h1 className="display-5 fw-bold text-dark">EV Dashboard</h1>
          <p className="lead text-muted">
            Real-time Expected Value opportunities across sportsbooks and P2P exchanges
          </p>
        </div>
        <div className="col-lg-4 text-lg-end">
          <button
            onClick={fetchEVData}
            disabled={loading}
            className="btn btn-primary"
          >
            <i className={`fas fa-sync ${loading ? 'spin' : ''} me-2`}></i>
            {loading ? 'Refreshing...' : 'Refresh Data'}
          </button>
          {lastUpdated && (
            <small className="d-block text-muted mt-2">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </small>
          )}
        </div>
      </div>

      {/* Stats Bar */}
      {evData && (
        <div className="card mb-4">
          <div className="card-body">
            <div className="row text-center">
              <div className="col-md-4">
                <h3 className="text-primary fw-bold">{evData.total}</h3>
                <small className="text-muted">Total Events</small>
              </div>
              <div className="col-md-4">
                <h3 className="text-success fw-bold">
                  {evData.methodology?.core_bookmakers ? Object.keys(evData.methodology.core_bookmakers).length : 6}
                </h3>
                <small className="text-muted">Core Bookmakers</small>
              </div>
              <div className="col-md-4">
                <h3 className="text-p2p fw-bold">
                  {evData.methodology?.calculation_method || '7-Step No-Vig'}
                </h3>
                <small className="text-muted">EV Method</small>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* EV Opportunities Grid */}
      {evData?.events && evData.events.length > 0 ? (
        <div className="row g-4">
          {evData.events.map((event, index) => (
            <div key={index} className="col-lg-6 col-xl-4">
              <div className="card h-100 card-hover">
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
                        <small className="text-muted">Positive EV Count:</small>
                        <span className="fw-bold text-success">
                          {event.summary.positive_ev_count}
                        </span>
                      </div>
                    </div>
                  )}

                  {/* Bookmaker Analysis */}
                  <div>
                    <h6 className="text-muted mb-2">Bookmaker Analysis:</h6>
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
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-5">
          <div className="display-1 mb-4">📊</div>
          <h3 className="fw-bold text-dark mb-2">No EV Opportunities Found</h3>
          <p className="text-muted mb-4">Check back later for new opportunities.</p>
          <button
            onClick={fetchEVData}
            className="btn btn-primary btn-lg"
          >
            <i className="fas fa-sync me-2"></i>Refresh Data
          </button>
        </div>
      )}

      {/* Methodology Info */}
      {evData?.methodology && (
        <div className="alert alert-info mt-4" role="alert">
          <h6 className="alert-heading">Methodology</h6>
          <p className="mb-0">{evData.methodology.explanation}</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 