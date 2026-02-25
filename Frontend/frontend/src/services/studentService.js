import axios from "axios";

import API_BASE_URL from './api';
const API_URL = `${API_BASE_URL}/api/student`;

// Get student profile
export const getStudentProfile = async (token) => {
  try {
    const res = await axios.get(`${API_URL}/profile`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return res.data;
  } catch (err) {
    const errorMessage = err.response?.data?.error || "Failed to fetch profile";
    console.error("Get profile error:", errorMessage);
    throw errorMessage;
  }
};

// Update student profile
export const updateStudentProfile = async (profileData, token) => {
  try {
    const res = await axios.put(`${API_URL}/profile`, profileData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });
    return res.data;
  } catch (err) {
    const errorMessage = err.response?.data?.error || "Failed to update profile";
    console.error("Update profile error:", errorMessage);
    throw errorMessage;
  }
};
``


