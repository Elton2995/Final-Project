import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Calendar,
  Save,
  Edit,
  Camera,
  Lock,
  Shield,
  AlertCircle,
  CheckCircle,
  ArrowLeft
} from 'lucide-react';
import MainLayout from '../../layouts/MainLayout';
import { useAuth } from '../../context/AuthContext';

const MyProfile = () => {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: '+1 234 567 8900',
    address: '123 Main Street, New York, NY 10001',
    bio: 'Customer at ServiceDesk. I appreciate quick and helpful support.'
  });

  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [passwordErrors, setPasswordErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      // API call to update profile
      await new Promise(resolve => setTimeout(resolve, 1000));
      updateUser({ name: formData.name, email: formData.email });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    const errors = {};
    if (passwordData.newPassword.length < 8) {
      errors.newPassword = 'Password must be at least 8 characters';
    }
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }
    if (Object.keys(errors).length > 0) {
      setPasswordErrors(errors);
      return;
    }

    // Handle password change
    alert('Password updated successfully!');
    setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
    setShowPasswordForm(false);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1
    }
  };

  return (
    <MainLayout>
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="p-4 p-md-5"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="d-flex align-items-center gap-3 mb-4">
          <button 
            className="btn btn-outline-secondary p-2" 
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft size={20} />
          </button>
          <div>
            <h2 className="fw-bold mb-0">My Profile</h2>
            <p className="text-muted">Manage your personal information</p>
          </div>
        </motion.div>

        <div className="row g-4">
          {/* Profile Card */}
          <motion.div variants={itemVariants} className="col-12 col-lg-4">
            <div className="card card-custom p-4 text-center">
              <div className="position-relative d-inline-block mx-auto">
                <img
                  src={user?.avatar || `https://ui-avatars.com/api/?name=${formData.name}`}
                  alt="Profile"
                  className="rounded-circle border border-3 border-primary"
                  width={120}
                  height={120}
                />
                <button className="btn btn-primary btn-sm rounded-circle position-absolute bottom-0 end-0 p-2">
                  <Camera size={16} />
                </button>
              </div>
              <h5 className="fw-bold mt-3">{formData.name}</h5>
              <p className="text-muted small">{formData.email}</p>
              <div className="d-flex justify-content-center gap-3 mt-2">
                <span className="badge bg-success">Active</span>
                <span className="badge bg-info">Customer</span>
              </div>
              <hr />
              <div className="text-start small">
                <p className="d-flex gap-2 mb-2">
                  <Mail size={16} className="text-muted flex-shrink-0" />
                  <span>{formData.email}</span>
                </p>
                <p className="d-flex gap-2 mb-2">
                  <Phone size={16} className="text-muted flex-shrink-0" />
                  <span>{formData.phone}</span>
                </p>
                <p className="d-flex gap-2 mb-2">
                  <MapPin size={16} className="text-muted flex-shrink-0" />
                  <span>{formData.address}</span>
                </p>
                <p className="d-flex gap-2 mb-0">
                  <Calendar size={16} className="text-muted flex-shrink-0" />
                  <span>Joined June 2025</span>
                </p>
              </div>
            </div>
          </motion.div>

          {/* Edit Form */}
          <motion.div variants={itemVariants} className="col-12 col-lg-8">
            <div className="card card-custom p-4">
              <div className="d-flex justify-content-between align-items-center mb-4">
                <h6 className="fw-bold mb-0">Personal Information</h6>
                {!isEditing && (
                  <button
                    className="btn btn-outline-primary btn-sm d-flex align-items-center gap-1"
                    onClick={() => setIsEditing(true)}
                  >
                    <Edit size={16} />
                    Edit Profile
                  </button>
                )}
              </div>

              {success && (
                <div className="alert alert-success d-flex align-items-center gap-2">
                  <CheckCircle size={18} />
                  Profile updated successfully!
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="row g-3">
                  <div className="col-12 col-md-6">
                    <label className="form-label fw-semibold">Full Name</label>
                    <input
                      type="text"
                      className="form-control"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      disabled={!isEditing}
                    />
                  </div>
                  <div className="col-12 col-md-6">
                    <label className="form-label fw-semibold">Email Address</label>
                    <input
                      type="email"
                      className="form-control"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      disabled={!isEditing}
                    />
                  </div>
                  <div className="col-12 col-md-6">
                    <label className="form-label fw-semibold">Phone Number</label>
                    <input
                      type="tel"
                      className="form-control"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      disabled={!isEditing}
                    />
                  </div>
                  <div className="col-12 col-md-6">
                    <label className="form-label fw-semibold">Address</label>
                    <input
                      type="text"
                      className="form-control"
                      name="address"
                      value={formData.address}
                      onChange={handleChange}
                      disabled={!isEditing}
                    />
                  </div>
                  <div className="col-12">
                    <label className="form-label fw-semibold">Bio</label>
                    <textarea
                      className="form-control"
                      name="bio"
                      value={formData.bio}
                      onChange={handleChange}
                      rows="2"
                      disabled={!isEditing}
                    />
                  </div>
                  {isEditing && (
                    <div className="col-12">
                      <div className="d-flex gap-2">
                        <button type="submit" className="btn btn-primary" disabled={saving}>
                          {saving ? (
                            <>
                              <span className="spinner-border spinner-border-sm me-2" role="status" />
                              Saving...
                            </>
                          ) : (
                            <Save size={16} className="me-1" />
                          )}
                          Save Changes
                        </button>
                        <button
                          type="button"
                          className="btn btn-outline-secondary"
                          onClick={() => setIsEditing(false)}
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </form>

              {/* Password Section */}
              <hr className="my-4" />
              <div>
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h6 className="fw-bold mb-0 d-flex align-items-center gap-2">
                    <Lock size={18} />
                    Security
                  </h6>
                  <button
                    className="btn btn-outline-primary btn-sm"
                    onClick={() => setShowPasswordForm(!showPasswordForm)}
                  >
                    {showPasswordForm ? 'Cancel' : 'Change Password'}
                  </button>
                </div>

                {showPasswordForm && (
                  <form onSubmit={handlePasswordSubmit}>
                    <div className="row g-3">
                      <div className="col-12">
                        <label className="form-label fw-semibold">Current Password</label>
                        <input
                          type="password"
                          className="form-control"
                          name="currentPassword"
                          value={passwordData.currentPassword}
                          onChange={handlePasswordChange}
                          required
                        />
                      </div>
                      <div className="col-12 col-md-6">
                        <label className="form-label fw-semibold">New Password</label>
                        <input
                          type="password"
                          className={`form-control ${passwordErrors.newPassword ? 'is-invalid' : ''}`}
                          name="newPassword"
                          value={passwordData.newPassword}
                          onChange={handlePasswordChange}
                          required
                        />
                        {passwordErrors.newPassword && (
                          <div className="invalid-feedback">{passwordErrors.newPassword}</div>
                        )}
                      </div>
                      <div className="col-12 col-md-6">
                        <label className="form-label fw-semibold">Confirm Password</label>
                        <input
                          type="password"
                          className={`form-control ${passwordErrors.confirmPassword ? 'is-invalid' : ''}`}
                          name="confirmPassword"
                          value={passwordData.confirmPassword}
                          onChange={handlePasswordChange}
                          required
                        />
                        {passwordErrors.confirmPassword && (
                          <div className="invalid-feedback">{passwordErrors.confirmPassword}</div>
                        )}
                      </div>
                      <div className="col-12">
                        <button type="submit" className="btn btn-primary">
                          <Lock size={16} className="me-1" />
                          Update Password
                        </button>
                      </div>
                    </div>
                  </form>
                )}
              </div>

              {/* Security Tips */}
              <div className="mt-3">
                <div className="alert alert-warning d-flex align-items-start gap-3">
                  <Shield size={20} className="flex-shrink-0 mt-1" />
                  <div>
                    <h6 className="fw-bold mb-1">Security Tips</h6>
                    <ul className="small mb-0 ps-3">
                      <li>Use a strong password with at least 8 characters</li>
                      <li>Include numbers, symbols, and both uppercase and lowercase letters</li>
                      <li>Never share your password with anyone</li>
                      <li>Enable two-factor authentication for extra security</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </MainLayout>
  );
};

export default MyProfile;