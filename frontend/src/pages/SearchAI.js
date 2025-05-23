import React from 'react';

const SearchAI = () => {
  return (
    <div className="container-fluid py-5">
      <div className="text-center py-5">
        <div className="display-1 mb-4">🤖</div>
        <h1 className="display-4 fw-bold text-dark mb-4">AI Search & Analysis</h1>
        <p className="lead text-muted mb-5 mx-auto" style={{maxWidth: '600px'}}>
          Advanced AI-powered search and analysis tools for betting intelligence. 
          This feature will include natural language queries, advanced filtering, 
          and AI-driven insights across all available betting data.
        </p>
        
        <div className="card border-primary mx-auto mb-5" style={{maxWidth: '800px'}}>
          <div className="card-body bg-primary bg-opacity-10">
            <h5 className="card-title text-primary fw-semibold mb-3">Coming Soon Features:</h5>
            <div className="row g-3">
              <div className="col-md-6">
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-check-circle text-primary me-2"></i>
                  <span className="text-primary">Natural language bet queries</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-check-circle text-primary me-2"></i>
                  <span className="text-primary">AI-powered opportunity detection</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-check-circle text-primary me-2"></i>
                  <span className="text-primary">Predictive analytics</span>
                </div>
              </div>
              <div className="col-md-6">
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-check-circle text-primary me-2"></i>
                  <span className="text-primary">Advanced filtering & sorting</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-check-circle text-primary me-2"></i>
                  <span className="text-primary">Bayesian probability models</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <i className="fas fa-check-circle text-primary me-2"></i>
                  <span className="text-primary">Monte Carlo simulations</span>
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
            <i className="fas fa-tools me-2"></i>Feature in Development
          </button>
          <p className="small text-muted mt-3">
            This page will be implemented in future phases of the project.
          </p>
        </div>
      </div>
    </div>
  );
};

export default SearchAI; 