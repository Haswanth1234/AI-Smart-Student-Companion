import React, { useEffect, useState } from "react";
import "./Profile.css";

export default function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const savedUser = JSON.parse(localStorage.getItem("user"));
    setUser(savedUser);
  }, []);

  if (!user) return <div className="loading">Loading Profile...</div>;

  return (
    <div className={`profile-wrapper ${user.role}-theme`}>
      <div className="glass-card profile-card">
        {user.role === "admin" ? <AdminProfile user={user} /> : <StudentProfile user={user} />}
      </div>
    </div>
  );
}

// Student View
const StudentProfile = ({ user }) => (
  <div className="profile-content">
    <div className="badge">Student Companion</div>
    <h2>Welcome, {user.name} 👋</h2>
    <div className="stats-grid">
      <div className="stat-item"><h4>Department</h4><p>{user.department}</p></div>
      <div className="stat-item"><h4>University</h4><p>{user.college_name}</p></div>
    </div>
    <button className="ai-btn">Launch AI Tutor</button>
  </div>
);

// Admin View
const AdminProfile = ({ user }) => (
  <div className="profile-content">
    <div className="badge admin-badge">System Administrator</div>
    <h2>Admin Dashboard: {user.name}</h2>
    <div className="admin-controls">
      <button className="control-btn">Manage Students</button>
      <button className="control-btn">System Analytics</button>
    </div>
  </div>
);