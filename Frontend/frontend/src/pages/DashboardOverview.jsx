import React, { useEffect, useState } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { getDashboardOverview } from '../services/dashboardService';
import { Loader2, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';

export default function DashboardOverview() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            // Assume endpoint or mock if necessary
            // Ideally backend shd provide this. If 404, we mock structure.
            const result = await getDashboardOverview();
            if (result) {
                // Map backend response to component state
                setData({
                    attendanceArgs: {
                        percentage: result.stats?.attendance || 0,
                        status: (result.stats?.attendance || 0) > 75 ? 'Good' : 'At Risk'
                    },
                    learningLevel: result.stats?.student_type || 'Intermediate Learner',
                    averageMarks: result.stats?.average_marks || 0,
                    pendingTasks: result.stats?.tasks_pending || 0,
                    alertsCount: result.stats?.alerts_unread || 0,
                    aiSummary: `You have ${result.stats?.tasks_pending || 0} pending tasks and ${result.stats?.alerts_unread || 0} unread alerts. Your attendance is at ${result.stats?.attendance || 0}%.`,
                });
            } else {
                // Mock data fallback if backend endpoint isn't ready
                setData({
                    attendanceArgs: { percentage: 85, status: 'Safe' },
                    learningLevel: 'Intermediate',
                    averageMarks: 78,
                    pendingTasks: 4,
                    alertsCount: 2,
                    aiSummary: "You're doing well in assignments, but attendance in 'OS' dropped slightly.",
                });
            }
            setLoading(false);
        };
        fetchData();
    }, []);

    if (loading) return <div className="flex-center" style={{ height: '100vh' }}><Loader2 className="spinner" /></div>;

    // Data for Donut Chart
    const attendanceChartData = [
        { name: 'Present', value: data.attendanceArgs.percentage },
        { name: 'Absent', value: 100 - data.attendanceArgs.percentage }
    ];
    const COLORS = ['#646cff', 'rgba(255, 255, 255, 0.05)'];

    return (
        <DashboardLayout title="Overview">
            {/* AI Summary Card - Highlighted */}
            <div className="glass-card mb-6" style={{
                background: 'linear-gradient(135deg, rgba(100, 108, 255, 0.1) 0%, rgba(100, 108, 255, 0.05) 100%)',
                borderColor: 'rgba(100, 108, 255, 0.3)'
            }}>
                <div className="flex-center mb-2" style={{ justifyContent: 'flex-start', gap: '0.75rem' }}>
                    <TrendingUp size={24} color="var(--primary-color)" />
                    <h3 className="heading-md" style={{ margin: 0 }}>AI Insights</h3>
                </div>
                <p className="text-secondary" style={{ fontSize: '1.1rem', lineHeight: '1.6' }}>
                    {data.aiSummary}
                </p>
            </div>

            <div className="grid-cols-3">
                {/* Attendance Card - Animated Chart */}
                <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '240px' }}>
                    <h4 className="text-secondary mb-2" style={{ margin: 0, width: '100%' }}>Attendance</h4>
                    <div style={{ width: '100%', height: '150px', position: 'relative', minWidth: 0, minHeight: 0 }}>
                        <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
                            <PieChart>
                                <Pie
                                    data={attendanceChartData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={45}
                                    outerRadius={60}
                                    paddingAngle={5}
                                    dataKey="value"
                                    startAngle={90}
                                    endAngle={-270}
                                    animationBegin={0}
                                    animationDuration={1500}
                                >
                                    {attendanceChartData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} cornerRadius={10} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ background: 'rgba(15, 23, 42, 0.9)', border: '1px solid var(--glass-border)', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                        <div style={{
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            textAlign: 'center'
                        }}>
                            <span className="text-xl font-bold" style={{ color: data.attendanceArgs.percentage > 75 ? 'var(--success-color)' : 'var(--danger-color)' }}>
                                {data.attendanceArgs.percentage}%
                            </span>
                        </div>
                    </div>
                    <span className={`badge ${data.attendanceArgs.percentage > 75 ? 'badge-success' : 'badge-danger'}`} style={{ marginTop: '0.5rem' }}>
                        {data.attendanceArgs.status}
                    </span>
                </div>

                {/* Learning Level Card */}
                <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <h4 className="text-secondary mb-4" style={{ margin: 0 }}>Learning Level</h4>
                    <div className="flex-center gap-2" style={{ justifyContent: 'flex-start' }}>
                        <TrendingUp size={32} color="var(--primary-color)" />
                        <span className="text-2xl font-semibold">{data.learningLevel}</span>
                    </div>
                </div>

                {/* Pending Tasks Card */}
                <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <h4 className="text-secondary mb-4" style={{ margin: 0 }}>Pending Tasks</h4>
                    <div className="flex-between">
                        <span className="text-3xl font-bold">{data.pendingTasks}</span>
                        <CheckCircle size={32} color="var(--warning-color)" />
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}
