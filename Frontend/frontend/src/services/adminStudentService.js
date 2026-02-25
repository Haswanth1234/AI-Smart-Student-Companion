import axios from 'axios';

const API_URL = 'http://localhost:5000/api/admin';

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    return { headers: { Authorization: `Bearer ${token}` } };
};

export const getStudentsList = async () => {
    try {
        const response = await axios.get(`${API_URL}/students`, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to fetch students list';
    }
};

export const getStudentDetails = async (studentId) => {
    try {
        const response = await axios.get(`${API_URL}/students/${studentId}`, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to fetch student details';
    }
};
