import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  Plus, 
  Search, 
  Filter, 
  Eye, 
  Clock,
  CheckCircle,
  AlertCircle,
  Wrench,
  Calendar,
  User,
  ChevronDown,
  MessageSquare,
  Edit,
  Trash2
} from 'lucide-react';
import MainLayout from '../../layouts/MainLayout';

const ServiceRequests = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedRequest, setSelectedRequest] = useState(null);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      setLoading(true);
      // Mock data for service requests
      setRequests([
        {
          id: 'REQ-001',
          title: 'Technician visit for router setup',
          description: 'I need a technician to come and set up my new router. I have all the equipment ready.',
          category: 'Installation',
          status: 'inprogress',
          priority: 'medium',
          scheduledDate: '2025-06-10T09:00:00Z',
          createdDate: '2025-06-05T10:30:00Z',
          updatedDate: '2025-06-06T14:20:00Z',
          technician: 'John Smith',
          responses: [
            { id: 1, message: 'Your request has been received. We are scheduling a technician.', date: '2025-06-05T14:00:00Z', staff: 'Support Team' },
            { id: 2, message: 'Technician John Smith has been assigned. He will visit on June 10th at 9:00 AM.', date: '2025-06-06T14:20:00Z', staff: 'Support Team' }
          ]
        },
        {
          id: 'REQ-002',
          title: 'Additional phone line installation',
          description: 'I would like to request an additional phone line for my home office.',
          category: 'New Service',
          status: 'open',
          priority: 'low',
          scheduledDate: null,
          createdDate: '2025-06-07T09:15:00Z',
          updatedDate: '2025-06-07T09:15:00Z',
          technician: null,
          responses: []
        },
        {
          id: 'REQ-003',
          title: 'Speed upgrade request',
          description: 'I would like to upgrade my internet speed from 100Mbps to 500Mbps.',
          category: 'Upgrade',
          status: 'resolved',
          priority: 'medium',
          scheduledDate: '2025-06-08T13:00:00Z',
          createdDate: '2025-06-01T11:00:00Z',
          updatedDate: '2025-06-08T15:00:00Z',
          technician: 'Sarah Johnson',
          responses: [
            { id: 1, message: 'Your speed upgrade request has been approved. The upgrade will be completed on June 8th.', date: '2025-06-03T10:00:00Z', staff: 'Support Team' },
            { id: 2, message: 'Your internet speed has been upgraded to 500Mbps. Please restart your modem.', date: '2025-06-08T15:00:00Z', staff: 'Support Team' }
          ]
        }
      ]);
    } catch (error) {
      console.error('Error fetching service requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      open: { class: 'badge-status-open', icon: <AlertCircle size={14} />, label: 'Pending' },
      inprogress: { class: 'badge-status-inprogress', icon: <Clock size={14} />, label: 'In Progress' },
      resolved: { class: 'badge-status-resolved', icon: <CheckCircle size={14} />, label: 'Completed' },
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
    if (!dateString) return 'Not scheduled';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatShortDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric'
    });
  };

  const filteredRequests = requests.filter(request => {
    const matchesSearch = request.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         request.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         request.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || request.status === filterStatus;
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
            <h2 className="fw-bold mb-1">Service Requests</h2>
            <p className="text-muted">Manage and track all your service requests</p>
          </div>
          <Link to="/customer/requests/new" className="btn btn-primary d-flex align-items-center gap-2">
            <Plus size={18} />
            <span>New Request</span>
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
                  placeholder="Search requests..."
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
                <option value="open">Pending</option>
                <option value="inprogress">In Progress</option>
                <option value="resolved">Completed</option>
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

        {/* Requests List */}
        <motion.div variants={itemVariants}>
          {loading ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
          ) : filteredRequests.length === 0 ? (
            <div className="card card-custom p-5 text-center">
              <Wrench size={48} className="text-muted mx-auto mb-3" />
              <h5 className="fw-bold">No service requests found</h5>
              <p className="text-muted">You haven't submitted any service requests yet.</p>
              <Link to="/customer/requests/new" className="btn btn-primary mt-3">
                Submit a Request
              </Link>
            </div>
          ) : (
            <div className="row g-3">
              {filteredRequests.map((request, index) => {
                const statusInfo = getStatusBadge(request.status);
                const hasResponses = request.responses && request.responses.length > 0;
                
                return (
                  <motion.div 
                    key={request.id} 
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
                            <h6 className="fw-bold mb-0">{request.title}</h6>
                            <span className={`badge-status ${statusInfo.class} d-flex align-items-center gap-1`}>
                              {statusInfo.icon}
                              {statusInfo.label}
                            </span>
                            <span className={`badge ${getPriorityBadge(request.priority)}`}>
                              {request.priority}
                            </span>
                          </div>
                          <p className="small text-muted mb-2">{request.description}</p>
                          <div className="d-flex flex-wrap gap-3 small">
                            <span className="text-muted">
                              <strong>Category:</strong> {request.category}
                            </span>
                            <span className="text-muted">
                              <strong>Created:</strong> {formatShortDate(request.createdDate)}
                            </span>
                            {request.technician && (
                              <span className="text-muted d-flex align-items-center gap-1">
                                <User size={14} />
                                <strong>Technician:</strong> {request.technician}
                              </span>
                            )}
                            {request.scheduledDate && (
                              <span className="text-muted d-flex align-items-center gap-1">
                                <Calendar size={14} />
                                <strong>Scheduled:</strong> {formatDate(request.scheduledDate)}
                              </span>
                            )}
                            {hasResponses && (
                              <span className="text-success d-flex align-items-center gap-1">
                                <MessageSquare size={14} />
                                {request.responses.length} response{request.responses.length > 1 ? 's' : ''}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="d-flex gap-2">
                          <button 
                            className="btn btn-sm btn-outline-primary d-flex align-items-center gap-1"
                            onClick={() => setSelectedRequest(selectedRequest === request.id ? null : request.id)}
                          >
                            <Eye size={16} />
                            <span>{selectedRequest === request.id ? 'Hide' : 'View'}</span>
                          </button>
                          {request.status === 'open' && (
                            <button className="btn btn-sm btn-outline-secondary">
                              <Edit size={16} />
                            </button>
                          )}
                        </div>
                      </div>

                      {/* Expanded Response Section */}
                      {selectedRequest === request.id && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                          className="mt-3 pt-3 border-top"
                        >
                          <h6 className="fw-bold mb-3">Request Details & Responses</h6>
                          
                          {/* Request Details */}
                          <div className="row g-3 mb-3">
                            <div className="col-12 col-md-6">
                              <div className="bg-light p-3 rounded-3">
                                <p className="small fw-semibold mb-1">Request ID</p>
                                <p className="small mb-0">{request.id}</p>
                              </div>
                            </div>
                            <div className="col-12 col-md-6">
                              <div className="bg-light p-3 rounded-3">
                                <p className="small fw-semibold mb-1">Status</p>
                                <p className="small mb-0">{statusInfo.label}</p>
                              </div>
                            </div>
                            {request.scheduledDate && (
                              <div className="col-12 col-md-6">
                                <div className="bg-light p-3 rounded-3">
                                  <p className="small fw-semibold mb-1">Scheduled Date</p>
                                  <p className="small mb-0">{formatDate(request.scheduledDate)}</p>
                                </div>
                              </div>
                            )}
                            {request.technician && (
                              <div className="col-12 col-md-6">
                                <div className="bg-light p-3 rounded-3">
                                  <p className="small fw-semibold mb-1">Assigned Technician</p>
                                  <p className="small mb-0">{request.technician}</p>
                                </div>
                              </div>
                            )}
                          </div>

                          {/* Responses */}
                          <h6 className="fw-bold mb-3">Responses</h6>
                          {hasResponses ? (
                            <div className="d-flex flex-column gap-3">
                              {request.responses.map((response) => (
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
                              placeholder="Add a message..."
                              rows="2"
                            />
                            <button className="btn btn-sm btn-primary mt-2">Send Message</button>
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

export default ServiceRequests;