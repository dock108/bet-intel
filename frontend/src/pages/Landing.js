import React from 'react';
import betIntelLogo from '../assets/images/betintel-logo.png';

const Landing = () => {
  return (
    <div className="min-vh-100">
      
      {/* Hero Section */}
      <section className="bg-primary text-white py-5">
        <div className="container">
          <div className="row align-items-center min-vh-75">
            <div className="col-lg-6">
              <div className="mb-4">
                <img 
                  src={betIntelLogo} 
                  alt="BetIntel Logo" 
                  className="mb-3"
                  style={{ height: '80px', width: 'auto' }}
                />
              </div>
              <h1 className="display-4 fw-bold mb-4">
                💡 Smarter Sports Betting Starts Here
              </h1>
              <p className="lead mb-4">
                Real-time +EV bets. Peer-to-peer odds intel. No fluff.
              </p>
              <div className="d-flex gap-3 flex-wrap">
                <a href="/dashboard" className="btn btn-light btn-lg">
                  <i className="fas fa-chart-bar me-2"></i>
                  📊 Try the Free Dashboard
                </a>
                <a href="/education" className="btn btn-outline-light btn-lg">
                  <i className="fas fa-graduation-cap me-2"></i>
                  Learn How It Works
                </a>
              </div>
            </div>
            <div className="col-lg-6 text-center">
              <div className="card border-0 shadow-lg bg-white text-dark">
                <div className="card-body p-4">
                  <h5 className="card-title text-success mb-3">
                    <i className="fas fa-broadcast-tower me-2"></i>
                    Live Dashboard Preview
                  </h5>
                  <div className="row text-center mb-3">
                    <div className="col-4">
                      <div className="h4 text-primary mb-1">47</div>
                      <small className="text-muted">+EV Bets</small>
                    </div>
                    <div className="col-4">
                      <div className="h4 text-success mb-1">+4.2%</div>
                      <small className="text-muted">Best EV</small>
                    </div>
                    <div className="col-4">
                      <div className="h4 text-warning mb-1">12</div>
                      <small className="text-muted">P2P Opportunities</small>
                    </div>
                  </div>
                  <div className="alert alert-success border-success py-2">
                    <small>
                      <i className="fas fa-sync me-1"></i>
                      Updated every 3 minutes • Real-time data
                    </small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* What is Bet Intel Section */}
      <section className="py-5 bg-light">
        <div className="container">
          <div className="row">
            <div className="col-lg-8 mx-auto text-center">
              <h2 className="display-6 fw-bold mb-4">What is Bet Intel?</h2>
              <p className="lead mb-4">
                We're the data layer between you and profitable sports betting. No bets taken, no house edge — just pure information advantage.
              </p>
              
              <div className="row g-4">
                <div className="col-md-6">
                  <div className="card border-0 h-100 shadow-sm">
                    <div className="card-body text-center p-4">
                      <div className="text-primary mb-3">
                        <i className="fas fa-chart-line fa-2x"></i>
                      </div>
                      <h6>📈 Real-Time Odds Analysis</h6>
                      <p className="small text-muted mb-0">Pulls live odds from major sportsbooks & P2P exchanges, calculating true expected value</p>
                    </div>
                  </div>
                </div>
                
                <div className="col-md-6">
                  <div className="card border-0 h-100 shadow-sm">
                    <div className="card-body text-center p-4">
                      <div className="text-success mb-3">
                        <i className="fas fa-target fa-2x"></i>
                      </div>
                      <h6>🎯 Sharp Line Detection</h6>
                      <p className="small text-muted mb-0">Uses Pinnacle and other sharp books to identify fair value and market inefficiencies</p>
                    </div>
                  </div>
                </div>
                
                <div className="col-md-6">
                  <div className="card border-0 h-100 shadow-sm">
                    <div className="card-body text-center p-4">
                      <div className="text-warning mb-3">
                        <i className="fas fa-handshake fa-2x"></i>
                      </div>
                      <h6>🛠️ P2P Strategy Optimization</h6>
                      <p className="small text-muted mb-0">Helps you set intelligent offers on peer-to-peer platforms with mathematical edge</p>
                    </div>
                  </div>
                </div>
                
                <div className="col-md-6">
                  <div className="card border-0 h-100 shadow-sm">
                    <div className="card-body text-center p-4">
                      <div className="text-danger mb-3">
                        <i className="fas fa-ban fa-2x"></i>
                      </div>
                      <h6>❌ Information Only</h6>
                      <p className="small text-muted mb-0">Doesn't take bets or manage funds — just makes you a sharper, more informed bettor</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Free Features Available Now */}
      <section className="py-5">
        <div className="container">
          <div className="row">
            <div className="col-lg-10 mx-auto">
              <div className="text-center mb-5">
                <h2 className="display-6 fw-bold mb-3">Free Features Available Now</h2>
                <p className="lead text-muted">Start using Bet Intel today with our comprehensive free tools</p>
              </div>
              
              <div className="row g-4">
                <div className="col-lg-4">
                  <div className="card border-success h-100">
                    <div className="card-header bg-success text-white d-flex justify-content-between align-items-center">
                      <h6 className="mb-0">
                        <i className="fas fa-chart-bar me-2"></i>
                        Live EV Dashboard
                      </h6>
                      <span className="badge bg-white text-success">FREE</span>
                    </div>
                    <div className="card-body">
                      <p className="card-text">Real-time betting opportunities ranked by expected value, updated every 3 minutes with live data from major sportsbooks.</p>
                      <ul className="list-unstyled small">
                        <li><i className="fas fa-check text-success me-2"></i>47+ live opportunities</li>
                        <li><i className="fas fa-check text-success me-2"></i>EV calculations with transparency</li>
                        <li><i className="fas fa-check text-success me-2"></i>Auto-refresh every 3 minutes</li>
                        <li><i className="fas fa-check text-success me-2"></i>Mobile-responsive design</li>
                      </ul>
                    </div>
                    <div className="card-footer bg-transparent">
                      <a href="/dashboard" className="btn btn-success w-100">
                        <i className="fas fa-external-link-alt me-2"></i>
                        Access Dashboard
                      </a>
                    </div>
                  </div>
                </div>
                
                <div className="col-lg-4">
                  <div className="card border-primary h-100">
                    <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                      <h6 className="mb-0">
                        <i className="fas fa-exchange-alt me-2"></i>
                        Odds Comparisons
                      </h6>
                      <span className="badge bg-white text-primary">FREE</span>
                    </div>
                    <div className="card-body">
                      <p className="card-text">Side-by-side analysis of traditional sportsbooks vs P2P exchanges, with fee-adjusted calculations and profitability warnings.</p>
                      <ul className="list-unstyled small">
                        <li><i className="fas fa-check text-primary me-2"></i>6+ major sportsbooks tracked</li>
                        <li><i className="fas fa-check text-primary me-2"></i>P2P exchange integration</li>
                        <li><i className="fas fa-check text-primary me-2"></i>Fee transparency and warnings</li>
                        <li><i className="fas fa-check text-primary me-2"></i>EV-based sorting and filtering</li>
                      </ul>
                    </div>
                    <div className="card-footer bg-transparent">
                      <a href="/dashboard" className="btn btn-primary w-100">
                        <i className="fas fa-external-link-alt me-2"></i>
                        View Comparisons
                      </a>
                    </div>
                  </div>
                </div>
                
                <div className="col-lg-4">
                  <div className="card border-info h-100">
                    <div className="card-header bg-info text-white d-flex justify-content-between align-items-center">
                      <h6 className="mb-0">
                        <i className="fas fa-graduation-cap me-2"></i>
                        Education Center
                      </h6>
                      <span className="badge bg-white text-info">FREE</span>
                    </div>
                    <div className="card-body">
                      <p className="card-text">Comprehensive guides on P2P betting, expected value calculations, and our 7-step methodology for finding profitable opportunities.</p>
                      <ul className="list-unstyled small">
                        <li><i className="fas fa-check text-info me-2"></i>P2P betting fundamentals</li>
                        <li><i className="fas fa-check text-info me-2"></i>EV calculation examples</li>
                        <li><i className="fas fa-check text-info me-2"></i>Step-by-step bet posting guide</li>
                        <li><i className="fas fa-check text-info me-2"></i>Interactive learning tools</li>
                      </ul>
                    </div>
                    <div className="card-footer bg-transparent">
                      <a href="/education" className="btn btn-info w-100">
                        <i className="fas fa-external-link-alt me-2"></i>
                        Start Learning
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Premium Features Coming Soon */}
      <section className="py-5 bg-light">
        <div className="container">
          <div className="row">
            <div className="col-lg-10 mx-auto">
              <div className="text-center mb-5">
                <h2 className="display-6 fw-bold mb-3">Premium Features Coming Soon</h2>
                <p className="lead text-muted">Advanced tools and AI-powered analysis for serious bettors</p>
              </div>
              
              <div className="row g-4">
                <div className="col-lg-6">
                  <div className="card border-warning h-100">
                    <div className="card-header bg-warning text-dark d-flex justify-content-between align-items-center">
                      <h6 className="mb-0">
                        <i className="fas fa-robot me-2"></i>
                        🤖 AI Betting Assistant
                      </h6>
                      <span className="badge bg-dark text-white">COMING SOON</span>
                    </div>
                    <div className="card-body">
                      <p className="card-text">Natural language queries and intelligent recommendations. Ask questions like "Show me NBA games with +3% EV" and get instant, personalized results.</p>
                      <ul className="list-unstyled small text-muted">
                        <li><i className="fas fa-star me-2"></i>Conversational betting intelligence</li>
                        <li><i className="fas fa-star me-2"></i>Personalized +EV suggestions</li>
                        <li><i className="fas fa-star me-2"></i>Advanced filtering and search</li>
                        <li><i className="fas fa-star me-2"></i>Smart bet sizing recommendations</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div className="col-lg-6">
                  <div className="card border-secondary h-100">
                    <div className="card-header bg-secondary text-white d-flex justify-content-between align-items-center">
                      <h6 className="mb-0">
                        <i className="fas fa-bell me-2"></i>
                        📬 Bet Alerts & Notifications
                      </h6>
                      <span className="badge bg-dark text-white">COMING SOON</span>
                    </div>
                    <div className="card-body">
                      <p className="card-text">Get notified instantly when new +EV opportunities appear in your favorite sports or betting categories. Never miss a profitable edge again.</p>
                      <ul className="list-unstyled small text-muted">
                        <li><i className="fas fa-star me-2"></i>Real-time push notifications</li>
                        <li><i className="fas fa-star me-2"></i>Custom EV thresholds</li>
                        <li><i className="fas fa-star me-2"></i>Sport and league filtering</li>
                        <li><i className="fas fa-star me-2"></i>Email and SMS integration</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div className="col-lg-6">
                  <div className="card border-success h-100">
                    <div className="card-header bg-success text-white d-flex justify-content-between align-items-center">
                      <h6 className="mb-0">
                        <i className="fas fa-chart-pie me-2"></i>
                        📊 Portfolio Tracker
                      </h6>
                      <span className="badge bg-dark text-white">COMING SOON</span>
                    </div>
                    <div className="card-body">
                      <p className="card-text">Track your betting performance, closing line value (CLV), bankroll management, and ROI across all platforms and strategies.</p>
                      <ul className="list-unstyled small text-muted">
                        <li><i className="fas fa-star me-2"></i>Performance analytics dashboard</li>
                        <li><i className="fas fa-star me-2"></i>CLV tracking and reporting</li>
                        <li><i className="fas fa-star me-2"></i>Bankroll management tools</li>
                        <li><i className="fas fa-star me-2"></i>Export to Excel/CSV</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div className="col-lg-6">
                  <div className="card border-primary h-100">
                    <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                      <h6 className="mb-0">
                        <i className="fas fa-cogs me-2"></i>
                        🧠 Advanced Analytics
                      </h6>
                      <span className="badge bg-dark text-white">COMING SOON</span>
                    </div>
                    <div className="card-body">
                      <p className="card-text">Monte Carlo simulations, Bayesian probability models, visual EV graphs, and sophisticated risk assessment tools for professional bettors.</p>
                      <ul className="list-unstyled small text-muted">
                        <li><i className="fas fa-star me-2"></i>Monte Carlo simulations</li>
                        <li><i className="fas fa-star me-2"></i>Bayesian probability models</li>
                        <li><i className="fas fa-star me-2"></i>Visual EV and trend graphs</li>
                        <li><i className="fas fa-star me-2"></i>Risk assessment matrices</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why P2P Betting CTA Section */}
      <section className="py-5 bg-primary text-white">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-8">
              <h2 className="display-6 fw-bold mb-4">Why Peer-to-Peer Betting?</h2>
              <p className="lead mb-4">
                Think of it as <strong>"eBay for sports bets"</strong> or <strong>limit orders for betting</strong>. Instead of taking whatever odds the house offers, you set your price and wait for someone to accept it.
              </p>
              
              <div className="row mb-4">
                <div className="col-md-6">
                  <div className="d-flex mb-3">
                    <div className="me-3">
                      <i className="fas fa-check-circle fa-lg text-success"></i>
                    </div>
                    <div>
                      <h6 className="mb-1">You Control the Odds</h6>
                      <small>Set fair prices based on data, not house edges</small>
                    </div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="d-flex mb-3">
                    <div className="me-3">
                      <i className="fas fa-shield-alt fa-lg text-info"></i>
                    </div>
                    <div>
                      <h6 className="mb-1">Asymmetric Risk</h6>
                      <small>Win when matched, risk nothing when not</small>
                    </div>
                  </div>
                </div>
              </div>
              
              <p className="mb-4">
                Bet Intel helps you identify the exact odds that give you a mathematical edge, taking into account exchange fees and market dynamics. You're not chasing bad lines — you're setting good ones.
              </p>
            </div>
            
            <div className="col-lg-4 text-center">
              <div className="card border-0 shadow-lg">
                <div className="card-body p-4">
                  <h5 className="text-dark mb-3">Ready to Learn?</h5>
                  <p className="text-muted small mb-4">Our Education Center explains everything from EV basics to advanced P2P strategies.</p>
                  <a href="/education" className="btn btn-primary btn-lg w-100">
                    <i className="fas fa-graduation-cap me-2"></i>
                    Learn How It Works
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-5 bg-dark text-white">
        <div className="container">
          <div className="row">
            <div className="col-lg-8 mx-auto text-center">
              <h2 className="display-6 fw-bold mb-4">Start Betting Smarter Today</h2>
              <p className="lead mb-4">
                Join hundreds of sharp bettors using data-driven strategies to find profitable opportunities across traditional sportsbooks and P2P exchanges.
              </p>
              
              <div className="d-flex gap-3 justify-content-center flex-wrap mb-4">
                <a href="/dashboard" className="btn btn-success btn-lg">
                  <i className="fas fa-chart-bar me-2"></i>
                  Access Free Dashboard
                </a>
                <a href="/education" className="btn btn-outline-light btn-lg">
                  <i className="fas fa-book-open me-2"></i>
                  Read the Guide
                </a>
              </div>
              
              <div className="row text-center">
                <div className="col-md-4">
                  <div className="h4 text-success">100%</div>
                  <small className="text-muted">Free to Use</small>
                </div>
                <div className="col-md-4">
                  <div className="h4 text-info">3min</div>
                  <small className="text-muted">Data Updates</small>
                </div>
                <div className="col-md-4">
                  <div className="h4 text-warning">47+</div>
                  <small className="text-muted">Live Opportunities</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-light py-4 border-top">
        <div className="container">
          <div className="row">
            <div className="col-lg-8 mx-auto">
              <div className="d-flex justify-content-center flex-wrap gap-4 mb-3">
                <a href="/dashboard" className="text-decoration-none">
                  <i className="fas fa-chart-bar me-1"></i>
                  Dashboard
                </a>
                <a href="/education" className="text-decoration-none">
                  <i className="fas fa-graduation-cap me-1"></i>
                  Education
                </a>
                <a href="/disclaimers" className="text-decoration-none">
                  <i className="fas fa-balance-scale me-1"></i>
                  Disclaimers
                </a>
              </div>
              
              <div className="text-center">
                <p className="text-muted small mb-2">
                  <strong>Bet Intel</strong> provides betting information only. Always gamble responsibly.
                </p>
                <p className="text-muted small mb-0">
                  <i className="fas fa-info-circle me-1"></i>
                  We are not a sportsbook or betting operator. All betting decisions are made independently by users.
                </p>
              </div>
            </div>
          </div>
        </div>
      </footer>

    </div>
  );
};

export default Landing; 