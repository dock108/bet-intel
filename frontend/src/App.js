import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import SearchAI from './pages/SearchAI';
import Education from './pages/Education';
import Disclaimers from './pages/Disclaimers';

function App() {
  return (
    <Router>
      <div className="min-vh-100 bg-light">
        <Navigation />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/search-ai" element={<SearchAI />} />
            <Route path="/education" element={<Education />} />
            <Route path="/disclaimers" element={<Disclaimers />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 