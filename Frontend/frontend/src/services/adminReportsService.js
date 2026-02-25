import axios from "axios";

const API_URL = "http://localhost:5000/api/admin/dashboard";

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
    throw error.response?.data?.error || "Failed to fetch reports data";
};

export const getReportsData = async () => {
    try {
        const res = await axios.get(`${API_URL}/reports`, {
            headers: getAuthHeader()
        });
        return res.data;
    } catch (err) {
        handleError(err);
    }
};
