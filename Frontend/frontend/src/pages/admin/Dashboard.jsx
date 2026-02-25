import React, { useEffect, useState } from 'react';
import { Users, UserCheck, UserX, Activity, AlertTriangle, Bell, CheckSquare, ChevronRight, Clock, Calendar } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import StatCard from '../../components/StatCard';
import ChartSection from '../../components/ChartSection';
import Loader from '../../components/Loader';
import { getDashboardOverview } from '../../services/adminDashboardService';

const Dashboard = () => {
    const navigate = useNavigate();
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const dashboardData = await getDashboardOverview();
                setData(dashboardData);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
            <Loader />
        </div>
    );

    if (error) return (
        <div className="glass-card text-danger" style={{ textAlign: 'center', marginTop: '50px' }}>
            <h3>Failed to load dashboard</h3>
            <p>{typeof error === 'string' ? error : error.message || 'Unknown error'}</p>
        </div>
    );

    if (!data) return null;

    // derived for StatCards
    const avgAttendance = data.students.average_attendance;
    const below75 = data.students.below_75;

    return (
        <div className="fade-in">
            {/* 1. Top Summary Cards */}
            <section className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
                <StatCard
                    label="Total Students"
                    value={data.students.total}
                    icon={Users}
                    color="accent"
                />
                <StatCard
                    label="Present Today"
                    value={data.students.present_today}
                    icon={UserCheck}
                    color="success"
                />
                <StatCard
                    label="Absent Today"
                    value={data.students.absent_today}
                    icon={UserX}
                    color="danger"
                />
                <StatCard
                    label="Avg Attendance"
                    value={`${avgAttendance}%`}
                    icon={Activity}
                    color={avgAttendance >= 75 ? 'success' : 'warning'}
                />
                <StatCard
                    label="Below 75%"
                    value={below75}
                    icon={AlertTriangle}
                    color="danger"
                    subLabel="Students at risk"
                />
            </section>

            <div className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
                {/* 2. Learning Level Analytics */}
                <section style={{ marginBottom: 0 }}>
                    <ChartSection data={data.learning_levels} />
                </section>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    {/* 3. Alerts Overview */}
                    <section className="glass-card">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <h3 style={{ margin: 0 }}>Alerts Overview</h3>
                            <div style={{ background: 'rgba(239, 68, 68, 0.2)', padding: '8px', borderRadius: '50%', cursor: 'pointer' }} onClick={() => navigate('/admin/alerts')}>
                                <Bell size={20} className="text-danger" />
                            </div>
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px', textAlign: 'center' }}>
                            <div style={{ background: 'rgba(255,255,255,0.05)', padding: '16px', borderRadius: '12px' }}>
                                <h4 style={{ fontSize: '1.5rem', marginBottom: '4px', margin: 0 }}>{data.alerts.total}</h4>
                                <span className="text-secondary" style={{ fontSize: '0.8rem' }}>Total</span>
                            </div>
                            <div style={{ background: 'rgba(255,255,255,0.05)', padding: '16px', borderRadius: '12px' }}>
                                <h4 className="text-warning" style={{ fontSize: '1.5rem', marginBottom: '4px', margin: 0 }}>{data.alerts.attendance}</h4>
                                <span className="text-secondary" style={{ fontSize: '0.8rem' }}>Attendance</span>
                            </div>
                            <div style={{ background: 'rgba(255,255,255,0.05)', padding: '16px', borderRadius: '12px' }}>
                                <h4 className="text-danger" style={{ fontSize: '1.5rem', marginBottom: '4px', margin: 0 }}>{data.alerts.performance}</h4>
                                <span className="text-secondary" style={{ fontSize: '0.8rem' }}>Performance</span>
                            </div>
                        </div>
                    </section>

                    {/* 4. Tasks Overview */}
                    <section className="glass-card" style={{ flex: 1 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <h3 style={{ margin: 0 }}>Tasks Overview</h3>
                            <div style={{ background: 'rgba(52, 211, 153, 0.2)', padding: '8px', borderRadius: '50%', cursor: 'pointer' }} onClick={() => navigate('/admin/tasks')}>
                                <CheckSquare size={20} className="text-success" />
                            </div>
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                                <span className="text-secondary">Completion Rate</span>
                                <span className="text-success">
                                    {data.tasks.total > 0 ? Math.round((data.tasks.completed / data.tasks.total) * 100) : 0}%
                                </span>
                            </div>
                            <div style={{ height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                                <div style={{
                                    height: '100%',
                                    width: `${data.tasks.total > 0 ? (data.tasks.completed / data.tasks.total) * 100 : 0}%`,
                                    background: 'var(--success-color)',
                                    borderRadius: '4px'
                                }}></div>
                            </div>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--success-color)' }}></div>
                                <div>
                                    <div style={{ fontWeight: 'bold' }}>{data.tasks.completed}</div>
                                    <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Completed</div>
                                </div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--warning-color)' }}></div>
                                <div>
                                    <div style={{ fontWeight: 'bold' }}>{data.tasks.pending}</div>
                                    <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Pending</div>
                                </div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--text-secondary)' }}></div>
                                <div>
                                    <div style={{ fontWeight: 'bold' }}>{data.tasks.total}</div>
                                    <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Total</div>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </div>

            {/* 5. Detailed Lists Row */}
            <div className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px', marginTop: '24px' }}>
                {/* Recent Alerts List */}
                <div className="glass-card" style={{ padding: 0 }}>
                    <div style={{ padding: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                        <h3 style={{ margin: 0 }}>Recent Alerts</h3>
                        <button onClick={() => navigate('/admin/alerts')} style={{ background: 'transparent', border: 'none', color: 'var(--primary-color)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.875rem' }}>
                            View All <ChevronRight size={16} />
                        </button>
                    </div>
                    <div style={{ padding: '8px 0' }}>
                        {data.alerts.recent && data.alerts.recent.length > 0 ? (
                            data.alerts.recent.map((alert, idx) => (
                                <div key={alert._id} style={{
                                    padding: '12px 24px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '16px',
                                    borderBottom: idx === data.alerts.recent.length - 1 ? 'none' : '1px solid rgba(255,255,255,0.03)'
                                }}>
                                    <div style={{
                                        width: '40px', height: '40px', borderRadius: '10px',
                                        background: alert.severity === 'high' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(245, 158, 11, 0.1)',
                                        display: 'flex', alignItems: 'center', justifyContent: 'center'
                                    }}>
                                        <AlertTriangle size={18} className={alert.severity === 'high' ? 'text-danger' : 'text-warning'} />
                                    </div>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
                                            <span style={{ fontWeight: '600', fontSize: '0.95rem' }}>{alert.student_name}</span>
                                            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                                                {new Date(alert.created_at).toLocaleDateString()}
                                            </span>
                                        </div>
                                        <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{alert.type}: {alert.message}</div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>No recent alerts</div>
                        )}
                    </div>
                </div>

                {/* Pending Tasks List */}
                <div className="glass-card" style={{ padding: 0 }}>
                    <div style={{ padding: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                        <h3 style={{ margin: 0 }}>Pending Tasks</h3>
                        <button onClick={() => navigate('/admin/tasks')} style={{ background: 'transparent', border: 'none', color: 'var(--primary-color)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.875rem' }}>
                            View All <ChevronRight size={16} />
                        </button>
                    </div>
                    <div style={{ padding: '8px 0' }}>
                        {data.tasks.recent && data.tasks.recent.length > 0 ? (
                            data.tasks.recent.map((task, idx) => (
                                <div key={task._id} style={{
                                    padding: '12px 24px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '16px',
                                    borderBottom: idx === data.tasks.recent.length - 1 ? 'none' : '1px solid rgba(255,255,255,0.03)'
                                }}>
                                    <div style={{
                                        width: '40px', height: '40px', borderRadius: '10px',
                                        background: 'rgba(6, 182, 212, 0.1)',
                                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                                        color: 'var(--primary-color)'
                                    }}>
                                        <Clock size={18} />
                                    </div>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
                                            <span style={{ fontWeight: '600', fontSize: '0.95rem' }}>{task.title}</span>
                                            <span style={{
                                                fontSize: '0.7rem',
                                                padding: '2px 8px',
                                                borderRadius: '4px',
                                                background: task.priority === 'high' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(245, 158, 11, 0.1)',
                                                color: task.priority === 'high' ? 'var(--danger-color)' : 'var(--warning-color)',
                                                fontWeight: 'bold',
                                                textTransform: 'uppercase'
                                            }}>
                                                {task.priority}
                                            </span>
                                        </div>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{task.student_name}</span>
                                            <span style={{ fontSize: '0.8rem', color: 'var(--primary-color)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                                                <Calendar size={12} /> {new Date(task.due_date).toLocaleDateString()}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>No pending tasks</div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
