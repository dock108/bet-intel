import React from 'react';
import betIntelLogo from '../assets/images/betintel-logo.png';

const Education = () => {
  return (
    <div className="container-fluid py-4">
      {/* Header */}
      <div className="row mb-5">
        <div className="col-lg-8 mx-auto text-center">
          <img 
            src={betIntelLogo} 
            alt="BetIntel Logo" 
            className="mb-3"
            style={{ height: '60px', width: 'auto' }}
          />
          <h1 className="display-4 fw-bold text-dark mb-3">Education Center</h1>
          <p className="lead text-muted">
            Master P2P betting and expected value to maximize your edge in sports betting
          </p>
        </div>
      </div>

      {/* Navigation Pills */}
      <div className="row mb-4">
        <div className="col-lg-10 mx-auto">
          <ul className="nav nav-pills justify-content-center flex-wrap">
            <li className="nav-item">
              <a className="nav-link" href="#p2p">💡 What is P2P Betting?</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#ev">📈 Expected Value</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#calculation">🎯 Our Method</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#offering">⚖️ Our Value</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#howto">🚀 How to Post</a>
            </li>
          </ul>
        </div>
      </div>

      <div className="row">
        <div className="col-lg-10 mx-auto">

          {/* Reality Check: U.S. Sports Betting */}
          <section className="mb-5">
            <div className="alert alert-secondary">
              <h5 className="mb-2">
                <i className="fas fa-flag-usa me-2"></i>Reality Check: The U.S. Market
              </h5>
              <p className="mb-2">
                With strict regulations, taxes, and increasingly efficient pricing, beating
                mainstream books like <strong>DraftKings</strong> or <strong>FanDuel</strong>
                long term is extremely difficult without a disciplined approach.
              </p>
              <p className="mb-0">
                Peer-to-peer exchanges let you post offers like <strong>limit orders</strong>
                in stock trading. By catching market swings or facing opponents who haven't
                done their homework, you can create opportunities those books rarely provide.
              </p>
            </div>
          </section>
          
          {/* Section 1: What is P2P Betting? */}
          <section id="p2p" className="mb-5">
            <div className="card border-primary">
              <div className="card-header bg-primary text-white">
                <h2 className="h3 mb-0">
                  <i className="fas fa-handshake me-2"></i>
                  💡 What is Peer-to-Peer (P2P) Betting?
                </h2>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-md-8">
                    <p className="lead">Think of P2P betting as <strong>"eBay for sports bets"</strong> — you're not betting against the house, you're betting against other users.</p>
                    
                    <h5 className="mt-4 mb-3">Key Differences:</h5>
                    <div className="row">
                      <div className="col-md-6">
                        <div className="card bg-light border-0 h-100">
                          <div className="card-body">
                            <h6 className="text-danger">❌ Traditional Sportsbooks</h6>
                            <ul className="small">
                              <li>Bet against the house</li>
                              <li>House sets the odds</li>
                              <li>House always has an edge</li>
                              <li>Limited to their lines</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                      <div className="col-md-6">
                        <div className="card bg-success bg-opacity-10 border-success h-100">
                          <div className="card-body">
                            <h6 className="text-success">✅ P2P Exchanges</h6>
                            <ul className="small">
                              <li>Bet against other users</li>
                              <li>You propose the odds</li>
                              <li>No house edge on odds</li>
                              <li>Set your own prices</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="alert alert-info mt-4">
                      <h6><i className="fas fa-info-circle me-2"></i>How It Works</h6>
                      <p className="mb-0">Exchanges charge a small commission (~2%) on winnings, but they don't manipulate odds. You set fair prices and wait for someone to take the other side.</p>
                    </div>
                  </div>
                  
                  <div className="col-md-4">
                    <div className="card border-0 bg-light h-100">
                      <div className="card-body text-center">
                        <h6 className="text-muted mb-3">P2P Flow</h6>
                        <div className="d-flex flex-column align-items-center">
                          <div className="badge bg-primary text-white px-3 py-2 mb-2 rounded-pill">
                            <i className="fas fa-user me-1"></i> You
                          </div>
                          <i className="fas fa-arrow-down text-muted mb-2"></i>
                          <div className="badge bg-warning text-dark px-3 py-2 mb-2 rounded-pill">
                            <i className="fas fa-exchange-alt me-1"></i> Exchange
                          </div>
                          <i className="fas fa-arrow-down text-muted mb-2"></i>
                          <div className="badge bg-success text-white px-3 py-2 rounded-pill">
                            <i className="fas fa-users me-1"></i> Other User
                          </div>
                        </div>
                        <small className="text-muted mt-3 d-block">Direct user-to-user betting with exchange facilitation</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Section 2: Understanding Odds & Expected Value */}
          <section id="ev" className="mb-5">
            <div className="card border-success">
              <div className="card-header bg-success text-white">
                <h2 className="h3 mb-0">
                  <i className="fas fa-chart-line me-2"></i>
                  📈 Understanding Odds & Expected Value
                </h2>
              </div>
              <div className="card-body">
                <div className="row mb-4">
                  <div className="col-md-6">
                    <h5>American Odds Explained</h5>
                    <div className="table-responsive">
                      <table className="table table-sm table-bordered">
                        <thead className="table-dark">
                          <tr>
                            <th>American Odds</th>
                            <th>Implied Probability</th>
                            <th>Meaning</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>+100</td>
                            <td>50%</td>
                            <td>Even money</td>
                          </tr>
                          <tr>
                            <td>+200</td>
                            <td>33.3%</td>
                            <td>2-to-1 underdog</td>
                          </tr>
                          <tr>
                            <td>-150</td>
                            <td>60%</td>
                            <td>Heavy favorite</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  
                  <div className="col-md-6">
                    <h5>What is "Vig"?</h5>
                    <p>The <strong>vig</strong> (vigorish) is the sportsbook's built-in edge. Instead of true 50/50 odds at +100, you might see:</p>
                    <div className="alert alert-warning">
                      <strong>Team A:</strong> -110 (52.4% implied)<br />
                      <strong>Team B:</strong> -110 (52.4% implied)<br />
                      <strong>Total:</strong> 104.8% (4.8% vig)
                    </div>
                    <p className="small text-muted">This extra 4.8% is the house edge — the odds are skewed against you.</p>
                  </div>
                </div>

                <h5 className="mb-3">Expected Value Formula</h5>
                <div className="card bg-dark text-white mb-4">
                  <div className="card-body text-center">
                    <h4 className="text-warning">EV = (Win Probability × Payout) - (Loss Probability × Stake)</h4>
                  </div>
                </div>

                <div className="row">
                  <div className="col-md-8">
                    <h6>Simple Example: The Magic Coin Flip</h6>
                    <p>Imagine a coin flip where you know it's exactly 50/50, but someone offers you <strong>+110 odds</strong>:</p>
                    
                    <div className="bg-light p-3 rounded">
                      <strong>Calculation:</strong><br />
                      • Win Probability: 50% (0.5)<br />
                      • Payout if Win: $110 profit on $100 bet<br />
                      • Loss Probability: 50% (0.5)<br />
                      • Loss if Lose: $100 stake<br /><br />
                      <strong>EV = (0.5 × $110) - (0.5 × $100) = $55 - $50 = +$5</strong>
                    </div>
                    
                    <div className="alert alert-success mt-3">
                      <strong>Result:</strong> You have a +$5 expected value per $100 bet. Over time, this edge compounds into consistent profit.
                    </div>
                  </div>
                  
                  <div className="col-md-4">
                    <div className="card border-success">
                      <div className="card-header bg-success text-white text-center">
                        <small>EV Over 100 Bets</small>
                      </div>
                      <div className="card-body text-center">
                        <div className="h4 text-success">+$500</div>
                        <small className="text-muted">Expected profit from +$5 EV per bet</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Section 3: How Bet Intel Calculates +EV */}
          <section id="calculation" className="mb-5">
            <div className="card border-warning">
              <div className="card-header bg-warning text-dark">
                <h2 className="h3 mb-0">
                  <i className="fas fa-calculator me-2"></i>
                  🎯 How Bet Intel Calculates +EV
                </h2>
              </div>
              <div className="card-body">
                <p className="lead">Our 7-step methodology ensures you only see bets with a real mathematical edge:</p>
                
                <div className="row">
                  <div className="col-lg-8">
                    <div className="accordion" id="methodologyAccordion">
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#step1">
                            <span className="badge bg-primary me-3">1</span>
                            Identify Sharp Bookmaker Odds
                          </button>
                        </h2>
                        <div id="step1" className="accordion-collapse collapse show" data-bs-parent="#methodologyAccordion">
                          <div className="accordion-body">
                            We use <strong>Pinnacle</strong> as our baseline because they accept sharp action and have minimal vig. Their odds reflect the true market consensus.
                          </div>
                        </div>
                      </div>
                      
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#step2">
                            <span className="badge bg-primary me-3">2</span>
                            Remove the Vig
                          </button>
                        </h2>
                        <div id="step2" className="accordion-collapse collapse" data-bs-parent="#methodologyAccordion">
                          <div className="accordion-body">
                            We strip out the bookmaker's edge to get "true" win probabilities. This reveals what the odds would be in a fair market.
                          </div>
                        </div>
                      </div>
                      
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#step3">
                            <span className="badge bg-primary me-3">3</span>
                            Compare Across Markets
                          </button>
                        </h2>
                        <div id="step3" className="accordion-collapse collapse" data-bs-parent="#methodologyAccordion">
                          <div className="accordion-body">
                            We scan odds from major sportsbooks and P2P exchanges to find discrepancies from the fair probability.
                          </div>
                        </div>
                      </div>
                      
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#step4">
                            <span className="badge bg-primary me-3">4</span>
                            Adjust for P2P Fees
                          </button>
                        </h2>
                        <div id="step4" className="accordion-collapse collapse" data-bs-parent="#methodologyAccordion">
                          <div className="accordion-body">
                            P2P exchanges charge ~2% commission on winnings. We factor this into our calculations to ensure post-fee profitability.
                          </div>
                        </div>
                      </div>
                      
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#step5">
                            <span className="badge bg-primary me-3">5</span>
                            Add EV Buffer
                          </button>
                        </h2>
                        <div id="step5" className="accordion-collapse collapse" data-bs-parent="#methodologyAccordion">
                          <div className="accordion-body">
                            We require a minimum +2.5% edge to account for model uncertainty and market noise. This protects you from borderline cases.
                          </div>
                        </div>
                      </div>
                      
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#step6">
                            <span className="badge bg-primary me-3">6</span>
                            Calculate Target Odds
                          </button>
                        </h2>
                        <div id="step6" className="accordion-collapse collapse" data-bs-parent="#methodologyAccordion">
                          <div className="accordion-body">
                            Using the true probability and our buffers, we calculate the exact odds you need to offer for profitable P2P betting.
                          </div>
                        </div>
                      </div>
                      
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#step7">
                            <span className="badge bg-primary me-3">7</span>
                            Filter & Highlight
                          </button>
                        </h2>
                        <div id="step7" className="accordion-collapse collapse" data-bs-parent="#methodologyAccordion">
                          <div className="accordion-body">
                            Only bets that pass all criteria make it to your dashboard, ranked by expected value and confidence level.
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="col-lg-4">
                    <div className="card bg-dark text-white">
                      <div className="card-header">
                        <h6 className="mb-0">Sample Calculation</h6>
                      </div>
                      <div className="card-body">
                        <p className="small mb-2"><strong>Pinnacle:</strong> Team A -105 (51.2% fair)</p>
                        <p className="small mb-2"><strong>Target:</strong> +4.5% EV (2% fee + 2.5% buffer)</p>
                        <p className="small mb-2"><strong>Required Odds:</strong> +110 or better</p>
                        <hr className="border-light" />
                        <p className="small mb-0 text-warning"><strong>Recommendation:</strong> Offer Team A at +110 on P2P exchange</p>
                      </div>
                    </div>
                    
                    <div className="alert alert-info mt-3">
                      <small>
                        <i className="fas fa-lightbulb me-1"></i>
                        <strong>Pro Tip:</strong> We don't chase pennies. Every recommendation has a clear mathematical edge to protect your bankroll.
                      </small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Section 4: What We're Offering */}
          <section id="offering" className="mb-5">
            <div className="card border-info">
              <div className="card-header bg-info text-white">
                <h2 className="h3 mb-0">
                  <i className="fas fa-gem me-2"></i>
                  ⚖️ What Bet Intel Offers You
                </h2>
              </div>
              <div className="card-body">
                <div className="row mb-4">
                  <div className="col-lg-8">
                    <div className="alert alert-primary border-primary">
                      <h5 className="alert-heading">
                        <i className="fas fa-quote-left me-2"></i>
                        You're not chasing bad lines. You're setting good ones.
                      </h5>
                      <p className="mb-0">Think of it as limit orders for sports betting. If someone wants to take the other side at your price, they can. If not, you risk nothing.</p>
                    </div>
                    
                    <h5 className="mb-3">Perfect Analogies:</h5>
                    <div className="row">
                      <div className="col-md-6">
                        <div className="card border-warning h-100">
                          <div className="card-body">
                            <h6 className="text-warning">
                              <i className="fab fa-ebay me-2"></i>eBay Seller
                            </h6>
                            <p className="small mb-0">"I'm offering this item at this price. If someone wants it, they'll buy it. If not, no problem."</p>
                          </div>
                        </div>
                      </div>
                      <div className="col-md-6">
                        <div className="card border-success h-100">
                          <div className="card-body">
                            <h6 className="text-success">
                              <i className="fas fa-chart-line me-2"></i>Stock Limit Order
                            </h6>
                            <p className="small mb-0">"I'll buy this stock if it hits my target price. Otherwise, I wait for better opportunities."</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="col-lg-4">
                    <div className="card bg-success bg-opacity-10 border-success">
                      <div className="card-header bg-success text-white">
                        <h6 className="mb-0">Your Edge</h6>
                      </div>
                      <div className="card-body">
                        <ul className="list-unstyled mb-0">
                          <li><i className="fas fa-check text-success me-2"></i>Data-backed recommendations</li>
                          <li><i className="fas fa-check text-success me-2"></i>Mathematical edge required</li>
                          <li><i className="fas fa-check text-success me-2"></i>Asymmetric upside</li>
                          <li><i className="fas fa-check text-success me-2"></i>No risk if unmatched</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>

                <h5 className="mb-3">Why People Accept Your Odds:</h5>
                <div className="row">
                  <div className="col-md-4">
                    <div className="text-center mb-3">
                      <div className="badge bg-primary rounded-circle p-3 mb-2">
                        <i className="fas fa-clock fa-lg"></i>
                      </div>
                      <h6>Line Movement</h6>
                      <p className="small text-muted">They want action on a line that moved, but you caught the better price earlier.</p>
                    </div>
                  </div>
                  <div className="col-md-4">
                    <div className="text-center mb-3">
                      <div className="badge bg-warning rounded-circle p-3 mb-2">
                        <i className="fas fa-gift fa-lg"></i>
                      </div>
                      <h6>Bonus Funds</h6>
                      <p className="small text-muted">They have promotional credits or gift cards and aren't focused on getting the absolute best odds.</p>
                    </div>
                  </div>
                  <div className="col-md-4">
                    <div className="text-center mb-3">
                      <div className="badge bg-info rounded-circle p-3 mb-2">
                        <i className="fas fa-zap fa-lg"></i>
                      </div>
                      <h6>Convenience</h6>
                      <p className="small text-muted">They want immediate action and don't shop around for better odds across multiple platforms.</p>
                    </div>
                  </div>
                </div>

                <div className="alert alert-dark mt-4">
                  <h6 className="alert-heading">
                    <i className="fas fa-trophy me-2"></i>
                    Core Message
                  </h6>
                  <p className="mb-0">This is <strong>betting with an edge</strong> — data-backed offers with asymmetric upside. You win when matched, and risk nothing when not.</p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 5: How to Post a Bet */}
          <section id="howto" className="mb-5">
            <div className="card border-dark">
              <div className="card-header bg-dark text-white">
                <h2 className="h3 mb-0">
                  <i className="fas fa-rocket me-2"></i>
                  🚀 How to Post a Bet
                </h2>
              </div>
              <div className="card-body">
                <p className="lead">Follow these simple steps to turn Bet Intel recommendations into actual +EV bets:</p>
                
                <div className="row">
                  <div className="col-lg-8">
                    <div className="row">
                      <div className="col-md-6 mb-4">
                        <div className="card h-100 border-primary">
                          <div className="card-body text-center">
                            <div className="badge bg-primary rounded-circle p-3 mb-3">
                              <span className="h4 text-white mb-0">1</span>
                            </div>
                            <h6>Find a Recommendation</h6>
                            <p className="small text-muted">Browse your Bet Intel dashboard for opportunities with positive EV and confidence scores you're comfortable with.</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="col-md-6 mb-4">
                        <div className="card h-100 border-success">
                          <div className="card-body text-center">
                            <div className="badge bg-success rounded-circle p-3 mb-3">
                              <span className="h4 text-white mb-0">2</span>
                            </div>
                            <h6>Copy the Target Odds</h6>
                            <p className="small text-muted">Use the exact odds we calculate — they're designed to give you the required edge after all fees and buffers.</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="col-md-6 mb-4">
                        <div className="card h-100 border-warning">
                          <div className="card-body text-center">
                            <div className="badge bg-warning rounded-circle p-3 mb-3">
                              <span className="h4 text-dark mb-0">3</span>
                            </div>
                            <h6>Go to P2P Exchange</h6>
                            <p className="small text-muted">Open your preferred exchange (Novig, ProphetX, or BetOpenly) and navigate to the recommended game.</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="col-md-6 mb-4">
                        <div className="card h-100 border-info">
                          <div className="card-body text-center">
                            <div className="badge bg-info rounded-circle p-3 mb-3">
                              <span className="h4 text-white mb-0">4</span>
                            </div>
                            <h6>Post Your Offer</h6>
                            <p className="small text-muted">Create your bet using our recommended odds and your chosen stake amount. Double-check the details before posting.</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="card bg-success bg-opacity-10 border-success">
                      <div className="card-body text-center">
                        <div className="badge bg-success rounded-circle p-3 mb-3">
                          <span className="h4 text-white mb-0">5</span>
                        </div>
                        <h6>Wait for Match & Win</h6>
                        <p className="small mb-3">Your bet is now live. If someone accepts your odds, you have a positive EV bet. If not, you've risked nothing.</p>
                        <div className="alert alert-success mb-0">
                          <small><strong>Pro Tip:</strong> You can post multiple offers and let the market come to you. Patience is key to maximizing your edge.</small>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="col-lg-4">
                    <h6 className="mb-3">Supported P2P Exchanges</h6>
                    
                    <div className="d-grid gap-2 mb-4">
                      <button className="btn btn-primary">
                        <i className="fas fa-external-link-alt me-2"></i>
                        🥇 Novig (Recommended)
                      </button>
                      <button className="btn btn-outline-primary">
                        <i className="fas fa-external-link-alt me-2"></i>
                        ProphetX
                      </button>
                      <button className="btn btn-outline-primary">
                        <i className="fas fa-external-link-alt me-2"></i>
                        BetOpenly
                      </button>
                    </div>
                    
                    <div className="card border-info">
                      <div className="card-header bg-info text-white">
                        <h6 className="mb-0">Sample Bet Post</h6>
                      </div>
                      <div className="card-body">
                        <div className="small">
                          <strong>Game:</strong> Lakers vs Warriors<br />
                          <strong>Bet:</strong> Lakers +6.5<br />
                          <strong>Your Odds:</strong> +110<br />
                          <strong>Stake:</strong> $100<br />
                          <strong>Potential Win:</strong> $110<br />
                          <strong>Expected Value:</strong> +$5.50
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Call to Action */}
          <section className="mb-5">
            <div className="card bg-primary text-white text-center">
              <div className="card-body py-5">
                <h3 className="mb-3">Ready to Start Betting with an Edge?</h3>
                <p className="lead mb-4">Join thousands of sharp bettors using data-driven P2P strategies</p>
                <div className="d-flex gap-3 justify-content-center flex-wrap">
                  <a href="/dashboard" className="btn btn-light btn-lg">
                    <i className="fas fa-chart-line me-2"></i>
                    View Dashboard
                  </a>
                  <a href="/disclaimers" className="btn btn-outline-light btn-lg">
                    <i className="fas fa-info-circle me-2"></i>
                    Legal Info
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

export default Education; 