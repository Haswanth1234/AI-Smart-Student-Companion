import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, LogOut, User as UserIcon, Menu } from 'lucide-react';

export default function Header({ title, onMenuClick }) {
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const alertsCount = 3;

    const handleLogout = () => {
        if (window.confirm('Are you sure you want to logout?')) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            navigate('/login');
        }
    };

    return (
        <header className="flex-between mb-6 pb-4" style={{ borderBottom: '1px solid var(--glass-border)', gap: '1rem' }}>
            <div className="flex-center gap-4">
                <button className="menu-toggle" onClick={onMenuClick}>
                    <Menu size={24} />
                </button>
                <div>
                    <h1 className="heading-md" style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>{title}</h1>
                    <p className="text-secondary text-sm hidden-mobile">Welcome back, {user.name || 'Student'}</p>
                </div>
            </div>

            <div className="flex-center gap-4">
                <div style={{ position: 'relative', cursor: 'pointer', padding: '0.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '50%' }}>
                    <Bell size={20} color="var(--text-secondary)" />
                    {alertsCount > 0 && (
                        <span style={{
                            position: 'absolute', top: '0', right: '0',
                            background: 'var(--danger-color)', color: 'white',
                            fontSize: '0.65rem', fontWeight: 'bold',
                            width: '14px', height: '14px', borderRadius: '50%',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            border: '2px solid #0f172a'
                        }}>
                            {alertsCount}
                        </span>
                    )}
                </div>

                <div className="flex-center gap-2 pl-4" style={{ borderLeft: '1px solid var(--glass-border)' }}>
                    <div className="text-right hidden-mobile">
                        <div className="text-sm font-semibold">{user.name}</div>
                        <div className="text-xs text-secondary">{user.department}</div>
                    </div>
                    <button onClick={handleLogout} className="glass-card flex-center" style={{ padding: '0.5rem', borderRadius: '10px', border: '1px solid var(--danger-color)', background: 'rgba(239, 68, 68, 0.1)' }}>
                        <LogOut size={18} color="var(--danger-color)" />
                    </button>
                </div>
            </div>
        </header>
    );
}
