import axios from 'axios';

const API_URL = 'http://localhost:5000/api/student/attendance';

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    return { headers: { Authorization: `Bearer ${token}` } };
};

export const getAttendance = async () => {
    try {
        const response = await axios.get(API_URL, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to fetch attendance';
    }
};
