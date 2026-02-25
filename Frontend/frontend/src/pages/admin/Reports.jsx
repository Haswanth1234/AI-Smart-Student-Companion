import React, { useState, useEffect } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    PieChart, Pie, Cell
} from 'recharts';
import {
    FileText,
    Download,
    TrendingUp,
    Users,
    AlertTriangle,
    CheckCircle
} from 'lucide-react';
import { getReportsData } from '../../services/adminReportsService';

const Reports = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            setLoading(true);
            const response = await getReportsData();
            setData(response);
            setError(null);
        } catch (err) {
            console.error("Failed to fetch reports:", err);
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    const handleExport = () => {
        // Simple mock export
        alert("Export functionality would generate a PDF/CSV here.");
    };

    if (loading) {
        return (
            <div className="flex-center" style={{ height: '400px', color: 'var(--text-secondary)' }}>
                <div className="animate-spin" style={{ marginRight: '10px' }}>⌛</div> Loading reports data...
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ padding: '24px', color: 'var(--danger-color)', textAlign: 'center' }}>
                <h3>Error loading reports</h3>
                <p>{error}</p>
                <button
                    onClick={fetchData}
                    className="btn btn-primary"
                    style={{ marginTop: '12px' }}
                >
                    Retry
                </button>
            </div>
        );
    }

    // Colors for Pie Chart
    const COLORS = ['#06b6d4', '#f59e0b', '#ef4444'];

    return (
        <div className="main-content fade-in">
            {/* Header */}
            <div className="flex-between mb-6">
                <div>
                    <h1 className="heading-lg flex-center gap-2" style={{ marginBottom: '8px' }}>
                        <FileText size={32} color="var(--primary-color)" />
                        Reports & Analytics
                    </h1>
                    <p className="text-secondary">
                        Comprehensive overview of student performance and attendance.
                    </p>
                </div>
                <button
                    onClick={handleExport}
                    className="btn glass-card flex-center gap-2"
                    style={{
                        padding: '10px 20px',
                        background: 'rgba(6, 182, 212, 0.1)',
                        color: 'var(--primary-color)',
                        border: '1px solid rgba(6, 182, 212, 0.2)',
                        cursor: 'pointer',
                        transition: 'all 0.2s'
                    }}
                >
                    <Download size={18} />
                    Export Report
                </button>
            </div>

            {/* Content Grid */}
            <div className="reports-grid" style={{ display: 'grid', gap: '24px' }}>

                {/* 1. Attendance Trend Chart */}
                <div className="glass-card attendance-chart">
                    <div className="flex-between mb-4">
                        <h3 className="heading-md flex-center gap-2">
                            <TrendingUp size={20} color="var(--primary-color)" />
                            Weekly Attendance Trend
                        </h3>
                        <div className="text-secondary" style={{ fontSize: '0.9rem' }}>Last 7 Days</div>
                    </div>

                    <div className="chart-container-lg" style={{ minWidth: 0, minHeight: 0 }}>
                        <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
                            <BarChart data={data?.attendance_trend || []}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                                <XAxis
                                    dataKey="date"
                                    stroke="#94a3b8"
                                    tick={{ fill: '#94a3b8' }}
                                    axisLine={false}
                                    tickLine={false}
                                />
                                <YAxis
                                    stroke="#94a3b8"
                                    tick={{ fill: '#94a3b8' }}
                                    axisLine={false}
                                    tickLine={false}
                                />
                                <Tooltip
                                    contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', color: '#f1f5f9' }}
                                    cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }}
                                />
                                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                                <Bar name="Present" dataKey="present" fill="#06b6d4" radius={[4, 4, 0, 0]} barSize={40} />
                                <Bar name="Absent" dataKey="absent" fill="#ef4444" radius={[4, 4, 0, 0]} barSize={40} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* 2. Performance Distribution */}
                <div className="glass-card performance-chart">
                    <h3 className="heading-md flex-center gap-2 mb-6">
                        <Users size={20} color="#f59e0b" />
                        Performance Distribution
                    </h3>

                    <div className="chart-container-lg flex-center" style={{ minWidth: 0, minHeight: 0 }}>
                        <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
                            <PieChart>
                                <Pie
                                    data={data?.performance_distribution || []}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={70}
                                    outerRadius={90}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {data?.performance_distribution?.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color || COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }} />
                                <Legend verticalAlign="bottom" height={36} />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* 3. At Risk Students Table */}
                <div className="glass-card risk-table" style={{ minHeight: '350px' }}>
                    <div className="flex-between mb-4">
                        <h3 className="heading-md flex-center gap-2">
                            <AlertTriangle size={20} color="var(--danger-color)" />
                            At-Risk Students
                        </h3>
                        <span className="badge badge-danger">
                            Low Attendance
                        </span>
                    </div>

                    <div style={{ overflowX: 'auto' }}>
                        <table className="glass-table">
                            <thead>
                                <tr>
                                    <th>Student</th>
                                    <th>Roll No</th>
                                    <th style={{ textAlign: 'center' }}>Attendance</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data?.at_risk_students?.length > 0 ? (
                                    data.at_risk_students.map((student) => (
                                        <tr key={student._id}>
                                            <td>
                                                <div style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{student.name}</div>
                                            </td>
                                            <td style={{ color: 'var(--text-secondary)' }}>
                                                {student.roll_number}
                                            </td>
                                            <td style={{ textAlign: 'center' }}>
                                                <span className="badge badge-danger">
                                                    {student.attendance}%
                                                </span>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="3" className="text-center text-secondary" style={{ padding: '24px' }}>
                                            No at-risk students found.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* 4. Top Performers Table */}
                <div className="glass-card performers-table" style={{ minHeight: '350px' }}>
                    <div className="flex-between mb-4">
                        <h3 className="heading-md flex-center gap-2">
                            <CheckCircle size={20} color="var(--success-color)" />
                            Top Performers
                        </h3>
                        <span className="badge badge-success">
                            High Avg. Marks
                        </span>
                    </div>

                    <div style={{ overflowX: 'auto' }}>
                        <table className="glass-table">
                            <thead>
                                <tr>
                                    <th>Student</th>
                                    <th style={{ textAlign: 'center' }}>Attendance</th>
                                    <th style={{ textAlign: 'center' }}>Avg Marks</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data?.top_performers?.length > 0 ? (
                                    data.top_performers.map((student) => (
                                        <tr key={student._id}>
                                            <td>
                                                <div style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{student.name}</div>
                                            </td>
                                            <td style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                                                {student.attendance}%
                                            </td>
                                            <td style={{ textAlign: 'center' }}>
                                                <span className="badge badge-success">
                                                    {student.avg_marks}
                                                </span>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="3" className="text-center text-secondary" style={{ padding: '24px' }}>
                                            No top performers data available.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Reports;
