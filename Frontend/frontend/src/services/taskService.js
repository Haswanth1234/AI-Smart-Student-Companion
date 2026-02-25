import axios from 'axios';

const API_URL = 'http://localhost:5000/api/student/tasks';

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    return { headers: { Authorization: `Bearer ${token}` } };
};

export const getTasks = async () => {
    try {
        const response = await axios.get(API_URL, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to fetch tasks';
    }
};

export const createTask = async (taskData) => {
    try {
        const response = await axios.post(API_URL, taskData, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to create task';
    }
};

export const updateTask = async (taskId, updates) => {
    try {
        const response = await axios.put(`${API_URL}/${taskId}`, updates, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to update task';
    }
};

export const deleteTask = async (taskId) => {
    try {
        const response = await axios.delete(`${API_URL}/${taskId}`, getAuthHeader());
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to delete task';
    }
};
