import axios from "axios";

// ✅ Corrected URL to match your Flask Blueprint setup
const API_URL = "http://localhost:5000/api/auth";

// Login API
export const login = async (email, password) => {
  try {
    const res = await axios.post(`${API_URL}/login`, { email, password });
    return res.data;
  } catch (err) {
    // ✅ Properly scoped error handling
    const errorMessage = 
      err.response?.data?.error || 
      err.response?.data?.message || 
      "Login failed";
    console.error("Login error:", errorMessage);
    throw errorMessage;
  }
};

// Register API
export const register = async (userData) => {
  try {
    const res = await axios.post(`${API_URL}/register`, userData);
    return res.data;
  } catch (err) {
    // ✅ Properly scoped error handling
    const errorMessage = 
      err.response?.data?.error || 
      err.response?.data?.message || 
      "Registration failed";
    console.error("Registration error:", errorMessage);
    throw errorMessage;
  }
};