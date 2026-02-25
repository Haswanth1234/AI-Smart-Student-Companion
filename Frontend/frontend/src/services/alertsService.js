import axios from 'axios';

import API_BASE_URL from './api';
const API_URL = `${API_BASE_URL}/api/student/alerts`;

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    return { headers: { Authorization: `Bearer ${token}` } };
};

export const getAlerts = async () => {
    try {
        const response = await axios.get(API_URL, getAuthHeader());
        return response.data; // Expected { alerts: [] }
    } catch (error) {
        console.error("Alerts fetch error", error);
        return { alerts: [] }; // Fallback
    }
};


