import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff, Loader2 } from "lucide-react";
import { register } from "../services/authService";
import "./ModernAuth.css";

export default function Register() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [showPass, setShowPass] = useState(false);
  const [error, setError] = useState("");
  
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    roll_number: "",
    department: "",
    college_name: "",
    role: "student" // Default role set to student
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await register(formData);
      navigate("/login");
    } catch (err) {
      setError(err || "Registration failed. Check server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modern-auth-container">
      <div className="auth-side-info">
        <h1>Smart Companion.</h1>
        <p>Initialize your academic neural profile.</p>
      </div>

      <div className="auth-form-section">
        <div className="form-box">
          <div className="step-indicator">Initialization</div>
          <h2>Create Account</h2>
          
          {error && <div className="error-badge">{error}</div>}

          <form className="modern-form" onSubmit={handleRegister}>
            <div className="form-row">
              <input name="name" placeholder="Full Name" onChange={handleChange} required />
              <input name="roll_number" placeholder="Roll Number" onChange={handleChange} required />
            </div>
            
            <input name="email" type="email" placeholder="Institutional Email" onChange={handleChange} required />
            
            <div className="form-row">
              {/* NEW ROLE SELECTION */}
              <select name="role" className="modern-select" onChange={handleChange} value={formData.role}>
                <option value="student">Student</option>
                <option value="admin">Admin</option>
              </select>
              <input name="department" placeholder="Department" onChange={handleChange} required />
            </div>

            <input name="college_name" placeholder="College Name" onChange={handleChange} required />
            
            <div className="password-wrapper">
              <input 
                name="password"
                placeholder="Password" 
                type={showPass ? "text" : "password"} 
                onChange={handleChange}
                required 
              />
              <button type="button" className="eye-icon" onClick={() => setShowPass(!showPass)}>
                {showPass ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>

            <button type="submit" className="neon-btn" disabled={loading}>
              {loading ? (
                <span className="loader-flex">
                  <Loader2 className="spinner" size={18} />
                  Initializing...
                </span>
              ) : "Register Unit"}
            </button>
          </form>

          <div className="auth-footer">
            <p className="switch-text">
              Already initialized? <Link to="/login" className="highlight-link">Sign In</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}