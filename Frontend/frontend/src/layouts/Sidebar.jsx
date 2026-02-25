import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
    LayoutDashboard,
    UserCircle,
    ClipboardCheck,
    ListTodo,
    Bot,
    Bell,
    LogOut
} from 'lucide-react';

export default function Sidebar({ isOpen }) {
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
    };

    const navItems = [
        { name: 'Overview', path: '/student/dashboard', icon: <LayoutDashboard size={20} /> },
        { name: 'Profile', path: '/profile', icon: <UserCircle size={20} /> },
        { name: 'Attendance', path: '/student/attendance', icon: <ClipboardCheck size={20} /> },
        { name: 'Tasks', path: '/student/tasks', icon: <ListTodo size={20} /> },
        { name: 'AI Chat', path: '/student/ai-chat', icon: <Bot size={20} /> },
        { name: 'Alerts', path: '/student/alerts', icon: <Bell size={20} /> },
    ];

    return (
        <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
            <div className="flex-center mb-6 gap-2">
                <div style={{
                    width: '32px', height: '32px',
                    background: 'linear-gradient(45deg, #646cff, #a5b4fc)',
                    borderRadius: '8px'
                }}></div>
                <h2 className="heading-md" style={{ margin: 0, fontSize: '1.25rem' }}>AI Companion</h2>
            </div>

            <div className="user-badge">
                <div style={{
                    width: '40px', height: '40px', borderRadius: '50%',
                    background: '#4ade80', display: 'flex', alignItems: 'center', justifyContent: 'center',
                    color: '#000', fontWeight: 'bold'
                }}>
                    {user.name ? user.name.charAt(0).toUpperCase() : 'S'}
                </div>
                <div style={{ overflow: 'hidden' }}>
                    <div className="font-semibold text-primary" style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {user.name || 'Student'}
                    </div>
                    <div className="text-xs text-secondary">
                        {user.department || 'Dept'}
                    </div>
                </div>
            </div>

            <nav style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                        end={item.path === '/student/dashboard'}
                    >
                        {item.icon}
                        <span>{item.name}</span>
                    </NavLink>
                ))}
            </nav>
        </aside>
    );
}
