// Centralized API Base URL
// In development, this will be http://localhost:5000
// In production (Vercel), this will be your Render URL
// Make sure to add VITE_API_URL in your Vercel Environment Variables

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

// Ensure there's no trailing slash to avoid double slashes in paths
const API_BASE_URL = BASE_URL.endsWith('/') ? BASE_URL.slice(0, -1) : BASE_URL;

export default API_BASE_URL;
