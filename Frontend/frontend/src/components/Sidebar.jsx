import React from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import {
    LayoutDashboard,
    UserCircle,
    ClipboardCheck,
    ListTodo,
    Bot,
    Bell,
    LogOut,
    FileText,
    Settings,
    X
} from 'lucide-react';

export default function Sidebar({ isOpen, toggleSidebar }) {
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
    };

    const navItems = [
        { name: 'Dashboard', path: '/admin/dashboard', icon: <LayoutDashboard size={20} /> },
        { name: 'Students', path: '/admin/students', icon: <UserCircle size={20} /> },
        { name: 'Attendance', path: '/admin/attendance', icon: <ClipboardCheck size={20} /> },
        { name: 'Tasks', path: '/admin/tasks', icon: <ListTodo size={20} /> },
        { name: 'Alerts', path: '/admin/alerts', icon: <Bell size={20} /> },
        { name: 'Reports', path: '/admin/reports', icon: <FileText size={20} /> },
        { name: 'Settings', path: '/admin/settings', icon: <Settings size={20} /> },
    ];

    return (
        <aside className={`admin-sidebar ${isOpen ? 'open' : ''}`}>
            {/* Header / Logo Area */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 8px 32px 8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{
                        width: '32px', height: '32px',
                        background: 'linear-gradient(45deg, #06b6d4, #6366f1)',
                        borderRadius: '8px'
                    }}></div>
                    <h1 style={{
                        fontSize: '1.25rem',
                        fontWeight: '700',
                        background: 'linear-gradient(to right, #fff, #cffafe)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        margin: 0
                    }}>AdminPanel</h1>
                </div>
                <button
                    className="close-sidebar-btn mobile-only"
                    onClick={toggleSidebar}
                    style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
                >
                    <X size={24} />
                </button>
            </div>

            {/* Navigation */}
            <nav style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        style={({ isActive }) => ({
                            display: 'flex',
                            alignItems: 'center',
                            gap: '16px',
                            padding: '16px 20px',
                            color: isActive ? '#06b6d4' : '#94a3b8',
                            textDecoration: 'none',
                            borderRadius: '12px',
                            fontWeight: '500',
                            fontSize: '0.95rem',
                            background: isActive ? 'linear-gradient(90deg, rgba(6, 182, 212, 0.2) 0%, rgba(6, 182, 212, 0.05) 100%)' : 'transparent',
                            border: isActive ? '1px solid rgba(6, 182, 212, 0.2)' : '1px solid transparent',
                            boxShadow: isActive ? '0 4px 12px rgba(6, 182, 212, 0.15)' : 'none',
                            position: 'relative',
                            overflow: 'hidden',
                            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
                        })}
                    >
                        {({ isActive }) => (
                            <>
                                {isActive && (
                                    <div style={{
                                        position: 'absolute', left: 0, top: '50%', transform: 'translateY(-50%)',
                                        width: '4px', height: '60%', background: '#06b6d4',
                                        borderRadius: '0 4px 4px 0', boxShadow: '0 0 10px #06b6d4'
                                    }}></div>
                                )}
                                <span style={{ zIndex: 1, display: 'flex', alignItems: 'center' }}>
                                    {item.icon}
                                </span>
                                <span style={{ zIndex: 1 }}>{item.name}</span>
                            </>
                        )}
                    </NavLink>
                ))}
            </nav>

            <button
                onClick={handleLogout}
                style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '16px',
                    padding: '16px 20px',
                    color: '#ef4444',
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    borderRadius: '12px',
                    fontWeight: '500',
                    marginTop: 'auto',
                    transition: 'all 0.2s',
                    width: '100%',
                    textAlign: 'left',
                    fontSize: '0.95rem'
                }}
                onMouseOver={(e) => {
                    e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                }}
                onMouseOut={(e) => {
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.transform = 'translateY(0)';
                }}
            >
                <LogOut size={20} />
                <span>Logout</span>
            </button>
        </aside>
    );
}
