import React, { useState, useEffect } from 'react';
import axios from 'axios';
import OpportunityCard from '../components/OpportunityCard';
import betIntelLogo from '../assets/images/betintel-logo.png';

const Dashboard = () => {
  const [evData, setEvData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [nextRefresh, setNextRefresh] = useState(180); // 3 minutes in seconds

  const fetchEVData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('/api/future-games-with-ev?limit=10');
      setEvData(response.data);
      setLastUpdated(new Date());
      setNextRefresh(180); // Reset countdown
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
    const fetchInterval = setInterval(fetchEVData, 180000);
    
    // Set up countdown timer that updates every second
    const countdownInterval = setInterval(() => {
      setNextRefresh(prev => {
        if (prev <= 1) {
          return 180; // Reset when it reaches 0
        }
        return prev - 1;
      });
    }, 1000);
    
    return () => {
      clearInterval(fetchInterval);
      clearInterval(countdownInterval);
    };
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

  const formatCountdown = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const getEVClass = (ev) => {
    if (ev > 0) return 'ev-positive';
    if (ev > -2) return 'ev-neutral';
    return 'ev-negative';
  };

  const getEVIndicator = (ev) => {
    if (ev > 2) {
      return { text: '🔥 HOT', class: 'bg-danger text-white' };
    } else if (ev > 0) {
      return { text: '✅ SAFE', class: 'bg-success text-white' };
    } else if (ev > -2) {
      return { text: '⚠️ CAUTION', class: 'bg-warning text-dark' };
    } else {
      return { text: '❌ AVOID', class: 'bg-secondary text-white' };
    }
  };

  const getBestEV = () => {
    if (!evData?.events || evData.events.length === 0) return 0;
    return Math.max(...evData.events.map(event => event.summary?.best_available_ev || -100));
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
      <div className="row mb-4 align-items-center">
        <div className="col-lg-6">
          <div className="d-flex align-items-center">
            <img 
              src={betIntelLogo} 
              alt="BetIntel Logo" 
              className="me-3"
              style={{ height: '80px', width: 'auto' }}
            />
            <div>
              <h1 className="display-5 fw-bold text-dark mb-1">EV Dashboard</h1>
              <p className="lead text-muted mb-0">
                Real-time Expected Value opportunities across sportsbooks and P2P exchanges
              </p>
            </div>
          </div>
        </div>
        <div className="col-lg-6">
          <div className="d-flex align-items-center justify-content-lg-end gap-4 flex-wrap">
            {/* Best EV Available */}
            {evData && (
              <div className="text-center">
                <div className="h4 fw-bold text-success mb-0">
                  {getBestEV() >= 0 ? '+' : ''}{getBestEV().toFixed(1)}%
                </div>
                <small className="text-muted">Best EV Available</small>
              </div>
            )}
            
            {/* Next Refresh */}
            {evData && (
              <div className="text-center">
                <div className="h4 fw-bold text-info mb-0">
                  <i className="fas fa-clock me-1"></i>
                  {formatCountdown(nextRefresh)}
                </div>
                <small className="text-muted">Next Refresh</small>
              </div>
            )}
            
            {/* Refresh Button */}
            <div className="text-center">
              <button
                onClick={fetchEVData}
                disabled={loading}
                className="btn btn-primary"
              >
                <i className={`fas fa-sync ${loading ? 'spin' : ''} me-2`}></i>
                {loading ? 'Refreshing...' : 'Refresh Data'}
              </button>
              {lastUpdated && (
                <small className="d-block text-muted mt-1">
                  Last updated: {lastUpdated.toLocaleTimeString()}
                </small>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* EV Opportunities Grid using OpportunityCard */}
      {evData?.events && evData.events.length > 0 ? (
        <>
          {/* P2P Calculation Explanation */}
          <div className="alert alert-warning border-warning bg-warning bg-opacity-10 mb-4" role="alert">
            <div className="d-flex align-items-center">
              <i className="fas fa-calculator me-3 text-warning"></i>
              <div>
                <h6 className="alert-heading mb-1 text-dark fw-bold">P2P Calculation Method</h6>
                <p className="mb-0 text-dark">
                  P2P target based on Pinnacle no-vig + 2% fee + 2.5% buffer
                </p>
              </div>
            </div>
          </div>
          
          <div className="row g-4">
            {evData.events
              .sort((a, b) => (b.summary?.best_available_ev || -100) - (a.summary?.best_available_ev || -100))
              .map((event, index) => (
              <div key={index} className="col-lg-6 col-xl-4">
                <OpportunityCard
                  event={event}
                  formatOdds={formatOdds}
                  formatTime={formatTime}
                  getEVClass={getEVClass}
                  getEVIndicator={getEVIndicator}
                />
              </div>
            ))}
          </div>
        </>
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
          <h6 className="alert-heading">
            <i className="fas fa-info-circle me-2"></i>
            Methodology
          </h6>
          <p className="mb-0">{evData.methodology.explanation}</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 