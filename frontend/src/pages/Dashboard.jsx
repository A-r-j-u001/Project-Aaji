import React from 'react';
import { Shield, Clock, DollarSign, Activity } from 'lucide-react';

const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ background: `rgba(${color}, 0.15)`, padding: '12px', borderRadius: '12px' }}>
            <Icon size={28} style={{ color: `rgb(${color})` }} />
        </div>
        <div>
            <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>{label}</div>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{value}</div>
        </div>
    </div>
);

const Dashboard = () => {
    return (
        <div className="animate-fade-in">
            <div style={{ marginBottom: '2rem' }}>
                <h1>Command Center</h1>
                <p>System Status: <span className="badge badge-success">OPERATIONAL - PROTECTING</span></p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
                <StatCard icon={Shield} label="Scams Intercepted" value="1,248" color="139, 92, 246" />
                <StatCard icon={Clock} label="Scammer Time Wasted" value="482h" color="16, 185, 129" />
                <StatCard icon={DollarSign} label="Estimated Saved" value="₹5.2 Cr" color="234, 179, 8" />
                <StatCard icon={Activity} label="Active Threads" value="12" color="239, 68, 68" />
            </div>

            <div className="glass-panel" style={{ padding: '2rem' }}>
                <h3>Recent Threat Activity</h3>
                <p>Chart coming soon...</p>
            </div>
        </div>
    );
};

export default Dashboard;
