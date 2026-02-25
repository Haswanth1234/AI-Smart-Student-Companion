import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff, Loader2 } from "lucide-react";
import { login } from "../services/authService"; // Ensure this is imported
import "./ModernAuth.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      // Calling your Python Backend via authService
      const data = await login(email, password);
      
      // Store auth data
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));

      // Redirect based on role
      if (data.user.role === "admin") {
        navigate("/admin/dashboard");
      } else {
        navigate("/student/dashboard");
      }
    } catch (err) {
      setError(err || "Invalid credentials. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modern-auth-container">
      {/* Left Side - Visual/Info */}
      <div className="auth-side-info">
        <h1>Welcome Back.</h1>
        <p>Syncing your academic neural network...</p>
      </div>

      {/* Right Side - Form */}
      <div className="auth-form-section">
        <div className="form-box">
          <h2>Secure Login</h2>
          
          {error && <div className="error-badge">{error}</div>}

          <form className="modern-form" onSubmit={handleLogin}>
            <div className="input-group">
              <input 
                placeholder="Email" 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required 
                disabled={loading} 
              />
            </div>
            
            <div className="password-wrapper">
              <input 
                placeholder="Password" 
                type={showPassword ? "text" : "password"} 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required 
                disabled={loading}
              />
              <button 
                type="button" 
                className="eye-icon" 
                onClick={() => setShowPassword(!showPassword)}
                disabled={loading}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>

            <button type="submit" className="neon-btn" disabled={loading}>
              {loading ? (
                <span className="loader-flex">
                  <Loader2 className="spinner" size={18} />
                  Authenticating...
                </span>
              ) : (
                "Authenticate"
              )}
            </button>
          </form>

          {/* Footer Links */}
          <div className="auth-footer">
            <p className="switch-text">
              New student?{" "}
              <Link to="/register" className="highlight-link">
                Initialize Account
              </Link>
            </p>
            <Link to="/forgot-password" id="forgot-link">
              Forgot Access Credentials?
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}