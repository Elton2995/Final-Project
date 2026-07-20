import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  Send, 
  MessageSquare, 
  Star, 
  User,
  Plus,
  ChevronRight,
  Clock,
  CheckCircle,
  AlertCircle,
  TrendingUp
} from 'lucide-react';
import MainLayout from '../layouts/MainLayout';

const CustomerDashboard = () => {
  const location = useLocation();
  const [accessDenied, setAccessDenied] = useState(false);
  const [stats, setStats] = useState({
    totalCases: 7,
    open: 2,
    inProgress: 3,
    resolved: 2
  });

  const [recentCases, setRecentCases] = useState([
    {
      id: 'CMP-001',
      title: 'Internet connection keeps dropping',
      type: 'Complaint',
      status: 'open',
      date: 'Jun 8, 2025'
    },
    {
      id: 'REQ-001',
      title: 'Technician visit for router setup',
      type: 'Request',
      status: 'inprogress',
      date: 'Jun 5, 2025'
    }
  ]);

  // Check for access denied message
  useEffect(() => {
    if (location.state?.accessDenied) {
      setAccessDenied(true);
      // Clear the state so message doesn't show again on refresh
      window.history.replaceState({}, document.title);
    }
  }, [location]);

  const quickActions = [
    { icon: <Plus size={20} />, label: 'Submit Complaint', path: '/customer/complaints/new', color: 'primary' },
    { icon: <Send size={20} />, label: 'New Request', path: '/customer/requests/new', color: 'success' },
    { icon: <MessageSquare size={20} />, label: 'View Messages', path: '/customer/messages', color: 'info' },
    { icon: <Star size={20} />, label: 'Leave Feedback', path: '/customer/feedback', color: 'warning' }
  ];

  const getStatusBadge = (status) => {
    const statusMap = {
      open: { class: 'badge-status-open', label: 'Open' },
      inprogress: { class: 'badge-status-inprogress', label: 'In Progress' },
      resolved: { class: 'badge-status-resolved', label: 'Resolved' },
      closed: { class: 'badge-status-closed', label: 'Closed' }
    };
    return statusMap[status] || statusMap.open;
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
        {/* Access Denied Alert */}
        {accessDenied && (
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="alert alert-danger d-flex align-items-center gap-2 mb-4"
            role="alert"
          >
            <AlertCircle size={20} />
            <div>
              <strong>Access Denied!</strong> You don't have permission to view that page.
            </div>
          </motion.div>
        )}

        {/* Welcome Section */}
        <motion.div variants={itemVariants} className="mb-4">
          <h2 className="fw-bold mb-1">
            Good morning, Elton 🎉
          </h2>
          <p className="text-muted">Here's a snapshot of your cases and recent activity.</p>
        </motion.div>

        {/* Stats Cards */}
        <motion.div variants={itemVariants} className="row g-3 mb-4">
          <div className="col-6 col-md-3">
            <div className="card card-custom p-3 text-center">
              <h3 className="fw-bold text-primary mb-0">{stats.totalCases}</h3>
              <p className="small text-muted mb-0">Total Cases</p>
            </div>
          </div>
          <div className="col-6 col-md-3">
            <div className="card card-custom p-3 text-center">
              <h3 className="fw-bold text-warning mb-0">{stats.open}</h3>
              <p className="small text-muted mb-0">Open</p>
            </div>
          </div>
          <div className="col-6 col-md-3">
            <div className="card card-custom p-3 text-center">
              <h3 className="fw-bold text-info mb-0">{stats.inProgress}</h3>
              <p className="small text-muted mb-0">In Progress</p>
            </div>
          </div>
          <div className="col-6 col-md-3">
            <div className="card card-custom p-3 text-center">
              <h3 className="fw-bold text-success mb-0">{stats.resolved}</h3>
              <p className="small text-muted mb-0">Resolved</p>
            </div>
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div variants={itemVariants} className="mb-4">
          <h6 className="fw-bold mb-3">Quick Actions</h6>
          <div className="row g-2">
            {quickActions.map((action, index) => (
              <div key={index} className="col-6 col-md-3">
                <Link to={action.path} className="text-decoration-none">
                  <div className="card card-custom p-3 text-center hover-lift cursor-pointer">
                    <div className={`bg-${action.color} bg-opacity-10 p-2 rounded-circle d-inline-block mx-auto mb-2`}>
                      <span className={`text-${action.color}`}>{action.icon}</span>
                    </div>
                    <p className="small fw-semibold mb-0">{action.label}</p>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Recent Activity Table */}
        <motion.div variants={itemVariants}>
          <div className="card card-custom p-3">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h6 className="fw-bold mb-0">Recent Activity</h6>
              <Link to="/customer/complaints" className="text-decoration-none small">
                View All <ChevronRight size={16} />
              </Link>
            </div>
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {recentCases.map((caseItem) => {
                    const statusInfo = getStatusBadge(caseItem.status);
                    return (
                      <tr key={caseItem.id}>
                        <td className="fw-semibold">{caseItem.id}</td>
                        <td>{caseItem.title}</td>
                        <td>
                          <span className={`badge bg-${caseItem.type === 'Complaint' ? 'warning' : 'info'}`}>
                            {caseItem.type}
                          </span>
                        </td>
                        <td>
                          <span className={`badge-status ${statusInfo.class}`}>
                            {statusInfo.label}
                          </span>
                        </td>
                        <td className="text-muted small">{caseItem.date}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>

        {/* Rating Section */}
        <motion.div variants={itemVariants} className="mt-3">
          <div className="card card-custom p-3 bg-primary bg-opacity-10">
            <div className="d-flex align-items-center justify-content-between flex-wrap gap-2">
              <div>
                <h6 className="fw-bold mb-0">Rate your experience</h6>
                <p className="small text-muted mb-0">Your feedback helps us improve</p>
              </div>
              <Link to="/customer/feedback" className="btn btn-primary">
                <Star size={18} className="me-1" />
                Leave Feedback
              </Link>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
};

export default CustomerDashboard;