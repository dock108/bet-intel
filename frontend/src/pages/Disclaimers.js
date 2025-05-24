import React from 'react';
import betIntelLogo from '../assets/images/betintel-logo.png';

const Disclaimers = () => {
  return (
    <div className="container py-5">
      {/* Header */}
      <div className="row mb-5">
        <div className="col-lg-8 mx-auto text-center">
          <img 
            src={betIntelLogo} 
            alt="BetIntel Logo" 
            className="mb-3"
            style={{ height: '50px', width: 'auto' }}
          />
          <h1 className="display-5 fw-bold text-dark mb-3">Legal Disclaimers</h1>
          <p className="lead text-muted">
            Important legal information and risk disclosures for Bet Intel users
          </p>
        </div>
      </div>

      <div className="row">
        <div className="col-lg-8 mx-auto">
          
          {/* Effective Date */}
          <div className="alert alert-info mb-4">
            <h6 className="alert-heading mb-2">
              <i className="fas fa-calendar-alt me-2"></i>
              Effective Date
            </h6>
            <p className="mb-0">These disclaimers are effective as of May 23, 2025 and apply to all users of the Bet Intel platform.</p>
          </div>

          {/* Section 1: Nature of Service */}
          <section className="mb-5">
            <div className="card border-primary">
              <div className="card-header bg-primary text-white">
                <h5 className="mb-0">
                  <i className="fas fa-info-circle me-2"></i>
                  1. Nature of Service
                </h5>
              </div>
              <div className="card-body">
                <p className="lead">Bet Intel is an <strong>informational analytics platform only</strong>.</p>
                
                <p>We do not accept, place, or manage bets in any capacity. Bet Intel provides data-driven recommendations designed to identify value opportunities across sportsbooks and peer-to-peer (P2P) exchanges. All decisions to bet are made independently by users.</p>
                
                <div className="alert alert-warning">
                  <h6 className="alert-heading">
                    <i className="fas fa-exclamation-triangle me-2"></i>
                    Important Clarification
                  </h6>
                  <p className="mb-0">Bet Intel is <strong>not a sportsbook, betting exchange, or gambling operator</strong>. We are an information service that analyzes publicly available odds data to identify potential value opportunities.</p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 2: No Warranties */}
          <section className="mb-5">
            <div className="card border-warning">
              <div className="card-header bg-warning text-dark">
                <h5 className="mb-0">
                  <i className="fas fa-shield-alt me-2"></i>
                  2. No Warranties or Guarantees
                </h5>
              </div>
              <div className="card-body">
                <p className="lead">We make <strong>no guarantees</strong> about betting outcomes or profits.</p>
                
                <div className="row mb-3">
                  <div className="col-md-6">
                    <h6 className="text-warning">❌ What We Don't Guarantee:</h6>
                    <ul>
                      <li>Winning bets or profit generation</li>
                      <li>Accuracy of odds calculations</li>
                      <li>Availability of recommended odds</li>
                      <li>Future performance based on past results</li>
                    </ul>
                  </div>
                  <div className="col-md-6">
                    <h6 className="text-success">✅ What We Provide:</h6>
                    <ul>
                      <li>Mathematical analysis of publicly available data</li>
                      <li>Educational content about betting concepts</li>
                      <li>Transparent methodology explanations</li>
                      <li>Information to help inform your decisions</li>
                    </ul>
                  </div>
                </div>
                
                <div className="bg-light p-3 rounded">
                  <p className="mb-2"><strong>Sports outcomes are inherently uncertain.</strong> Even mathematically positive expected value (+EV) bets can and will lose. Individual bet results do not validate or invalidate our analytical approach.</p>
                  <p className="mb-0"><strong>Historical performance is not indicative of future results.</strong> Past success does not guarantee future profitability.</p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 3: Risk of Loss */}
          <section className="mb-5">
            <div className="card border-danger">
              <div className="card-header bg-danger text-white">
                <h5 className="mb-0">
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  3. Risk of Loss & Responsible Gambling
                </h5>
              </div>
              <div className="card-body">
                <p className="lead">Bet responsibly. <strong>All sports betting carries significant financial risk.</strong></p>
                
                <div className="alert alert-danger border-danger">
                  <h6 className="alert-heading text-danger">⚠️ Critical Risk Warning</h6>
                  <p className="mb-2">You should <strong>never bet more than you can afford to lose</strong>. Sports betting should be treated as entertainment, not as an investment strategy or income source.</p>
                  <p className="mb-0">Even with sophisticated analysis, <strong>losing streaks are inevitable</strong> and can be longer than expected.</p>
                </div>

                <h6 className="mt-4 mb-3">Responsible Gambling Guidelines:</h6>
                <div className="row">
                  <div className="col-md-6">
                    <ul>
                      <li>Set strict bankroll limits before betting</li>
                      <li>Never chase losses with larger bets</li>
                      <li>Take regular breaks from betting activity</li>
                      <li>Don't bet when emotional or impaired</li>
                    </ul>
                  </div>
                  <div className="col-md-6">
                    <ul>
                      <li>Keep betting separate from necessary funds</li>
                      <li>Monitor your betting behavior regularly</li>
                      <li>Seek help if gambling becomes problematic</li>
                      <li>Remember: betting should be fun, not stressful</li>
                    </ul>
                  </div>
                </div>

                <div className="card bg-info bg-opacity-10 border-info mt-4">
                  <div className="card-body text-center">
                    <h6 className="text-info">
                      <i className="fas fa-phone me-2"></i>
                      Need Help with Problem Gambling?
                    </h6>
                    <p className="mb-3">If you or someone you know has a gambling problem, help is available.</p>
                    <div className="d-flex gap-3 justify-content-center flex-wrap">
                      <button className="btn btn-info">
                        <i className="fas fa-phone me-2"></i>
                        Call 1-800-GAMBLER
                      </button>
                      <button className="btn btn-outline-info">
                        <i className="fas fa-external-link-alt me-2"></i>
                        Visit ncpgambling.org
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Section 4: Age and Jurisdiction */}
          <section className="mb-5">
            <div className="card border-secondary">
              <div className="card-header bg-secondary text-white">
                <h5 className="mb-0">
                  <i className="fas fa-id-card me-2"></i>
                  4. Age and Jurisdiction Requirements
                </h5>
              </div>
              <div className="card-body">
                <p className="lead">Bet Intel is intended only for users of <strong>legal betting age</strong>.</p>
                
                <div className="row mb-4">
                  <div className="col-md-6">
                    <div className="card border-warning h-100">
                      <div className="card-body">
                        <h6 className="text-warning">
                          <i className="fas fa-calendar-check me-2"></i>
                          Age Requirements
                        </h6>
                        <p className="small mb-0">You must be <strong>18+ or 21+</strong> (depending on your region) to use this platform for wagering advice and to access sportsbook/exchange links.</p>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="card border-info h-100">
                      <div className="card-body">
                        <h6 className="text-info">
                          <i className="fas fa-map-marker-alt me-2"></i>
                          Jurisdiction Compliance
                        </h6>
                        <p className="small mb-0">If sports betting is not legal in your jurisdiction, you may use the site for <strong>entertainment and educational purposes only</strong>.</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="alert alert-secondary">
                  <h6 className="alert-heading">
                    <i className="fas fa-gavel me-2"></i>
                    Your Responsibility
                  </h6>
                  <p className="mb-0">It is <strong>your responsibility</strong> to ensure that your use of Bet Intel and any subsequent betting activity complies with all applicable local, state, and federal laws in your jurisdiction.</p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 5: Affiliate Disclosure */}
          <section className="mb-5">
            <div className="card border-success">
              <div className="card-header bg-success text-white">
                <h5 className="mb-0">
                  <i className="fas fa-handshake me-2"></i>
                  5. Affiliate Disclosure
                </h5>
              </div>
              <div className="card-body">
                <p className="lead">Some links may be <strong>affiliate links</strong>.</p>
                
                <p>Bet Intel may earn commissions when users sign up or place bets through our partnered sportsbook or exchange links. This helps support our platform and keep our analysis tools free for users.</p>

                <div className="alert alert-success border-success">
                  <h6 className="alert-heading">
                    <i className="fas fa-balance-scale me-2"></i>
                    Our Commitment to Objectivity
                  </h6>
                  <p className="mb-0">These affiliate relationships <strong>do not affect the objectivity</strong> of our data analysis or recommendations. Our mathematical models and EV calculations are independent of any commercial relationships.</p>
                </div>

                <h6 className="mt-3 mb-2">Transparency Promise:</h6>
                <ul>
                  <li>We clearly identify when links are affiliate relationships</li>
                  <li>Our recommendations are based on mathematical analysis, not affiliate payouts</li>
                  <li>We recommend multiple platforms to give users choice</li>
                  <li>Users are never required to use affiliate links</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 6: Methodology Transparency */}
          <section className="mb-5">
            <div className="card border-dark">
              <div className="card-header bg-dark text-white">
                <h5 className="mb-0">
                  <i className="fas fa-calculator me-2"></i>
                  6. Methodology Transparency
                </h5>
              </div>
              <div className="card-body">
                <p className="lead">Want to understand how we calculate fair odds and +EV opportunities?</p>
                
                <p>We believe in complete transparency about our analytical methods. Our calculations are based on publicly available odds data, statistical models, and clearly defined mathematical principles.</p>

                <div className="alert alert-dark border-dark">
                  <h6 className="alert-heading">
                    <i className="fas fa-graduation-cap me-2"></i>
                    Learn Our Methodology
                  </h6>
                  <p className="mb-3">Our Education Center provides a comprehensive breakdown of our 7-step calculation process, including how we identify sharp lines, remove vig, and calculate target P2P odds.</p>
                  <a href="/education" className="btn btn-dark">
                    <i className="fas fa-book-open me-2"></i>
                    Visit Education Center
                  </a>
                </div>

                <h6 className="mt-3 mb-2">What We Analyze:</h6>
                <div className="row">
                  <div className="col-md-6">
                    <ul>
                      <li>Real-time odds from major sportsbooks</li>
                      <li>P2P exchange pricing data</li>
                      <li>Historical line movement patterns</li>
                      <li>Market efficiency indicators</li>
                    </ul>
                  </div>
                  <div className="col-md-6">
                    <ul>
                      <li>Vig calculations and removal techniques</li>
                      <li>Fair value probability assessments</li>
                      <li>Expected value computations</li>
                      <li>Risk-adjusted recommendations</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Section 7: Limitation of Liability */}
          <section className="mb-5">
            <div className="card border-dark">
              <div className="card-header bg-dark text-white">
                <h5 className="mb-0">
                  <i className="fas fa-shield-alt me-2"></i>
                  7. Limitation of Liability
                </h5>
              </div>
              <div className="card-body">
                <p className="lead">Bet Intel provides information services <strong>"as is"</strong> without warranties.</p>
                
                <div className="bg-light p-3 rounded mb-3">
                  <p className="mb-2"><strong>To the fullest extent permitted by law</strong>, Bet Intel and its operators disclaim all liability for:</p>
                  <ul className="mb-0">
                    <li>Financial losses resulting from betting decisions</li>
                    <li>Inaccuracies in data, calculations, or recommendations</li>
                    <li>Technical issues, downtime, or service interruptions</li>
                    <li>Third-party sportsbook or exchange problems</li>
                    <li>Any direct, indirect, incidental, or consequential damages</li>
                  </ul>
                </div>

                <div className="alert alert-warning">
                  <h6 className="alert-heading">
                    <i className="fas fa-user-shield me-2"></i>
                    User Responsibility
                  </h6>
                  <p className="mb-0">By using Bet Intel, you acknowledge that <strong>you are solely responsible</strong> for your betting decisions and any resulting financial outcomes. You agree to use our information at your own risk.</p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 8: Changes to Disclaimers */}
          <section className="mb-5">
            <div className="card border-info">
              <div className="card-header bg-info text-white">
                <h5 className="mb-0">
                  <i className="fas fa-edit me-2"></i>
                  8. Changes to These Disclaimers
                </h5>
              </div>
              <div className="card-body">
                <p>We reserve the right to update these disclaimers at any time. Material changes will be posted on this page with an updated effective date.</p>
                
                <p className="mb-0">Continued use of Bet Intel after changes are posted constitutes acceptance of the revised disclaimers.</p>
              </div>
            </div>
          </section>

          {/* Contact Information */}
          <section className="mb-5">
            <div className="card bg-primary text-white text-center">
              <div className="card-body">
                <h5 className="mb-3">Questions About These Disclaimers?</h5>
                <p className="mb-3">If you have questions about these legal disclaimers or need clarification about our services, please contact us.</p>
                <div className="d-flex gap-3 justify-content-center flex-wrap">
                  <a href="/education" className="btn btn-light">
                    <i className="fas fa-graduation-cap me-2"></i>
                    Education Center
                  </a>
                  <a href="/dashboard" className="btn btn-outline-light">
                    <i className="fas fa-chart-line me-2"></i>
                    Return to Dashboard
                  </a>
                </div>
              </div>
            </div>
          </section>

        </div>
      </div>
    </div>
  );
};

export default Disclaimers; 