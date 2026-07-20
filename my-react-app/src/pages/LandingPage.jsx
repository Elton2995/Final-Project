import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mail, Lock, CheckCircle, MessageSquare, BarChart3, Users } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const LandingPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Check for registration success message from location state
  useEffect(() => {
    if (location.state?.registrationSuccess) {
      setSuccessMessage(`Account created successfully! Please sign in with ${location.state.email || 'your email'}.`);
      // Clear the state so message doesn't show again on refresh
      window.history.replaceState({}, document.title);
    }
  }, [location]);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    setIsLoading(true);

    try {
      const result = await login(email, password);
      
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.error || 'Login failed. Please try again.');
        setIsLoading(false);
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('An error occurred. Please try again.');
      setIsLoading(false);
    }
  };

  // Feature cards data
  const features = [
    {
      icon: <CheckCircle className="text-primary" size={24} />,
      title: 'Submit & Track Complaints',
      description: 'Submit complaints in real-time and track their progress from submission to resolution.'
    },
    {
      icon: <MessageSquare className="text-primary" size={24} />,
      title: 'Direct Staff Messaging',
      description: 'Communicate directly with customer service staff for faster issue resolution.'
    },
    {
      icon: <BarChart3 className="text-primary" size={24} />,
      title: 'Admin Reports & Insights',
      description: 'Get comprehensive reports and performance insights to improve service quality.'
    }
  ];

  return (
    <div className="min-vh-100 d-flex align-items-center bg-light">
      <div className="container py-5">
        <div className="row g-0 shadow-lg rounded-4 overflow-hidden bg-white">
          {/* Left Section - Branding */}
          <motion.div 
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="col-lg-6 d-none d-lg-flex flex-column justify-content-center p-5 bg-primary bg-gradient text-white"
            style={{ minHeight: '600px' }}
          >
            <div className="mb-4">
              <h1 className="display-3 fw-bold mb-3">ServiceDesk</h1>
              <p className="lead fs-4 opacity-75">Customer service, made simple.</p>
            </div>
            
            <p className="fs-5 mb-4">
              A unified platform for small businesses to manage complaints, requests, and customer feedback.
            </p>

            <ul className="list-unstyled">
              {features.map((feature, index) => (
                <motion.li 
                  key={index}
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.2 * (index + 1) }}
                  className="d-flex align-items-start mb-3"
                >
                  <span className="me-3 bg-white bg-opacity-25 p-2 rounded-circle">
                    {feature.icon}
                  </span>
                  <div>
                    <h6 className="fw-bold mb-1">{feature.title}</h6>
                    <p className="small opacity-75 mb-0">{feature.description}</p>
                  </div>
                </motion.li>
              ))}
            </ul>

            <div className="mt-4">
              <div className="d-flex align-items-center gap-4 small">
                <span className="d-flex align-items-center">
                  <Users size={16} className="me-1" /> 500+ Users
                </span>
                <span className="d-flex align-items-center">
                  <CheckCircle size={16} className="me-1" /> 98% Satisfaction
                </span>
              </div>
            </div>
          </motion.div>

          {/* Right Section - Login Form */}
          <motion.div 
            initial={{ x: 50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="col-lg-6 d-flex align-items-center p-4 p-md-5"
          >
            <div className="w-100">
              <div className="text-center mb-4 d-lg-none">
                <h2 className="fw-bold text-primary">ServiceDesk</h2>
                <p className="text-muted">Customer service, made simple.</p>
              </div>

              <h2 className="fw-bold mb-1">Welcome back</h2>
              <p className="text-muted mb-4">Sign in to your account to continue</p>

              {successMessage && (
                <div className="alert alert-success d-flex align-items-center gap-2" role="alert">
                  <CheckCircle size={18} />
                  {successMessage}
                </div>
              )}

              {error && (
                <div className="alert alert-danger d-flex align-items-center gap-2" role="alert">
                  <span>⚠️</span>
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label fw-semibold">
                    Email address
                  </label>
                  <div className="input-group">
                    <span className="input-group-text bg-light border-end-0">
                      <Mail size={18} className="text-muted" />
                    </span>
                    <input
                      type="email"
                      className="form-control border-start-0 ps-0"
                      id="email"
                      placeholder="you@example.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label htmlFor="password" className="form-label fw-semibold">
                    Password
                  </label>
                  <div className="input-group">
                    <span className="input-group-text bg-light border-end-0">
                      <Lock size={18} className="text-muted" />
                    </span>
                    <input
                      type="password"
                      className="form-control border-start-0 ps-0"
                      id="password"
                      placeholder="Enter your password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="d-flex justify-content-between align-items-center mb-4">
                  <div className="form-check">
                    <input
                      type="checkbox"
                      className="form-check-input"
                      id="rememberMe"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                    />
                    <label className="form-check-label small" htmlFor="rememberMe">
                      Remember me
                    </label>
                  </div>
                  <Link to="/forgot-password" className="text-decoration-none small">
                    Forgot password?
                  </Link>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary w-100 py-2 fw-semibold"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" />
                      Signing in...
                    </>
                  ) : (
                    'Sign in'
                  )}
                </button>
              </form>

              <div className="text-center mt-4">
                <p className="small text-muted mb-0">
                  New to ServiceDesk?{' '}
                  <Link to="/register" className="text-decoration-none fw-semibold">
                    Create one →
                  </Link>
                </p>
              </div>

              <div className="text-center mt-4 pt-3 border-top">
                <p className="small text-muted mb-0">
                  © 2025 ServiceDesk - Elton Mallya Final Year Project
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;