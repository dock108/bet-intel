import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: 'fas fa-chart-bar' },
    { path: '/search-ai', label: 'Search AI', icon: 'fas fa-robot' },
    { path: '/education', label: 'Education', icon: 'fas fa-book' },
    { path: '/disclaimers', label: 'Disclaimers', icon: 'fas fa-balance-scale' }
  ];

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm border-bottom sticky-top">
      <div className="container-fluid">
        {/* Logo & Title */}
        <Link to="/" className="navbar-brand d-flex align-items-center">
          <span className="text-dark">Bet Intel</span>
          <span className="badge bg-success ms-2 fs-6">LIVE DATA</span>
        </Link>

        {/* Mobile toggle button */}
        <button 
          className="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
          aria-controls="navbarNav" 
          aria-expanded="false" 
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        {/* Navigation Links */}
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            {navItems.map((item) => (
              <li key={item.path} className="nav-item">
                <Link
                  to={item.path}
                  className={`nav-link px-3 py-2 mx-1 d-flex align-items-center ${
                    isActive(item.path) ? 'active text-primary fw-semibold' : 'text-dark'
                  }`}
                >
                  <i className={`${item.icon} me-2`}></i>
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navigation; 