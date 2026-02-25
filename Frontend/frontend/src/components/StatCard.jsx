import React from 'react';
import { ArrowUp, ArrowDown, Minus } from 'lucide-react';

const StatCard = ({ icon: Icon, label, value, subLabel, color }) => {
    return (
        <div className="glass-card stat-card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            {Icon && (
                <div style={{
                    padding: '12px',
                    borderRadius: '12px',
                    background: 'rgba(255,255,255,0.1)',
                    color: color === 'danger' ? 'var(--danger-color)' :
                        color === 'success' ? 'var(--success-color)' :
                            color === 'warning' ? 'var(--warning-color)' : 'var(--accent-color)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    <Icon size={28} />
                </div>
            )}
            <div>
                <p className="text-secondary" style={{ margin: 0, fontSize: '0.9rem' }}>{label}</p>
                <h3 style={{ margin: '4px 0 0 0', fontSize: '1.8rem' }}>{value}</h3>
                {subLabel && <p className="text-secondary" style={{ fontSize: '0.75rem', marginTop: '4px' }}>{subLabel}</p>}
            </div>
        </div>
    );
};

export default StatCard;
