import React from 'react';
import { Terminal } from 'lucide-react';

const LogItem = ({ time, source, message, type }) => (
    <div style={{
        display: 'flex',
        gap: '1rem',
        padding: '1rem',
        borderBottom: '1px solid var(--glass-border)',
        fontFamily: 'monospace',
        fontSize: '0.9rem'
    }}>
        <div style={{ color: 'var(--text-muted)', minWidth: '80px' }}>{time}</div>
        <div style={{ width: '100px' }}><span className={`badge ${type === 'danger' ? 'badge-danger' : 'badge-success'}`}>{source}</span></div>
        <div style={{ flex: 1, color: 'var(--text-main)' }}>{message}</div>
    </div>
);

const LiveFeed = () => {
    // Mock Data
    const logs = [
        { time: "19:42:01", source: "WHATSAPP", message: "Scammer: 'Sir your KYC is pending...'", type: "danger" },
        { time: "19:42:05", source: "AAJI", message: "Aaji: 'Beta I don't know what is KYC? Is it safe?'", type: "success" },
        { time: "19:42:12", source: "SYSTEM", message: "Extraction: Detected keyword 'KYC' (Risk Score: 0.9)", type: "info" },
        { time: "19:43:00", source: "INSTAGRAM", message: "Scammer: 'You won iPhone 15 pro max!'", type: "danger" },
        { time: "19:43:10", source: "AAJI", message: "Aaji: 'What?? Really? My grandson Rohan wanted one.'", type: "success" }
    ];

    return (
        <div className="animate-fade-in" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div style={{ marginBottom: '2rem' }}>
                <h1>Live Intelligence Feed</h1>
                <p>Real-time interception and engagement logs.</p>
            </div>

            <div className="glass-panel" style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
                <div style={{ padding: '1rem', borderBottom: '1px solid var(--glass-border)', background: 'rgba(0,0,0,0.2)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Terminal size={18} /> <span>/var/log/aaji-interceptor</span>
                </div>
                <div style={{ overflowY: 'auto', flex: 1 }}>
                    {logs.map((log, i) => (
                        <LogItem key={i} {...log} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default LiveFeed;
