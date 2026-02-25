import axios from 'axios';

import API_BASE_URL from './api';
const API_URL = `${API_BASE_URL}/api/admin/attendance`;

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    return { headers: { Authorization: `Bearer ${token}` } };
};

export const getAttendanceSummary = async () => {
    try {
        const response = await axios.get(`${API_URL}/summary`, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to fetch attendance summary';
    }
};

export const markAttendance = async (studentId, date, status) => {
    try {
        const response = await axios.post(`${API_URL}/mark`, {
            student_id: studentId,
            date,
            status
        }, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to mark attendance';
    }
};


