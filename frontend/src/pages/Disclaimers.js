import React from 'react';

const Disclaimers = () => {
  return (
    <div className="container-fluid py-5">
      <div className="text-center py-5">
        <div className="display-1 mb-4">⚖️</div>
        <h1 className="display-4 fw-bold text-dark mb-4">Legal Disclaimers</h1>
        <p className="lead text-muted mb-5 mx-auto" style={{maxWidth: '600px'}}>
          Important legal information, terms of use, and disclaimers 
          regarding the use of this betting intelligence platform.
        </p>
        
        <div className="alert alert-warning mx-auto mb-4" style={{maxWidth: '900px'}}>
          <h5 className="alert-heading fw-bold">Important Notice</h5>
          <div className="text-start">
            <p className="mb-3">
              <strong><i className="fas fa-exclamation-triangle me-2"></i>Educational Purpose Only:</strong> This platform is designed for educational 
              and informational purposes only. All data, calculations, and recommendations should not 
              be considered as financial or gambling advice.
            </p>
            <p className="mb-3">
              <strong><i className="fas fa-target me-2"></i>No Guarantee of Accuracy:</strong> While we strive to provide accurate data 
              and calculations, we cannot guarantee the accuracy, completeness, or timeliness of any 
              information provided.
            </p>
            <p className="mb-3">
              <strong><i className="fas fa-dollar-sign me-2"></i>Gambling Risks:</strong> Gambling involves significant financial risk. 
              Never bet more than you can afford to lose. Please gamble responsibly.
            </p>
            <p className="mb-0">
              <strong><i className="fas fa-map-marker-alt me-2"></i>Legal Compliance:</strong> Users are responsible for ensuring their use 
              of this platform complies with all applicable local, state, and federal laws.
            </p>
          </div>
        </div>

        <div className="alert alert-danger mx-auto mb-5" style={{maxWidth: '900px'}}>
          <h5 className="alert-heading fw-bold">Planned Legal Documentation:</h5>
          <div className="row g-3">
            <div className="col-md-6">
              <div className="d-flex align-items-center mb-2">
                <i className="fas fa-file-contract text-danger me-2"></i>
                <span className="text-danger">Terms of Service</span>
              </div>
              <div className="d-flex align-items-center mb-2">
                <i className="fas fa-file-contract text-danger me-2"></i>
                <span className="text-danger">Privacy Policy</span>
              </div>
              <div className="d-flex align-items-center mb-2">
                <i className="fas fa-file-contract text-danger me-2"></i>
                <span className="text-danger">Data Usage Policy</span>
              </div>
            </div>
            <div className="col-md-6">
              <div className="d-flex align-items-center mb-2">
                <i className="fas fa-file-contract text-danger me-2"></i>
                <span className="text-danger">Liability Limitations</span>
              </div>
              <div className="d-flex align-items-center mb-2">
                <i className="fas fa-file-contract text-danger me-2"></i>
                <span className="text-danger">Responsible Gambling Resources</span>
              </div>
              <div className="d-flex align-items-center mb-2">
                <i className="fas fa-file-contract text-danger me-2"></i>
                <span className="text-danger">Jurisdiction-Specific Notices</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-4">
          <button 
            disabled 
            className="btn btn-secondary btn-lg"
          >
            <i className="fas fa-gavel me-2"></i>Full Legal Documentation Coming Soon
          </button>
          <p className="small text-muted mt-3">
            Comprehensive legal documentation will be added before public release.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Disclaimers; 