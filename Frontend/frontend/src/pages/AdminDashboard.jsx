import React, { useEffect, useState } from "react";
import {
  Users, CheckCircle, XCircle, AlertTriangle,
  BarChart2, List, Activity, Search, Bell, Download, Calendar, Filter
} from "lucide-react";
import { getDashboardOverview } from "../services/adminDashboardService";
import {
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip as ReTooltip, Legend,
  LineChart, Line, XAxis, YAxis, CartesianGrid
} from "recharts";
import StatCard from "../components/StatCard";
import Sidebar from "../components/Sidebar";
import "../pages/AdminDashboard.css";

const AdminDashboard = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock Data for Visuals (Backend doesn't provide these yet)
  const attendanceTrendData = [
    { date: 'Mon', attendance: 85 },
    { date: 'Tue', attendance: 82 },
    { date: 'Wed', attendance: 88 },
    { date: 'Thu', attendance: 78 },
    { date: 'Fri', attendance: 84 },
    { date: 'Sat', attendance: 90 },
  ];

  const recentAlerts = [
    { id: 1, name: "John Doe", type: "Attendance", date: "2026-02-08", status: "Pending" },
    { id: 2, name: "Jane Smith", type: "Performance", date: "2026-02-07", status: "Resolved" },
    { id: 3, name: "Mike Ross", type: "Attendance", date: "2026-02-06", status: "Pending" },
  ];

  const lowPerformanceStudents = [
    { id: 101, name: "Alex Johnson", attendance: 65, level: "Slow", risk: "High" },
    { id: 102, name: "Sarah Williams", attendance: 72, level: "Slow", risk: "Medium" },
    { id: 103, name: "David Brown", attendance: 68, level: "Intermediate", risk: "High" },
  ];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const result = await getDashboardOverview();
      setData(result);
    } catch (err) {
      const errorMessage = err.message || String(err);
      if (errorMessage.includes("400") || errorMessage.includes("Admin setup incomplete")) {
        setError("Session outdated. Please logout and login again.");
      } else {
        setError(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) return (
    <div className="dashboard-loading">
      <div className="loader"></div>
      <p>Loading Dashboard...</p>
    </div>
  );

  if (error) return (
    <div className="dashboard-error">
      <AlertTriangle size={48} color="#ef4444" />
      <h2>Failed to load data</h2>
      <p>{error}</p>
      <button onClick={() => window.location.reload()} className="retry-btn">Retry</button>
    </div>
  );



  const learningData = [
    { name: 'Slow', value: data.learning_levels.slow, color: '#ef4444' },
    { name: 'Intermediate', value: data.learning_levels.intermediate, color: '#f59e0b' },
    { name: 'Advanced', value: data.learning_levels.advanced, color: '#10b981' },
  ];

  return (
    <div className="app-container">
      <Sidebar isOpen={isSidebarOpen} toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />

      {/* Mobile Overlay */}
      {isSidebarOpen && <div className="sidebar-overlay" onClick={() => setIsSidebarOpen(false)}></div>}

      <main className="main-content">
        {/* Top Header */}
        <header className="top-bar glass-panel">
          <div className="mobile-menu-btn" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
            <List size={24} />
          </div>
          <div className="search-bar">
            <Search size={18} color="#9ca3af" />
            <input type="text" placeholder="Search students, alerts..." />
          </div>

          <div className="top-actions">
            <div className="filter-group">
              <span className="filter-btn"><Calendar size={16} /> This Week</span>
              <span className="filter-btn"><Filter size={16} /> {data.department}</span>
            </div>

            <div className="notification-bell">
              <Bell size={20} />
              <span className="badge">3</span>
            </div>

            <div className="profile-section">
              <div className="admin-profile-icon">A</div>
              <div className="profile-info">
                <span className="name">Admin User</span>
                <span className="role">HOD - {data.department}</span>
              </div>
            </div>
          </div>
        </header>

        <div className="dashboard-content">
          <div className="page-header">
            <div>
              <h1>Dashboard Overview</h1>
              <p className="subtitle">Welcome back, here's what's happening today.</p>
            </div>
            <div className="action-buttons">
              <button className="btn-secondary"><Download size={16} /> Export CSV</button>
              <button className="btn-primary"><Download size={16} /> Download Report</button>
            </div>
          </div>

          {/* 1. Stats Grid */}
          <section className="stats-grid">
            <StatCard icon={Users} label="Total Students" value={data.students.total} color="#3b82f6" />
            <StatCard icon={CheckCircle} label="Present Today" value={data.students.present_today} color="#10b981" />
            <StatCard icon={XCircle} label="Absent Today" value={data.students.absent_today} color="#ef4444" />
            <StatCard icon={Activity} label="Avg Attendance" value={`${data.students.average_attendance}%`} color="#8b5cf6" />
            <StatCard icon={AlertTriangle} label="Below 75%" value={data.students.below_75} color="#f59e0b" />
          </section>

          {/* 2. Charts Row */}
          <section className="charts-row">
            {/* Learning Levels */}
            <div className="chart-card glass-panel">
              <div className="card-header">
                <h3>Learning Levels</h3>
              </div>
              <div className="chart-wrapper" style={{ minWidth: 0, minHeight: 0 }}>
                <ResponsiveContainer width="100%" height={250} minWidth={0} minHeight={0}>
                  <PieChart>
                    <Pie data={learningData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                      {learningData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <ReTooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} itemStyle={{ color: '#fff' }} />
                    <Legend verticalAlign="bottom" height={36} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Attendance Trend */}
            <div className="chart-card glass-panel">
              <div className="card-header">
                <h3>Attendance Trend</h3>
              </div>
              <div className="chart-wrapper" style={{ minWidth: 0, minHeight: 0 }}>
                <ResponsiveContainer width="100%" height={250} minWidth={0} minHeight={0}>
                  <LineChart data={attendanceTrendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="date" stroke="#9ca3af" />
                    <YAxis stroke="#9ca3af" />
                    <ReTooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
                    <Line type="monotone" dataKey="attendance" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </section>

          {/* 3. Tables Row */}
          <section className="tables-row">
            {/* Recent Alerts */}
            <div className="table-card glass-panel">
              <div className="card-header">
                <h3>Recent Alerts</h3>
                <span className="view-all">View All</span>
              </div>
              <div className="table-responsive">
                <table className="glass-table">
                  <thead>
                    <tr>
                      <th>Student</th>
                      <th>Type</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentAlerts.map(alert => (
                      <tr key={alert.id}>
                        <td>{alert.name}</td>
                        <td>
                          <span className={`badge ${alert.type === 'Attendance' ? 'badge-warning' : 'badge-danger'}`}>
                            {alert.type}
                          </span>
                        </td>
                        <td><span className="status-dot"></span> {alert.status}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Performance Watchlist */}
            <div className="table-card glass-panel">
              <div className="card-header">
                <h3>At Risk Students (Low Attendance)</h3>
                <span className="view-all">View All</span>
              </div>
              <div className="table-responsive">
                <table className="glass-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Attendance</th>
                      <th>Risk</th>
                    </tr>
                  </thead>
                  <tbody>
                    {lowPerformanceStudents.map(student => (
                      <tr key={student.id}>
                        <td>{student.name}</td>
                        <td className="text-danger font-bold">{student.attendance}%</td>
                        <td><span className="badge badge-danger">{student.risk}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;