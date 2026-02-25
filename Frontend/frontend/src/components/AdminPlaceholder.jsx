import React from 'react';

const AdminPlaceholder = ({ title }) => {
    return (
        <div className="glass-card" style={{ padding: '40px', textAlign: 'center' }}>
            <h1>{title}</h1>
            <p className="text-secondary" style={{ marginTop: '16px' }}>
                This module is under development.
            </p>
        </div>
    );
};

export default AdminPlaceholder;
