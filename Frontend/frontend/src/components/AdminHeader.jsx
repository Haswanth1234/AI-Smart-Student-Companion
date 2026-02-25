import React from 'react';
import { Bell, Calendar, ChevronDown, Menu, LogOut, User as UserIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const AdminHeader = ({ toggleSidebar }) => {
    const navigate = useNavigate();

    // Mock user data - normally this would come from context/auth
    const user = {
        name: 'Admin User',
        role: 'HOD - MCA',
        initials: 'A'
    };

    const handleLogout = () => {
        if (window.confirm('Are you sure you want to logout?')) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            navigate('/login');
        }
    };

    return (
        <header style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '48px',
            padding: '8px 0',
            gap: '1rem'
        }}>
            {/* Left: Mobile Menu Toggle */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <button
                    className="mobile-only"
                    onClick={toggleSidebar}
                    style={{
                        background: 'rgba(255,255,255,0.05)',
                        border: '1px solid var(--glass-border)',
                        borderRadius: '10px',
                        padding: '8px',
                        color: 'white',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                    }}
                >
                    <Menu size={24} />
                </button>
            </div>

            {/* Right: Actions & Profile */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>

                {/* Date Controls */}
                <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                    <button className="glass-card hidden-mobile" style={{
                        padding: '8px 16px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        borderRadius: '20px',
                        border: '1px solid rgba(255,255,255,0.05)',
                        background: 'transparent',
                        color: '#94a3b8',
                        fontSize: '0.875rem',
                        cursor: 'pointer'
                    }}>
                        <Calendar size={16} />
                        <span>This Week</span>
                        <ChevronDown size={14} />
                    </button>

                    {/* Notification Icon */}
                    <div
                        onClick={() => navigate('/admin/alerts')}
                        style={{
                            position: 'relative',
                            cursor: 'pointer',
                            padding: '8px',
                            background: 'rgba(255,255,255,0.05)',
                            borderRadius: '50%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}
                    >
                        <Bell size={20} color="var(--text-secondary)" />
                        <span style={{
                            position: 'absolute', top: '0', right: '0',
                            background: 'var(--danger-color)', color: 'white',
                            fontSize: '0.65rem', fontWeight: 'bold',
                            width: '16px', height: '16px', borderRadius: '50%',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            border: '2px solid #0f172a',
                            boxShadow: '0 0 8px rgba(239, 68, 68, 0.5)'
                        }}>
                            3
                        </span>
                    </div>
                </div>

                <div style={{ width: '1px', height: '32px', background: 'rgba(255,255,255,0.1)' }}></div>

                {/* Profile & Logout */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }}>
                        <div style={{
                            width: '40px',
                            height: '40px',
                            borderRadius: '50%',
                            background: 'var(--primary-color)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'white',
                            fontWeight: '600',
                            fontSize: '1rem',
                            boxShadow: '0 0 10px var(--primary-glow)'
                        }}>
                            {user.initials}
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column' }} className="hidden-mobile">
                            <span style={{ fontSize: '0.9rem', fontWeight: '600', color: 'white' }}>{user.name}</span>
                            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{user.role}</span>
                        </div>
                    </div>

                    <button
                        onClick={handleLogout}
                        className="glass-card"
                        style={{
                            padding: '8px',
                            borderRadius: '10px',
                            border: '1px solid var(--danger-color)',
                            background: 'rgba(239, 68, 68, 0.1)',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}
                        title="Logout"
                    >
                        <LogOut size={18} color="var(--danger-color)" />
                    </button>
                </div>
            </div>
        </header>
    );
};

export default AdminHeader;
