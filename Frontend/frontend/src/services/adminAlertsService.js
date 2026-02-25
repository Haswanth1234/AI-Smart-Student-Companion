import axios from 'axios';

import API_BASE_URL from './api';
const API_URL = `${API_BASE_URL}/api/admin`;

export const getAlerts = async () => {
    const token = localStorage.getItem('token');
    try {
        // Fetch real alerts from the new backend endpoint
        const response = await axios.get(`${API_URL}/dashboard/alerts`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error("Failed to fetch alerts:", error);
        throw error; // Re-throw to handle in component
    }
}

export const resolveAlert = async (alertId, notes) => {
    const token = localStorage.getItem('token');
    try {
        const response = await axios.post(`${API_URL}/dashboard/alerts/${alertId}/resolve`,
            { notes },
            { headers: { Authorization: `Bearer ${token}` } }
        );
        return response.data;
    } catch (error) {
        console.error("Failed to resolve alert:", error);
        throw error;
    }
};


