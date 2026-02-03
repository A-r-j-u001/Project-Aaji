import React from 'react';
import { MessageCircle, Mail, Send, Camera } from 'lucide-react';

const ConnectionCard = ({ icon: Icon, title, description, endpoint, color, status }) => {
    const [copied, setCopied] = React.useState(false);

    const copyToClipboard = () => {
        // In a real app, we'd prefix with the actual Tunnel URL
        const text = `[YOUR_TUNNEL_URL]${endpoint}`;
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="glass-panel panel-hover" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ background: `rgba(${color}, 0.1)`, padding: '10px', borderRadius: '12px' }}>
                    <Icon size={24} style={{ color: `rgb(${color})` }} />
                </div>
                <span className={`badge ${status === 'Active' ? 'badge-success' : 'badge-danger'}`}>{status}</span>
            </div>

            <div>
                <h3>{title}</h3>
                <p style={{ fontSize: '0.9rem' }}>{description}</p>
            </div>

            <div style={{ marginTop: 'auto', background: 'rgba(0,0,0,0.3)', padding: '0.75rem', borderRadius: '8px', fontSize: '0.8rem', fontFamily: 'monospace', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '180px' }}>
                    ...{endpoint}
                </span>
                <button onClick={copyToClipboard} className="btn-ghost" style={{ padding: '4px', height: 'auto' }}>
                    {copied ? 'Copied!' : 'Copy'}
                </button>
            </div>
        </div>
    );
};

const Connections = () => {
    return (
        <div className="animate-fade-in">
            <div style={{ marginBottom: '2rem' }}>
                <h1>Connections</h1>
                <p>Connect your communication channels to the Aaji Brain.</p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
                <ConnectionCard
                    icon={MessageCircle}
                    title="WhatsApp"
                    description="Twilio Sandbox / Business API"
                    endpoint="/twilio/whatsapp"
                    color="37, 211, 102"
                    status="Active"
                />

                <ConnectionCard
                    icon={Camera}
                    title="Instagram"
                    description="Meta Graph API Webhooks"
                    endpoint="/meta/instagram"
                    color="225, 48, 108"
                    status="Active"
                />

                <ConnectionCard
                    icon={Send}
                    title="Telegram"
                    description="Telegram Bot API (Coming Soon)"
                    endpoint="/telegram/webhook"
                    color="0, 136, 204"
                    status="Pending"
                />

                <ConnectionCard
                    icon={Mail}
                    title="Email"
                    description="SMTP / IMAP Integration (Coming Soon)"
                    endpoint="/email/webhook"
                    color="234, 179, 8"
                    status="Pending"
                />
            </div>
        </div>
    );
};

export default Connections;
