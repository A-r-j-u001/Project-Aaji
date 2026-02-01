import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Radio, MessageSquare, Settings, Activity } from 'lucide-react';
import './index.css';

import Dashboard from './pages/Dashboard';
import Connections from './pages/Connections';
import LiveFeed from './pages/LiveFeed';

const SidebarItem = ({ to, icon: Icon, label }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link to={to} className={`btn btn-ghost ${isActive ? 'active-nav' : ''}`} style={{ justifyContent: 'flex-start', marginBottom: '0.5rem', background: isActive ? 'rgba(139, 92, 246, 0.1)' : '', color: isActive ? '#fff' : '' }}>
      <Icon size={20} color={isActive ? '#8b5cf6' : 'currentColor'} />
      {label}
    </Link>
  );
};

function App() {
  return (
    <Router>
      <div className="app-layout">
        <aside className="sidebar glass-panel" style={{ borderRadius: 0, borderTop: 0, borderBottom: 0, borderLeft: 0 }}>
          <div style={{ marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: 40, height: 40, background: 'var(--color-primary)', borderRadius: '50%', display: 'grid', placeItems: 'center', boxShadow: '0 0 15px var(--color-primary-glow)' }}>
              <Activity color="white" />
            </div>
            <h2 style={{ fontSize: '1.2rem', letterSpacing: '1px' }}>AAJI AGENT</h2>
          </div>

          <SidebarItem to="/" icon={LayoutDashboard} label="Dashboard" />
          <SidebarItem to="/connections" icon={Radio} label="Connections" />
          <SidebarItem to="/feed" icon={Activity} label="Live Feed" />
          <SidebarItem to="/logs" icon={MessageSquare} label="Logs" />

          <div style={{ marginTop: 'auto' }}>
            <SidebarItem to="/settings" icon={Settings} label="Settings" />
          </div>
        </aside>

        <main className="content-area">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/connections" element={<Connections />} />
            <Route path="/feed" element={<LiveFeed />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
