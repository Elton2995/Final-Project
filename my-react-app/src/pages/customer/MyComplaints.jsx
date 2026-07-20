import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  Plus, 
  Search, 
  Filter, 
  Eye, 
  Edit, 
  Trash2,
  ChevronDown,
  Clock,
  CheckCircle,
  AlertCircle,
  MessageSquare
} from 'lucide-react';
import MainLayout from '../../layouts/MainLayout';
import { complaintAPI } from '../../api/complaintAPI';

const MyComplaints = () => {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedComplaint, setSelectedComplaint] = useState(null);

  useEffect(() => {
    fetchComplaints();
  }, []);

  const fetchComplaints = async () => {
    try {
      setLoading(true);
      // const response = await complaintAPI.getMyComplaints();
      // setComplaints(response.data);
      
      // Mock data for now
      setComplaints([
        {
          id: 'CMP-001',
          title: 'Internet connection keeps dropping',
          description: 'My internet connection drops every 30 minutes. This has been happening for the past 3 days.',
          category: 'Technical Issue',
          status: 'open',
          priority: 'high',
          createdDate: '2025-06-08T10:30:00Z',
          updatedDate: '2025-06-08T14:20:00Z',
          responses: [
            { id: 1, message: 'We are looking into this issue. Our team will contact you shortly.', date: '2025-06-08T14:20:00Z', staff: 'Support Team' }
          ]
        },
        {
          id: 'CMP-002',
          title: 'Billing error on invoice #INV-2025-06',
          description: 'I was charged an incorrect amount on my latest invoice. The charge is $50 more than expected.',
          category: 'Billing',
          status: 'inprogress',
          priority: 'medium',
          createdDate: '2025-06-07T09:15:00Z',
          updatedDate: '2025-06-07T16:45:00Z',
          responses: [
            { id: 1, message: 'We have reviewed your invoice and found a discrepancy. Our billing team is working on a correction.', date: '2025-06-07T16:45:00Z', staff: 'Billing Team' }
          ]
        },
        {
          id: 'CMP-003',
          title: 'Service outage in my area',
          description: 'There is no internet service in my area since yesterday afternoon.',
          category: 'Outage',
          status: 'resolved',
          priority: 'high',
          createdDate: '2025-06-06T08:00:00Z',
          updatedDate: '2025-06-06T19:30:00Z',
          responses: [
            { id: 1, message: 'We are aware of the outage and working to restore service.', date: '2025-06-06T10:00:00Z', staff: 'Support Team' },
            { id: 2, message: 'Service has been restored. We apologize for the inconvenience.', date: '2025-06-06T19:30:00Z', staff: 'Support Team' }
          ]
        }
      ]);
    } catch (error) {
      console.error('Error fetching complaints:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      open: { class: 'badge-status-open', icon: <AlertCircle size={14} />, label: 'Open' },
      inprogress: { class: 'badge-status-inprogress', icon: <Clock size={14} />, label: 'In Progress' },
      resolved: { class: 'badge-status-resolved', icon: <CheckCircle size={14} />, label: 'Resolved' },
      closed: { class: 'badge-status-closed', icon: <CheckCircle size={14} />, label: 'Closed' }
    };
    return statusMap[status] || statusMap.open;
  };

  const getPriorityBadge = (priority) => {
    const priorityMap = {
      high: 'bg-danger',
      medium: 'bg-warning',
      low: 'bg-info'
    };
    return priorityMap[priority] || 'bg-secondary';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredComplaints = complaints.filter(complaint => {
    const matchesSearch = complaint.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         complaint.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || complaint.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

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
        <motion.div variants={itemVariants} className="d-flex flex-wrap justify-content-between align-items-center mb-4">
          <div>
            <h2 className="fw-bold mb-1">My Complaints</h2>
            <p className="text-muted">View and track all your complaints</p>
          </div>
          <Link to="/customer/complaints/new" className="btn btn-primary d-flex align-items-center gap-2">
            <Plus size={18} />
            <span>New Complaint</span>
          </Link>
        </motion.div>

        {/* Filters */}
        <motion.div variants={itemVariants} className="card card-custom p-3 mb-4">
          <div className="row g-3">
            <div className="col-12 col-md-6">
              <div className="position-relative">
                <Search size={18} className="position-absolute text-muted" style={{ left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
                <input
                  type="text"
                  className="form-control ps-5"
                  placeholder="Search complaints..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div className="col-12 col-md-3">
              <select 
                className="form-select"
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
              >
                <option value="all">All Status</option>
                <option value="open">Open</option>
                <option value="inprogress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>
            </div>
            <div className="col-12 col-md-3">
              <button className="btn btn-outline-secondary w-100 d-flex align-items-center justify-content-center gap-2">
                <Filter size={18} />
                <span>More Filters</span>
                <ChevronDown size={16} />
              </button>
            </div>
          </div>
        </motion.div>

        {/* Complaints List */}
        <motion.div variants={itemVariants}>
          {loading ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
          ) : filteredComplaints.length === 0 ? (
            <div className="card card-custom p-5 text-center">
              <AlertCircle size={48} className="text-muted mx-auto mb-3" />
              <h5 className="fw-bold">No complaints found</h5>
              <p className="text-muted">You haven't submitted any complaints yet.</p>
              <Link to="/customer/complaints/new" className="btn btn-primary mt-3">
                Submit a Complaint
              </Link>
            </div>
          ) : (
            <div className="row g-3">
              {filteredComplaints.map((complaint, index) => {
                const statusInfo = getStatusBadge(complaint.status);
                const hasResponses = complaint.responses && complaint.responses.length > 0;
                
                return (
                  <motion.div 
                    key={complaint.id} 
                    className="col-12"
                    variants={itemVariants}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                  >
                    <div className="card card-custom p-3 hover-lift">
                      <div className="d-flex flex-wrap justify-content-between align-items-start gap-2">
                        <div className="flex-grow-1">
                          <div className="d-flex flex-wrap align-items-center gap-2 mb-2">
                            <h6 className="fw-bold mb-0">{complaint.title}</h6>
                            <span className={`badge-status ${statusInfo.class} d-flex align-items-center gap-1`}>
                              {statusInfo.icon}
                              {statusInfo.label}
                            </span>
                            <span className={`badge ${getPriorityBadge(complaint.priority)}`}>
                              {complaint.priority}
                            </span>
                          </div>
                          <p className="small text-muted mb-2">{complaint.description}</p>
                          <div className="d-flex flex-wrap gap-3 small">
                            <span className="text-muted">
                              <strong>Category:</strong> {complaint.category}
                            </span>
                            <span className="text-muted">
                              <strong>Created:</strong> {formatDate(complaint.createdDate)}
                            </span>
                            {hasResponses && (
                              <span className="text-success d-flex align-items-center gap-1">
                                <MessageSquare size={14} />
                                {complaint.responses.length} response{complaint.responses.length > 1 ? 's' : ''}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="d-flex gap-2">
                          <button 
                            className="btn btn-sm btn-outline-primary d-flex align-items-center gap-1"
                            onClick={() => setSelectedComplaint(selectedComplaint === complaint.id ? null : complaint.id)}
                          >
                            <Eye size={16} />
                            <span>{selectedComplaint === complaint.id ? 'Hide' : 'View'}</span>
                          </button>
                          {complaint.status === 'open' && (
                            <Link to={`/customer/complaints/${complaint.id}/edit`} className="btn btn-sm btn-outline-secondary">
                              <Edit size={16} />
                            </Link>
                          )}
                        </div>
                      </div>

                      {/* Expanded Response Section */}
                      {selectedComplaint === complaint.id && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                          className="mt-3 pt-3 border-top"
                        >
                          <h6 className="fw-bold mb-3">Responses</h6>
                          {hasResponses ? (
                            <div className="d-flex flex-column gap-3">
                              {complaint.responses.map((response) => (
                                <div key={response.id} className="bg-light p-3 rounded-3">
                                  <div className="d-flex justify-content-between align-items-center mb-1">
                                    <span className="fw-semibold small">{response.staff}</span>
                                    <span className="text-muted small">{formatDate(response.date)}</span>
                                  </div>
                                  <p className="small mb-0">{response.message}</p>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <p className="text-muted small">No responses yet.</p>
                          )}
                          
                          <div className="mt-3">
                            <textarea 
                              className="form-control form-control-sm" 
                              placeholder="Add a response..."
                              rows="2"
                            />
                            <button className="btn btn-sm btn-primary mt-2">Send Response</button>
                          </div>
                        </motion.div>
                      )}
                    </div>
                  </motion.div>
                );
              })}
            </div>
          )}
        </motion.div>
      </motion.div>
    </MainLayout>
  );
};

export default MyComplaints;