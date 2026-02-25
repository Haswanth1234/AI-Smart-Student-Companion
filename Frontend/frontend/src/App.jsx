import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import DashboardOverview from "./pages/DashboardOverview";
import StudentProfile from "./pages/StudentProfile";
import TaskPage from "./pages/TaskPage";
import AttendancePage from "./pages/AttendancePage";
import AIChatPage from "./pages/AIChatPage";
import AlertsPage from "./pages/AlertsPage";

// Admin Imports
import AdminLayout from "./layouts/AdminLayout";
import Dashboard from "./pages/admin/Dashboard";
import Students from "./pages/admin/Students";
import StudentDetails from "./pages/admin/StudentDetails"; // IMPORT ADDED
import Attendance from "./pages/admin/Attendance";
import Tasks from "./pages/admin/Tasks";
import Alerts from "./pages/admin/Alerts";
import Reports from "./pages/admin/Reports";
import Settings from "./pages/admin/Settings";

// Components
import AdminPlaceholder from "./components/AdminPlaceholder";

export default function App() {
  const profileCompleted = localStorage.getItem("profileCompleted");

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Student Routes */}
        <Route element={<PrivateRoute allowedRoles={['student']} />}>
          <Route path="/profile" element={<StudentProfile />} />
          <Route path="/student/dashboard" element={<DashboardOverview />} />
          <Route path="/student/tasks" element={<TaskPage />} />
          <Route path="/student/attendance" element={<AttendancePage />} />
          <Route path="/student/ai-chat" element={<AIChatPage />} />
          <Route path="/student/alerts" element={<AlertsPage />} />
        </Route>

        {/* Protected Admin Routes */}
        <Route element={<PrivateRoute allowedRoles={['admin']} />}>
          <Route element={<AdminLayout />}>
            <Route path="/admin/dashboard" element={<Dashboard />} />
            <Route path="/admin/students" element={<Students />} />
            <Route path="/admin/students/:studentId" element={<StudentDetails />} /> {/* ROUTE ADDED */}
            <Route path="/admin/attendance" element={<Attendance />} />
            <Route path="/admin/tasks" element={<Tasks />} />
            <Route path="/admin/alerts" element={<Alerts />} />
            <Route path="/admin/reports" element={<Reports />} />
            <Route path="/admin/settings" element={<Settings />} />
          </Route>
        </Route>

        {/* Redirect logic */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}