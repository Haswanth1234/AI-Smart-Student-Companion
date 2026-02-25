import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

export default function DashboardLayout({ children, title }) {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <div className="dashboard-layout">
            <div
                className={`overlay ${sidebarOpen ? 'visible' : ''}`}
                onClick={() => setSidebarOpen(false)}
            />
            <Sidebar isOpen={sidebarOpen} />
            <main className="main-content">
                <Header title={title} onMenuClick={() => setSidebarOpen(true)} />
                {children}
            </main>
        </div>
    );
}
