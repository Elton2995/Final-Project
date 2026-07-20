import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Users, 
  Ticket, 
  CheckCircle, 
  Clock,
  MessageSquare,
  TrendingUp,
  Filter,
  Search,
  MoreVertical
} from 'lucide-react';
import StaffLayout from '../layouts/StaffLayout';

const StaffDashboard = () => {
  const [stats, setStats] = useState({
    assignedCases: 15,
    pending: 5,
    inProgress: 7,
    resolved: 3,
    customerSatisfaction: 92
  });

  const [assignedCases, setAssignedCases] = useState([
    { id: 'CMP-001', customer: 'John Doe', issue: 'Internet connection dropping', priority: 'high', status: 'open', date: '2025-06-08' },
    { id: 'CMP-002', customer: 'Sarah Smith', issue: 'Billing error on invoice', priority: 'medium', status: 'inprogress', date: '2025-06-07' },
    { id: 'REQ-001', customer: 'Mike Johnson', issue: 'Router setup assistance', priority: 'low', status: 'inprogress', date: '2025-06-05' },
    { id: 'CMP-003', customer: 'Emily Davis', issue: 'Service outage in area', priority: 'high', status: 'resolved', date: '2025-06-04' }
  ]);

  const getPriorityBadge = (priority) => {
    const map = {
      high: 'bg-danger',
      medium: 'bg-warning',
      low: 'bg-info'
    };
    return map[priority] || 'bg-secondary';
  };

  const getStatusBadge = (status) => {
    const map = {
      open: 'badge-status-open',
      inprogress: 'badge-status-inprogress',
      resolved: 'badge-status-resolved',
      closed: 'badge-status-closed'
    };
    return map[status] || 'badge-status-open';
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
    <StaffLayout>
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="p-4 p-md-5"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="d-flex flex-wrap justify-content-between align-items-center mb-4">
          <div>
            <h2 className="fw-bold mb-1">Staff Dashboard</h2>
            <p className="text-muted">Manage and respond to customer complaints and requests.</p>
          </div>
          <div className="d-flex gap-2">
            <button className="btn btn-outline-secondary d-flex align-items-center gap-2">
              <Filter size={18} />
              <span>Filter</span>
            </button>
            <button className="btn btn-primary d-flex align-items-center gap-2">
              <MessageSquare size={18} />
              <span>Messages</span>
            </button>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <motion.div variants={itemVariants} className="row g-3 mb-4">
          <div className="col-6 col-md-3">
            <div className="card card-custom p-3">
              <div className="d-flex align-items-center justify-content-between">
                <div>
                  <p className="text-muted small mb-0">Assigned Cases</p>
                  <h3 className="fw-bold mb-0">{stats.assignedCases}</h3>
                </div>
                <div className="bg-primary bg-opacity-10 p-3 rounded-circle">
                  <Ticket className="text-primary" size={24} />
                </div>
              </div>
            </div>
          </div>

          <div className="col-6 col-md-3">
            <div className="card card-custom p-3">
              <div className="d-flex align-items-center justify-content-between">
                <div>
                  <p className="text-muted small mb-0">Pending</p>
                  <h3 className="fw-bold mb-0">{stats.pending}</h3>
                </div>
                <div className="bg-warning bg-opacity-10 p-3 rounded-circle">
                  <Clock className="text-warning" size={24} />
                </div>
              </div>
            </div>
          </div>

          <div className="col-6 col-md-3">
            <div className="card card-custom p-3">
              <div className="d-flex align-items-center justify-content-between">
                <div>
                  <p className="text-muted small mb-0">In Progress</p>
                  <h3 className="fw-bold mb-0">{stats.inProgress}</h3>
                </div>
                <div className="bg-info bg-opacity-10 p-3 rounded-circle">
                  <TrendingUp className="text-info" size={24} />
                </div>
              </div>
            </div>
          </div>

          <div className="col-6 col-md-3">
            <div className="card card-custom p-3">
              <div className="d-flex align-items-center justify-content-between">
                <div>
                  <p className="text-muted small mb-0">Satisfaction</p>
                  <h3 className="fw-bold mb-0">{stats.customerSatisfaction}%</h3>
                </div>
                <div className="bg-success bg-opacity-10 p-3 rounded-circle">
                  <CheckCircle className="text-success" size={24} />
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Assigned Cases Table */}
        <motion.div variants={itemVariants}>
          <div className="card card-custom p-3">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h6 className="fw-bold mb-0">Assigned Cases</h6>
              <div className="d-flex gap-2">
                <div className="position-relative">
                  <Search size={18} className="position-absolute text-muted" style={{ left: '10px', top: '50%', transform: 'translateY(-50%)' }} />
                  <input type="text" className="form-control form-control-sm ps-5" placeholder="Search cases..." style={{ width: '200px' }} />
                </div>
              </div>
            </div>
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Case ID</th>
                    <th>Customer</th>
                    <th>Issue</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {assignedCases.map((caseItem) => (
                    <tr key={caseItem.id}>
                      <td className="fw-semibold">{caseItem.id}</td>
                      <td>{caseItem.customer}</td>
                      <td>{caseItem.issue}</td>
                      <td>
                        <span className={`badge ${getPriorityBadge(caseItem.priority)}`}>
                          {caseItem.priority}
                        </span>
                      </td>
                      <td>
                        <span className={`badge-status ${getStatusBadge(caseItem.status)}`}>
                          {caseItem.status}
                        </span>
                      </td>
                      <td className="text-muted small">{caseItem.date}</td>
                      <td>
                        <button className="btn btn-sm btn-outline-primary">Respond</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </StaffLayout>
  );
};

export default StaffDashboard;