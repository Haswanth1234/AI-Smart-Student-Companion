import axios from 'axios';
// We might not have a dedicated aggregator endpoint in backend, 
// so this service can either call a new endpoint or be a place to aggregate multiple calls.
// For now, let's assume we fetch from individual services in the component or have a dedicated endpoint.
// The user request mentioned: GET /api/student/dashboard/overview
// I will attempt to hit that, if 404, we handle gracefully.

const API_URL = 'http://localhost:5000/api/student/dashboard/overview';

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    return { headers: { Authorization: `Bearer ${token}` } };
};

export const getDashboardOverview = async () => {
    try {
        const response = await axios.get(API_URL, getAuthHeader());
        return response.data;
    } catch (error) {
        // If 404, we might need to fallback to client-side aggregation
        // But for now, let's return null or throw to let component handle
        console.warn("Dashboard overview endpoint not found or failed", error);
        return null;
    }
};
