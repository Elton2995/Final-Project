import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  Star, 
  Send, 
  AlertCircle,
  CheckCircle,
  ArrowLeft,
  ThumbsUp,
  ThumbsDown,
  Smile,
  Frown,
  Meh
} from 'lucide-react';
import MainLayout from '../../layouts/MainLayout';

const GiveFeedback = () => {
  const navigate = useNavigate();
  const [rating, setRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [feedback, setFeedback] = useState({
    category: '',
    message: '',
    suggestion: '',
    wouldRecommend: null
  });
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errors, setErrors] = useState({});

  const categories = [
    'Overall Experience',
    'Service Quality',
    'Staff Professionalism',
    'Resolution Time',
    'Communication',
    'Website/App Usability'
  ];

  const ratingLabels = ['Terrible', 'Poor', 'Average', 'Good', 'Excellent'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFeedback(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    if (rating === 0) newErrors.rating = 'Please select a rating';
    if (!feedback.category) newErrors.category = 'Please select a category';
    if (!feedback.message.trim()) newErrors.message = 'Please share your feedback';
    if (feedback.message.length < 20) newErrors.message = 'Feedback must be at least 20 characters';
    if (feedback.wouldRecommend === null) newErrors.wouldRecommend = 'Please let us know if you would recommend us';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      setSubmitting(true);
      // API call would go here
      await new Promise(resolve => setTimeout(resolve, 1500));
      setSuccess(true);
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const getRatingEmoji = (rating) => {
    if (rating >= 4) return <Smile size={24} className="text-success" />;
    if (rating >= 3) return <Meh size={24} className="text-warning" />;
    return <Frown size={24} className="text-danger" />;
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
            <h3 className="fw-bold mb-2">Thank You for Your Feedback!</h3>
            <p className="text-muted">Your feedback helps us improve our service. We appreciate your time!</p>
            <div className="d-flex gap-3 justify-content-center mt-4">
              <button onClick={() => navigate('/dashboard')} className="btn btn-primary">
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
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft size={20} />
          </button>
          <div>
            <h2 className="fw-bold mb-0">Give Feedback</h2>
            <p className="text-muted">Share your experience with us</p>
          </div>
        </motion.div>

        {/* Feedback Form */}
        <motion.div variants={itemVariants}>
          <div className="card card-custom p-4">
            <form onSubmit={handleSubmit}>
              <div className="row g-4">
                {/* Rating */}
                <div className="col-12">
                  <label className="form-label fw-semibold">How would you rate your experience? *</label>
                  <div className="d-flex flex-wrap gap-2">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        className="btn p-0 border-0"
                        onMouseEnter={() => setHoveredRating(star)}
                        onMouseLeave={() => setHoveredRating(0)}
                        onClick={() => setRating(star)}
                      >
                        <Star
                          size={40}
                          className={`transition-all ${
                            star <= (hoveredRating || rating)
                              ? 'text-warning fill-warning'
                              : 'text-secondary'
                          }`}
                        />
                      </button>
                    ))}
                  </div>
                  <div className="mt-2 d-flex align-items-center gap-3">
                    {rating > 0 && (
                      <>
                        <span className="fw-semibold">{ratingLabels[rating - 1]}</span>
                        {getRatingEmoji(rating)}
                      </>
                    )}
                  </div>
                  {errors.rating && <div className="text-danger small mt-1">{errors.rating}</div>}
                </div>

                {/* Category */}
                <div className="col-12">
                  <label className="form-label fw-semibold">Category *</label>
                  <select
                    className={`form-select ${errors.category ? 'is-invalid' : ''}`}
                    name="category"
                    value={feedback.category}
                    onChange={handleChange}
                  >
                    <option value="">Select a category</option>
                    {categories.map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                  {errors.category && <div className="invalid-feedback">{errors.category}</div>}
                </div>

                {/* Feedback Message */}
                <div className="col-12">
                  <label className="form-label fw-semibold">Your Feedback *</label>
                  <textarea
                    className={`form-control ${errors.message ? 'is-invalid' : ''}`}
                    name="message"
                    value={feedback.message}
                    onChange={handleChange}
                    rows="5"
                    placeholder="Please share your detailed feedback about your experience..."
                  />
                  {errors.message && <div className="invalid-feedback">{errors.message}</div>}
                  <small className="text-muted">
                    Minimum 20 characters. Be specific about what you liked or what could be improved.
                  </small>
                </div>

                {/* Suggestions */}
                <div className="col-12">
                  <label className="form-label fw-semibold">Suggestions for Improvement</label>
                  <textarea
                    className="form-control"
                    name="suggestion"
                    value={feedback.suggestion}
                    onChange={handleChange}
                    rows="3"
                    placeholder="Do you have any suggestions on how we can improve?"
                  />
                </div>

                {/* Would Recommend */}
                <div className="col-12">
                  <label className="form-label fw-semibold">Would you recommend us to others? *</label>
                  <div className="d-flex gap-3">
                    <button
                      type="button"
                      className={`btn d-flex align-items-center gap-2 ${
                        feedback.wouldRecommend === true ? 'btn-success active' : 'btn-outline-secondary'
                      }`}
                      onClick={() => setFeedback(prev => ({ ...prev, wouldRecommend: true }))}
                    >
                      <ThumbsUp size={18} />
                      Yes
                    </button>
                    <button
                      type="button"
                      className={`btn d-flex align-items-center gap-2 ${
                        feedback.wouldRecommend === false ? 'btn-danger active' : 'btn-outline-secondary'
                      }`}
                      onClick={() => setFeedback(prev => ({ ...prev, wouldRecommend: false }))}
                    >
                      <ThumbsDown size={18} />
                      No
                    </button>
                  </div>
                  {errors.wouldRecommend && <div className="text-danger small mt-1">{errors.wouldRecommend}</div>}
                </div>

                {/* Submit Button */}
                <div className="col-12">
                  <div className="d-flex gap-3">
                    <button
                      type="submit"
                      className="btn btn-primary px-4 py-2 d-flex align-items-center gap-2"
                      disabled={submitting}
                    >
                      {submitting ? (
                        <>
                          <span className="spinner-border spinner-border-sm" role="status" />
                          Submitting...
                        </>
                      ) : (
                        <>
                          <Send size={18} />
                          Submit Feedback
                        </>
                      )}
                    </button>
                    <button
                      type="button"
                      className="btn btn-outline-secondary"
                      onClick={() => navigate('/dashboard')}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            </form>
          </div>

          {/* Info Alert */}
          <div className="mt-3">
            <div className="alert alert-info d-flex align-items-start gap-3">
              <AlertCircle size={20} className="flex-shrink-0 mt-1" />
              <div>
                <h6 className="fw-bold mb-1">Why your feedback matters</h6>
                <p className="small mb-0">
                  Your feedback helps us understand what we're doing well and where we can improve.
                  We take all feedback seriously and use it to enhance our service.
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
};

export default GiveFeedback;