import axios from "axios";
import API_BASE_URL from "./api";

const API_URL = `${API_BASE_URL}/api/admin/dashboard`;

// Helper to get auth header
const getAuthHeader = () => {
    const token = localStorage.getItem("token");
    return token ? { Authorization: `Bearer ${token}` } : {};
};

// Handle unauthorized access (401)
const handleUnauthorized = (error) => {
    if (error.response && error.response.status === 401) {
        // Redirect to login or dispatch logout action
        // For now, let's just clear token and reload/redirect
        localStorage.removeItem("token");
        window.location.href = "/login";
    }
    throw error;
};

export const getDashboardOverview = async () => {
    try {
        const res = await axios.get(`${API_URL}/overview`, {
            headers: getAuthHeader()
        });
        return res.data;
    } catch (err) {
        console.error("Error fetching dashboard overview:", err);
        handleUnauthorized(err);
        throw err.response?.data?.error || "Failed to load dashboard data";
    }
};

// Placeholder functions for other endpoints
export const getStudents = async () => {
    // TODO: Implement actual API call
    return [];
};

export const getAttendance = async () => {
    // TODO: Implement actual API call
    return [];
};

