import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  AlertCircle, 
  Upload, 
  X,
  CheckCircle,
  ArrowLeft,
  Calendar,
  Clock
} from 'lucide-react';
import MainLayout from '../../layouts/MainLayout';

const SubmitRequest = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    priority: 'medium',
    description: '',
    preferredDate: '',
    preferredTime: '',
    attachments: []
  });
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errors, setErrors] = useState({});

  const categories = [
    'Installation',
    'New Service',
    'Upgrade',
    'Repair',
    'Maintenance',
    'Other'
  ];

  const priorities = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    const validFiles = files.filter(file => {
      const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
      return validTypes.includes(file.type) && file.size <= 5 * 1024 * 1024;
    });

    setFormData(prev => ({
      ...prev,
      attachments: [...prev.attachments, ...validFiles]
    }));
  };

  const removeAttachment = (index) => {
    setFormData(prev => ({
      ...prev,
      attachments: prev.attachments.filter((_, i) => i !== index)
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.title.trim()) newErrors.title = 'Title is required';
    if (!formData.category) newErrors.category = 'Category is required';
    if (!formData.description.trim()) newErrors.description = 'Description is required';
    if (formData.description.length < 20) newErrors.description = 'Description must be at least 20 characters';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      setSubmitting(true);
      await new Promise(resolve => setTimeout(resolve, 1500));
      setSuccess(true);
      setTimeout(() => {
        navigate('/customer/requests');
      }, 2000);
    } catch (error) {
      console.error('Error submitting request:', error);
      alert('Failed to submit request. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (success) {
    return (
      <MainLayout>
        <div className="p-4 p-md-5 d-flex align-items-center justify-content-center" style={{ minHeight: '70vh' }}>
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="text-center"
          >
            <div className="bg-success bg-opacity-10 p-4 rounded-circle d-inline-block mb-4">
              <CheckCircle size={64} className="text-success" />
            </div>
            <h3 className="fw-bold mb-2">Request Submitted!</h3>
            <p className="text-muted">Your service request has been submitted successfully.</p>
            <div className="d-flex gap-3 justify-content-center mt-4">
              <button onClick={() => navigate('/customer/requests')} className="btn btn-primary">
                View My Requests
              </button>
              <button onClick={() => navigate('/dashboard')} className="btn btn-outline-secondary">
                Go to Dashboard
              </button>
            </div>
          </motion.div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="p-4 p-md-5"
      >
        {/* Header */}
        <div className="d-flex align-items-center gap-3 mb-4">
          <button 
            className="btn btn-outline-secondary p-2" 
            onClick={() => navigate('/customer/requests')}
          >
            <ArrowLeft size={20} />
          </button>
          <div>
            <h2 className="fw-bold mb-0">Submit Service Request</h2>
            <p className="text-muted">Request a new service or schedule a technician visit</p>
          </div>
        </div>

        {/* Form */}
        <div className="card card-custom p-4">
          <form onSubmit={handleSubmit}>
            <div className="row g-4">
              {/* Title */}
              <div className="col-12">
                <label className="form-label fw-semibold">Request Title *</label>
                <input
                  type="text"
                  className={`form-control ${errors.title ? 'is-invalid' : ''}`}
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="Brief summary of your request"
                />
                {errors.title && <div className="invalid-feedback">{errors.title}</div>}
              </div>

              {/* Category & Priority */}
              <div className="col-12 col-md-6">
                <label className="form-label fw-semibold">Category *</label>
                <select
                  className={`form-select ${errors.category ? 'is-invalid' : ''}`}
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                >
                  <option value="">Select a category</option>
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
                {errors.category && <div className="invalid-feedback">{errors.category}</div>}
              </div>

              <div className="col-12 col-md-6">
                <label className="form-label fw-semibold">Priority</label>
                <select
                  className="form-select"
                  name="priority"
                  value={formData.priority}
                  onChange={handleChange}
                >
                  {priorities.map(p => (
                    <option key={p.value} value={p.value}>{p.label}</option>
                  ))}
                </select>
              </div>

              {/* Description */}
              <div className="col-12">
                <label className="form-label fw-semibold">Description *</label>
                <textarea
                  className={`form-control ${errors.description ? 'is-invalid' : ''}`}
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows="5"
                  placeholder="Please provide detailed information about your request..."
                />
                {errors.description && <div className="invalid-feedback">{errors.description}</div>}
                <small className="text-muted">
                  Minimum 20 characters. Include relevant details, location, etc.
                </small>
              </div>

              {/* Preferred Date & Time */}
              <div className="col-12 col-md-6">
                <label className="form-label fw-semibold">Preferred Date</label>
                <div className="input-group">
                  <span className="input-group-text bg-light">
                    <Calendar size={18} />
                  </span>
                  <input
                    type="date"
                    className="form-control"
                    name="preferredDate"
                    value={formData.preferredDate}
                    onChange={handleChange}
                  />
                </div>
              </div>

              <div className="col-12 col-md-6">
                <label className="form-label fw-semibold">Preferred Time</label>
                <div className="input-group">
                  <span className="input-group-text bg-light">
                    <Clock size={18} />
                  </span>
                  <input
                    type="time"
                    className="form-control"
                    name="preferredTime"
                    value={formData.preferredTime}
                    onChange={handleChange}
                  />
                </div>
              </div>

              {/* Attachments */}
              <div className="col-12">
                <label className="form-label fw-semibold">Attachments</label>
                <div className="border-2 border-dashed rounded-3 p-4 text-center" style={{ borderColor: '#dee2e6' }}>
                  <input
                    type="file"
                    className="d-none"
                    id="file-upload"
                    multiple
                    accept=".jpg,.jpeg,.png,.gif,.pdf"
                    onChange={handleFileUpload}
                  />
                  <label htmlFor="file-upload" className="d-block cursor-pointer">
                    <Upload size={32} className="text-muted mx-auto d-block mb-2" />
                    <p className="mb-0">
                      <span className="text-primary fw-semibold">Click to upload</span> or drag and drop
                    </p>
                    <small className="text-muted">PNG, JPG, PDF (Max 5MB each)</small>
                  </label>
                </div>

                {formData.attachments.length > 0 && (
                  <div className="mt-3 d-flex flex-wrap gap-2">
                    {formData.attachments.map((file, index) => (
                      <div key={index} className="bg-light p-2 rounded-3 d-flex align-items-center gap-2">
                        <span className="small">{file.name}</span>
                        <span className="text-muted small">({(file.size / 1024).toFixed(0)} KB)</span>
                        <button
                          type="button"
                          className="btn btn-link p-0 text-danger"
                          onClick={() => removeAttachment(index)}
                        >
                          <X size={16} />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Submit Button */}
              <div className="col-12">
                <div className="d-flex gap-3">
                  <button
                    type="submit"
                    className="btn btn-primary px-4 py-2"
                    disabled={submitting}
                  >
                    {submitting ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" />
                        Submitting...
                      </>
                    ) : (
                      'Submit Request'
                    )}
                  </button>
                  <button
                    type="button"
                    className="btn btn-outline-secondary"
                    onClick={() => navigate('/customer/requests')}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>

        {/* Help Text */}
        <div className="mt-3">
          <div className="alert alert-info d-flex align-items-start gap-3">
            <AlertCircle size={20} className="flex-shrink-0 mt-1" />
            <div>
              <h6 className="fw-bold mb-1">What happens next?</h6>
              <p className="small mb-0">
                Our team will review your request and get back to you within 24 hours.
                You will receive notifications about updates to your request status.
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </MainLayout>
  );
};

export default SubmitRequest;