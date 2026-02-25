import axios from "axios";

import API_BASE_URL from './api';
const API_URL = `${API_BASE_URL}/api/admin`;

// Helper to get auth header
const getAuthHeader = () => {
    const token = localStorage.getItem("token");
    return token ? { Authorization: `Bearer ${token}` } : {};
};

// Handle unauthorized access or errors
const handleError = (error) => {
    if (error.response && error.response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/login";
    }
    throw error.response?.data?.error || "An error occurred";
};

export const getAdminProfile = async () => {
    try {
        const res = await axios.get(`${API_URL}/profile`, {
            headers: getAuthHeader()
        });
        return res.data;
    } catch (err) {
        handleError(err);
    }
};

export const changeAdminPassword = async (currentPassword, newPassword) => {
    try {
        const res = await axios.post(`${API_URL}/change-password`,
            { current_password: currentPassword, new_password: newPassword },
            { headers: getAuthHeader() }
        );
        return res.data;
    } catch (err) {
        throw err.response?.data?.error || "Failed to change password";
    }
};


