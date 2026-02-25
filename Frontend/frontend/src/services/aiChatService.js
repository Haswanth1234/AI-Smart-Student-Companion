import axios from 'axios';

import API_BASE_URL from './api';
const API_URL = `${API_BASE_URL}/api/student/ai/chat`;

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    return { headers: { Authorization: `Bearer ${token}` } };
};

export const sendMessage = async (message) => {
    try {
        const response = await axios.post(API_URL, { message }, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'AI service unavailable';
    }
};

export const getChatHistory = async () => {
    // Mocking history if API doesn't exist yet, or call actual endpoint if available
    // Assuming GET /api/student/ai/history might exist in future
    return [];
};


