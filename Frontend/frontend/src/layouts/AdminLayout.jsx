import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import AdminHeader from '../components/AdminHeader';
import '../styles/admin-glass.css';

const AdminLayout = () => {
    const [sidebarOpen, setSidebarOpen] = React.useState(false);

    const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

    return (
        <div className="admin-layout" style={{ width: '100%', minHeight: '100vh', display: 'flex' }}>
            {sidebarOpen && <div className="sidebar-overlay mobile-only" onClick={toggleSidebar}></div>}
            <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
            <main className="admin-content">
                <div style={{ maxWidth: '1600px', width: '100%', margin: '0 auto' }}>
                    <AdminHeader toggleSidebar={toggleSidebar} />
                    <div style={{ padding: '0 1rem' }}>
                        <Outlet />
                    </div>
                </div>
            </main>
        </div>
    );
};

export default AdminLayout;
