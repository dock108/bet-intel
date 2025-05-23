import React from 'react';

const Education = () => {
  return (
    <div className="container-fluid py-5">
      <div className="text-center py-5">
        <div className="display-1 mb-4">📚</div>
        <h1 className="display-4 fw-bold text-dark mb-4">Education Center</h1>
        <p className="lead text-muted mb-5 mx-auto" style={{maxWidth: '600px'}}>
          Comprehensive educational resources about peer-to-peer betting, 
          expected value calculations, and advanced betting strategies.
        </p>
        
        <div className="card border-success mx-auto mb-5" style={{maxWidth: '800px'}}>
          <div className="card-body bg-success bg-opacity-10">
            <h5 className="card-title text-success fw-semibold mb-3">Planned Educational Content:</h5>
            <div className="row g-3">
              <div className="col-md-6">
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-graduation-cap text-success me-2"></i>
                  <span className="text-success">P2P Betting Fundamentals</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-graduation-cap text-success me-2"></i>
                  <span className="text-success">Expected Value Calculations</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-graduation-cap text-success me-2"></i>
                  <span className="text-success">Bankroll Management</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-graduation-cap text-success me-2"></i>
                  <span className="text-success">Risk Assessment</span>
                </div>
              </div>
              <div className="col-md-6">
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-graduation-cap text-success me-2"></i>
                  <span className="text-success">Market Analysis Techniques</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-graduation-cap text-success me-2"></i>
                  <span className="text-success">Probability Theory Basics</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-graduation-cap text-success me-2"></i>
                  <span className="text-success">Advanced Statistical Models</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-graduation-cap text-success me-2"></i>
                  <span className="text-success">Interactive Tutorials</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-4">
          <button 
            disabled 
            className="btn btn-secondary btn-lg"
          >
            <i className="fas fa-book-open me-2"></i>Content Coming Soon
          </button>
          <p className="small text-muted mt-3">
            Educational materials will be added in upcoming releases.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Education; 