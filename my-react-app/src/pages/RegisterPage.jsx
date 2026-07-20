import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Mail, 
  Lock, 
  User, 
  Phone, 
  CheckCircle, 
  MessageSquare, 
  BarChart3, 
  Users,
  Eye,
  EyeOff,
  AlertCircle
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const RegisterPage = () => {
  const navigate = useNavigate();
  const { register, isAuthenticated } = useAuth();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    agreeTerms: false
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState('');
  const [registrationSuccess, setRegistrationSuccess] = useState(false);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

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

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    if (submitError) {
      setSubmitError('');
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.fullName.trim()) {
      newErrors.fullName = 'Full name is required';
    } else if (formData.fullName.length < 3) {
      newErrors.fullName = 'Name must be at least 3 characters';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^\+?[\d\s-]{10,}$/.test(formData.phone.replace(/\s/g, ''))) {
      newErrors.phone = 'Please enter a valid phone number';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }
    
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    if (!formData.agreeTerms) {
      newErrors.agreeTerms = 'You must agree to the terms and conditions';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');
    setRegistrationSuccess(false);
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      console.log('Registration form submitted');
      
      // In a real app, this would call your API to create the user
      // For now, we'll just simulate a successful registration
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Store registration info (but don't log in yet)
      // This is just to remember that the user just registered
      localStorage.setItem('registrationEmail', formData.email);
      
      // Set success state
      setRegistrationSuccess(true);
      
      // Redirect to login page after showing success message
      setTimeout(() => {
        navigate('/login', { 
          state: { 
            registrationSuccess: true, 
            email: formData.email 
          } 
        });
      }, 2000);
      
    } catch (err) {
      console.error('Registration error:', err);
      setSubmitError('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // If registration is successful, show success message
  if (registrationSuccess) {
    return (
      <div className="min-vh-100 d-flex align-items-center bg-light">
        <div className="container py-5">
          <div className="row g-0 shadow-lg rounded-4 overflow-hidden bg-white">
            <div className="col-12 p-5 text-center">
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.5 }}
              >
                <div className="bg-success bg-opacity-10 p-4 rounded-circle d-inline-block mb-4">
                  <CheckCircle size={64} className="text-success" />
                </div>
                <h3 className="fw-bold mb-2">Account Created Successfully! 🎉</h3>
                <p className="text-muted mb-3">
                  Your account has been created. You will be redirected to the login page...
                </p>
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
                <div className="mt-3">
                  <Link to="/login" className="btn btn-primary">
                    Go to Login Now
                  </Link>
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-vh-100 d-flex align-items-center bg-light">
      <div className="container py-4">
        <div className="row g-0 shadow-lg rounded-4 overflow-hidden bg-white">
          {/* Left Section - Branding */}
          <motion.div 
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="col-lg-6 d-none d-lg-flex flex-column justify-content-center p-5 bg-primary bg-gradient text-white"
            style={{ minHeight: '650px' }}
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

          {/* Right Section - Registration Form */}
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

              <h2 className="fw-bold mb-1">Create Account</h2>
              <p className="text-muted mb-4">Join ServiceDesk and start managing your requests</p>

              {submitError && (
                <div className="alert alert-danger d-flex align-items-center gap-2">
                  <AlertCircle size={18} />
                  {submitError}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                {/* Full Name */}
                <div className="mb-3">
                  <label htmlFor="fullName" className="form-label fw-semibold">
                    Full Name *
                  </label>
                  <div className="input-group">
                    <span className="input-group-text bg-light border-end-0">
                      <User size={18} className="text-muted" />
                    </span>
                    <input
                      type="text"
                      className={`form-control border-start-0 ps-0 ${errors.fullName ? 'is-invalid' : ''}`}
                      id="fullName"
                      name="fullName"
                      placeholder="John Doe"
                      value={formData.fullName}
                      onChange={handleChange}
                    />
                    {errors.fullName && (
                      <div className="invalid-feedback">{errors.fullName}</div>
                    )}
                  </div>
                </div>

                {/* Email */}
                <div className="mb-3">
                  <label htmlFor="email" className="form-label fw-semibold">
                    Email Address *
                  </label>
                  <div className="input-group">
                    <span className="input-group-text bg-light border-end-0">
                      <Mail size={18} className="text-muted" />
                    </span>
                    <input
                      type="email"
                      className={`form-control border-start-0 ps-0 ${errors.email ? 'is-invalid' : ''}`}
                      id="email"
                      name="email"
                      placeholder="you@example.com"
                      value={formData.email}
                      onChange={handleChange}
                    />
                    {errors.email && (
                      <div className="invalid-feedback">{errors.email}</div>
                    )}
                  </div>
                </div>

                {/* Phone */}
                <div className="mb-3">
                  <label htmlFor="phone" className="form-label fw-semibold">
                    Phone Number *
                  </label>
                  <div className="input-group">
                    <span className="input-group-text bg-light border-end-0">
                      <Phone size={18} className="text-muted" />
                    </span>
                    <input
                      type="tel"
                      className={`form-control border-start-0 ps-0 ${errors.phone ? 'is-invalid' : ''}`}
                      id="phone"
                      name="phone"
                      placeholder="+1 234 567 8900"
                      value={formData.phone}
                      onChange={handleChange}
                    />
                    {errors.phone && (
                      <div className="invalid-feedback">{errors.phone}</div>
                    )}
                  </div>
                </div>

                {/* Password */}
                <div className="mb-3">
                  <label htmlFor="password" className="form-label fw-semibold">
                    Password *
                  </label>
                  <div className="input-group">
                    <span className="input-group-text bg-light border-end-0">
                      <Lock size={18} className="text-muted" />
                    </span>
                    <input
                      type={showPassword ? 'text' : 'password'}
                      className={`form-control border-start-0 ps-0 ${errors.password ? 'is-invalid' : ''}`}
                      id="password"
                      name="password"
                      placeholder="Create a password"
                      value={formData.password}
                      onChange={handleChange}
                    />
                    <button
                      type="button"
                      className="btn btn-outline-secondary border-start-0"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                    {errors.password && (
                      <div className="invalid-feedback">{errors.password}</div>
                    )}
                  </div>
                  <small className="text-muted">Must be at least 8 characters</small>
                </div>

                {/* Confirm Password */}
                <div className="mb-3">
                  <label htmlFor="confirmPassword" className="form-label fw-semibold">
                    Confirm Password *
                  </label>
                  <div className="input-group">
                    <span className="input-group-text bg-light border-end-0">
                      <Lock size={18} className="text-muted" />
                    </span>
                    <input
                      type={showConfirmPassword ? 'text' : 'password'}
                      className={`form-control border-start-0 ps-0 ${errors.confirmPassword ? 'is-invalid' : ''}`}
                      id="confirmPassword"
                      name="confirmPassword"
                      placeholder="Confirm your password"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                    />
                    <button
                      type="button"
                      className="btn btn-outline-secondary border-start-0"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    >
                      {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                    {errors.confirmPassword && (
                      <div className="invalid-feedback">{errors.confirmPassword}</div>
                    )}
                  </div>
                </div>

                {/* Terms and Conditions */}
                <div className="mb-4">
                  <div className="form-check">
                    <input
                      type="checkbox"
                      className={`form-check-input ${errors.agreeTerms ? 'is-invalid' : ''}`}
                      id="agreeTerms"
                      name="agreeTerms"
                      checked={formData.agreeTerms}
                      onChange={handleChange}
                    />
                    <label className="form-check-label small" htmlFor="agreeTerms">
                      I agree to the{' '}
                      <Link to="/terms" className="text-decoration-none">
                        Terms and Conditions
                      </Link>
                      {' '}and{' '}
                      <Link to="/privacy" className="text-decoration-none">
                        Privacy Policy
                      </Link>
                    </label>
                    {errors.agreeTerms && (
                      <div className="invalid-feedback">{errors.agreeTerms}</div>
                    )}
                  </div>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary w-100 py-2 fw-semibold"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" />
                      Creating Account...
                    </>
                  ) : (
                    'Create Account'
                  )}
                </button>
              </form>

              <div className="text-center mt-4">
                <p className="small text-muted mb-0">
                  Already have an account?{' '}
                  <Link to="/login" className="text-decoration-none fw-semibold">
                    Sign in →
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

export default RegisterPage;