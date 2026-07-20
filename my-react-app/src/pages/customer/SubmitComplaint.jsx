import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  AlertCircle, 
  Upload, 
  X,
  CheckCircle,
  ArrowLeft
} from 'lucide-react';
import MainLayout from '../../layouts/MainLayout';
import { complaintAPI } from '../../api/complaintAPI';

const SubmitComplaint = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    priority: 'medium',
    description: '',
    attachments: []
  });
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errors, setErrors] = useState({});

  const categories = [
    'Technical Issue',
    'Billing',
    'Service Outage',
    'Account Management',
    'Product Quality',
    'Customer Service',
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
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    const validFiles = files.filter(file => {
      const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
      return validTypes.includes(file.type) && file.size <= 5 * 1024 * 1024; // 5MB limit
    });

    if (validFiles.length !== files.length) {
      alert('Some files were not uploaded. Please ensure files are under 5MB and are images or PDFs.');
    }

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
      // const response = await complaintAPI.createComplaint(formData);
      // console.log('Complaint submitted:', response);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setSuccess(true);
      setTimeout(() => {
        navigate('/customer/complaints');
      }, 2000);
    } catch (error) {
      console.error('Error submitting complaint:', error);
      alert('Failed to submit complaint. Please try again.');
    } finally {
      setSubmitting(false);
    }
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
            <h3 className="fw-bold mb-2">Complaint Submitted!</h3>
            <p className="text-muted">Your complaint has been submitted successfully. You will receive updates via email.</p>
            <div className="d-flex gap-3 justify-content-center mt-4">
              <button onClick={() => navigate('/customer/complaints')} className="btn btn-primary">
                View My Complaints
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
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="p-4 p-md-5"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="d-flex align-items-center gap-3 mb-4">
          <button 
            className="btn btn-outline-secondary p-2" 
            onClick={() => navigate('/customer/complaints')}
          >
            <ArrowLeft size={20} />
          </button>
          <div>
            <h2 className="fw-bold mb-0">Submit Complaint</h2>
            <p className="text-muted">Describe your issue and we'll help you resolve it</p>
          </div>
        </motion.div>

        {/* Form */}
        <motion.div variants={itemVariants}>
          <div className="card card-custom p-4">
            <form onSubmit={handleSubmit}>
              <div className="row g-4">
                {/* Title */}
                <div className="col-12">
                  <label className="form-label fw-semibold">Complaint Title *</label>
                  <input
                    type="text"
                    className={`form-control ${errors.title ? 'is-invalid' : ''}`}
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    placeholder="Brief summary of your complaint"
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
                    rows="6"
                    placeholder="Please provide detailed information about your complaint..."
                  />
                  {errors.description && <div className="invalid-feedback">{errors.description}</div>}
                  <small className="text-muted">
                    Minimum 20 characters. Include relevant details like dates, error messages, etc.
                  </small>
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

                  {/* Attachment Previews */}
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
                        'Submit Complaint'
                      )}
                    </button>
                    <button
                      type="button"
                      className="btn btn-outline-secondary"
                      onClick={() => navigate('/customer/complaints')}
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
                  Our support team will review your complaint and respond within 24 hours.
                  You will receive notifications about updates to your complaint status.
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
};

export default SubmitComplaint;