import React, { useEffect, useState } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { getAlerts } from '../services/alertsService';
import { Loader2, Bell, AlertTriangle, Info } from 'lucide-react';

export default function AlertsPage() {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAlerts = async () => {
            try {
                const data = await getAlerts();
                setAlerts(data.alerts || []);
            } catch (err) {
                console.error("Failed to fetch alerts", err);
                setAlerts([]);
            } finally {
                setLoading(false);
            }
        };
        fetchAlerts();
    }, []);

    if (loading) return <div className="flex-center" style={{ height: '100vh' }}><Loader2 className="spinner" /></div>;

    return (
        <DashboardLayout title="Alerts & Notifications">
            <div className="flex-col gap-4">
                {alerts.map(alert => (
                    <div key={alert.id} className="glass-card flex-between" style={{ borderLeft: `4px solid ${alert.type === 'critical' ? 'var(--danger-color)' : alert.type === 'warning' ? 'var(--warning-color)' : 'var(--primary-color)'}` }}>
                        <div className="flex-center gap-4" style={{ justifyContent: 'flex-start' }}>
                            {alert.type === 'critical' ? <AlertTriangle color="var(--danger-color)" /> : <Info color="var(--primary-color)" />}
                            <div>
                                <div className="text-xl mb-1">{alert.message}</div>
                                <div className="text-xs text-secondary">{alert.timestamp}</div>
                            </div>
                        </div>
                    </div>
                ))}
                {alerts.length === 0 && <div className="text-center text-secondary" style={{ padding: '3rem' }}>No new alerts</div>}
            </div>
        </DashboardLayout>
    );
}
