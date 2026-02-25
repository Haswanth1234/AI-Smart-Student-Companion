import React, { useState, useEffect } from 'react';
import { AlertTriangle, CheckCircle, Clock, Search, Filter, Bell } from 'lucide-react';
import { getAlerts, resolveAlert } from '../../services/adminAlertsService';
import Loader from '../../components/Loader';
import { X } from 'lucide-react';

const Alerts = () => {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState('all'); // all, pending, resolved
    const [searchTerm, setSearchTerm] = useState('');

    // Modal State
    const [selectedAlert, setSelectedAlert] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [resolutionNotes, setResolutionNotes] = useState('');
    const [resolving, setResolving] = useState(false);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            setLoading(true);
            const data = await getAlerts();
            setAlerts(data);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'high': return 'var(--danger-color)';
            case 'medium': return 'var(--warning-color)';
            case 'low': return 'var(--success-color)'; // or info color
            default: return 'var(--text-secondary)';
        }
    };

    const handleViewAlert = (alert) => {
        setSelectedAlert(alert);
        setResolutionNotes(alert.resolution_notes || '');
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setSelectedAlert(null);
        setResolutionNotes('');
    };

    const handleResolve = async () => {
        if (!selectedAlert) return;

        try {
            setResolving(true);
            await resolveAlert(selectedAlert._id, resolutionNotes);

            // Update local state
            setAlerts(prev => prev.map(a =>
                a._id === selectedAlert._id
                    ? { ...a, status: 'resolved', resolution_notes: resolutionNotes }
                    : a
            ));

            handleCloseModal();
        } catch (err) {
            setError(err);
        } finally {
            setResolving(false);
        }
    };

    const filteredAlerts = alerts.filter(alert => {
        const matchesSearch =
            alert.student_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            alert.type.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesFilter = filter === 'all' || alert.status === filter;

        return matchesSearch && matchesFilter;
    });

    if (loading) return <div className="flex-center" style={{ height: '80vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}><Loader /></div>;

    return (
        <div className="fade-in">
            <header style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '2rem', marginBottom: '8px' }}>System Alerts</h1>
                <p className="text-secondary">Monitor and resolve student-related alerts.</p>

                <div style={{ marginTop: '24px', display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between' }}>
                    {/* Search Bar */}
                    <div style={{ position: 'relative', minWidth: '320px', flex: '1 1 auto' }}>
                        <Search size={20} className="text-secondary" style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)' }} />
                        <input
                            type="text"
                            placeholder="Search alerts..."
                            className="glass-input"
                            style={{ paddingLeft: '48px', width: '100%' }}
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    {/* Filter Buttons */}
                    <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                        <select
                            value={filter}
                            onChange={(e) => setFilter(e.target.value)}
                            className="glass-input"
                            style={{ width: 'auto', minWidth: '160px' }}
                        >
                            <option value="all" style={{ background: '#1a1a2e' }}>All Alerts</option>
                            <option value="pending" style={{ background: '#1a1a2e' }}>Pending</option>
                            <option value="resolved" style={{ background: '#1a1a2e' }}>Resolved</option>
                        </select>
                    </div>
                </div>
            </header>

            {/* Statistics Row (Derived from local data for now) */}
            <div className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
                <div className="glass-card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                        <span className="text-secondary" style={{ fontSize: '0.875rem' }}>Total Alerts</span>
                        <Bell size={16} className="text-secondary" />
                    </div>
                    <h3 style={{ fontSize: '1.75rem' }}>{alerts.length}</h3>
                </div>
                <div className="glass-card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                        <span className="text-secondary" style={{ fontSize: '0.875rem' }}>High Severity</span>
                        <AlertTriangle size={16} className="text-danger" />
                    </div>
                    <h3 style={{ fontSize: '1.75rem' }} className="text-danger">
                        {alerts.filter(a => a.severity === 'high').length}
                    </h3>
                </div>
                <div className="glass-card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                        <span className="text-secondary" style={{ fontSize: '0.875rem' }}>Pending</span>
                        <Clock size={16} className="text-warning" />
                    </div>
                    <h3 style={{ fontSize: '1.75rem' }} className="text-warning">
                        {alerts.filter(a => a.status === 'pending').length}
                    </h3>
                </div>
            </div>

            <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
                <div style={{ overflowX: 'auto' }}>
                    <table className="glass-table">
                        <thead>
                            <tr>
                                <th>Alert Details</th>
                                <th>Student</th>
                                <th>Date</th>
                                <th className="text-center" style={{ textAlign: 'center' }}>Severity</th>
                                <th className="text-center" style={{ textAlign: 'center' }}>Status</th>
                                <th className="text-center" style={{ textAlign: 'center' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredAlerts.length > 0 ? (
                                filteredAlerts.map((alert) => (
                                    <tr key={alert._id}>
                                        <td>
                                            <div style={{ fontWeight: '500', marginBottom: '4px' }}>{alert.type}</div>
                                            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{alert.message}</div>
                                        </td>
                                        <td>
                                            <div style={{ fontWeight: '500' }}>{alert.student_name}</div>
                                            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{alert.student_roll}</div>
                                        </td>
                                        <td>
                                            <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                                                {new Date(alert.created_at || alert.date).toLocaleDateString()}
                                            </div>
                                        </td>
                                        <td style={{ textAlign: 'center' }}>
                                            <span style={{
                                                padding: '4px 12px',
                                                borderRadius: '20px',
                                                fontSize: '0.75rem',
                                                fontWeight: '600',
                                                background: `rgba(var(--${alert.severity === 'high' ? 'danger' : alert.severity === 'medium' ? 'warning' : 'success'}-rgb), 0.1)`,
                                                /* Fallback to simple colors if RGB vars aren't set */
                                                backgroundColor: alert.severity === 'high' ? 'rgba(239, 68, 68, 0.15)' : alert.severity === 'medium' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(16, 185, 129, 0.15)',
                                                color: getSeverityColor(alert.severity),
                                                textTransform: 'uppercase',
                                                letterSpacing: '0.05em',
                                                border: `1px solid ${getSeverityColor(alert.severity)}`
                                            }}>
                                                {alert.severity}
                                            </span>
                                        </td>
                                        <td style={{ textAlign: 'center' }}>
                                            {alert.status === 'resolved' ? (
                                                <span className="text-success" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontWeight: '500' }}>
                                                    <CheckCircle size={14} /> Resolved
                                                </span>
                                            ) : (
                                                <span className="text-warning" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontWeight: '500' }}>
                                                    <Clock size={14} /> Pending
                                                </span>
                                            )}
                                        </td>
                                        <td style={{ textAlign: 'center' }}>
                                            <button
                                                className="btn-primary"
                                                style={{ padding: '6px 16px', fontSize: '0.8rem', borderRadius: '8px' }}
                                                onClick={() => handleViewAlert(alert)}
                                            >
                                                View
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>
                                        No alerts found.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
            {/* Resolution Modal */}
            {showModal && selectedAlert && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)',
                    display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000
                }}>
                    <div className="glass-card" style={{ width: '90%', maxWidth: '500px', maxHeight: '90vh', overflowY: 'auto', position: 'relative' }}>
                        <button
                            onClick={handleCloseModal}
                            style={{ position: 'absolute', right: '16px', top: '16px', background: 'transparent', border: 'none', color: 'white', cursor: 'pointer' }}
                        >
                            <X size={20} />
                        </button>

                        <h2 style={{ marginBottom: '16px', fontSize: '1.5rem' }}>Alert Details</h2>

                        <div style={{ marginBottom: '20px' }}>
                            <div style={{ marginBottom: '8px' }}>
                                <span className="text-secondary" style={{ fontSize: '0.85rem' }}>Type</span>
                                <div style={{ fontWeight: '500' }}>{selectedAlert.type || selectedAlert.alert_type}</div>
                            </div>
                            <div style={{ marginBottom: '8px' }}>
                                <span className="text-secondary" style={{ fontSize: '0.85rem' }}>Student</span>
                                <div style={{ fontWeight: '500' }}>{selectedAlert.student_name} ({selectedAlert.student_roll})</div>
                            </div>
                            <div style={{ marginBottom: '8px' }}>
                                <span className="text-secondary" style={{ fontSize: '0.85rem' }}>Message</span>
                                <div style={{ background: 'rgba(255,255,255,0.05)', padding: '12px', borderRadius: '8px', marginTop: '4px' }}>
                                    {selectedAlert.message}
                                </div>
                            </div>
                        </div>

                        <div style={{ borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '20px' }}>
                            <h3 style={{ fontSize: '1.1rem', marginBottom: '12px' }}>Resolution</h3>

                            {selectedAlert.status === 'resolved' ? (
                                <div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--success-color)', marginBottom: '12px' }}>
                                        <CheckCircle size={18} />
                                        <span style={{ fontWeight: 'bold' }}>Resolved</span>
                                    </div>
                                    <div style={{ marginBottom: '8px' }}>
                                        <span className="text-secondary" style={{ fontSize: '0.85rem' }}>Notes</span>
                                        <div style={{ marginTop: '4px' }}>{selectedAlert.resolution_notes || 'No notes provided.'}</div>
                                    </div>
                                </div>
                            ) : (
                                <div>
                                    <div style={{ marginBottom: '16px' }}>
                                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem' }}>Resolution Notes</label>
                                        <textarea
                                            className="glass-input"
                                            rows="3"
                                            placeholder="Describe how this issue was resolved..."
                                            value={resolutionNotes}
                                            onChange={(e) => setResolutionNotes(e.target.value)}
                                            style={{ width: '100%', resize: 'vertical' }}
                                        ></textarea>
                                    </div>

                                    <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                                        <button className="btn glass-card" onClick={handleCloseModal}>Cancel</button>
                                        <button
                                            className="btn btn-primary"
                                            onClick={handleResolve}
                                            disabled={resolving}
                                        >
                                            {resolving ? 'Saving...' : 'Mark as Resolved'}
                                        </button>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )
            }
        </div >
    );
};

export default Alerts;
