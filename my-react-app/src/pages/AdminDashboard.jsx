import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Users, 
  Ticket, 
  UserCheck, 
  CheckCircle, 
  TrendingUp, 
  Clock,
  BarChart3,
  PieChart,
  Download,
  Filter,
  Search,
  MoreVertical,
  ArrowUp,
  ArrowDown
} from 'lucide-react';
import AdminLayout from '../layouts/AdminLayout';

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalUsers: 13,
    usersGrowth: 2,
    activeCases: 12,
    highPriority: 5,
    staffOnline: 3,
    totalStaff: 4,
    resolvedToday: 18,
    resolvedGrowth: 4
  });

  const [casesData, setCasesData] = useState({
    new: 8,
    inProgress: 12,
    resolved: 38,
    closed: 11
  });

  const [chartData, setChartData] = useState({
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    new: [12, 19, 15, 8],
    resolved: [8, 14, 22, 18]
  });

  const [recentActivities, setRecentActivities] = useState([
    { id: 1, user: 'John Doe', action: 'Submitted a complaint', time: '2 min ago', type: 'complaint' },
    { id: 2, user: 'Sarah Smith', action: 'Resolved ticket #1234', time: '15 min ago', type: 'resolution' },
    { id: 3, user: 'Mike Johnson', action: 'Created new user account', time: '1 hour ago', type: 'user' },
    { id: 4, user: 'Emily Davis', action: 'Updated complaint status', time: '2 hours ago', type: 'update' }
  ]);

  // Animation variants
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
    <AdminLayout>
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="p-4 p-md-5"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="d-flex flex-wrap justify-content-between align-items-center mb-4">
          <div>
            <h2 className="fw-bold mb-1">Dashboard</h2>
            <p className="text-muted">Real-time snapshot across all users, staff, and cases.</p>
          </div>
          <div className="d-flex gap-2">
            <button className="btn btn-outline-secondary d-flex align-items-center gap-2">
              <Filter size={18} />
              <span>Filter</span>
            </button>
            <button className="btn btn-primary d-flex align-items-center gap-2">
              <Download size={18} />
              <span>Export</span>
            </button>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <motion.div variants={itemVariants} className="row g-3 mb-4">
          <div className="col-12 col-sm-6 col-xl-3">
            <div className="card card-custom p-3">
              <div className="d-flex align-items-center justify-content-between">
                <div>
                  <p className="text-muted small mb-1">Total Users</p>
                  <h3 className="fw-bold mb-0">{stats.totalUsers}</h3>
                  <span className="text-success small d-flex align-items-center gap-1">
                    <ArrowUp size={14} />
                    ↑ {stats.usersGrowth} this week
                  </span>
                </div>
                <div className="bg-primary bg-opacity-10 p-3 rounded-circle">
                  <Users className="text-primary" size={28} />
                </div>
              </div>
            </div>
          </div>

          <div className="col-12 col-sm-6 col-xl-3">
            <div className="card card-custom p-3">
              <div className="d-flex align-items-center justify-content-between">
                <div>
                  <p className="text-muted small mb-1">Active Cases</p>
                  <h3 className="fw-bold mb-0">{stats.activeCases}</h3>
                  <span className="text-danger small d-flex align-items-center gap-1">
                    <ArrowUp size={14} />
                    ↑ {stats.highPriority} high priority
                  </span>
                </div>
                <div className="bg-danger bg-opacity-10 p-3 rounded-circle">
                  <Ticket className="text-danger" size={28} />
                </div>
              </div>
            </div>
          </div>

          <div className="col-12 col-sm-6 col-xl-3">
            <div className="card card-custom p-3">
              <div className="d-flex align-items-center justify-content-between">
                <div>
                  <p className="text-muted small mb-1">Staff Online</p>
                  <h3 className="fw-bold mb-0">{stats.staffOnline} / {stats.totalStaff}</h3>
                  <span className="text-success small">
                    {Math.round((stats.staffOnline / stats.totalStaff) * 100)}% available
                  </span>
                </div>
                <div className="bg-success bg-opacity-10 p-3 rounded-circle">
                  <UserCheck className="text-success" size={28} />
                </div>
              </div>
            </div>
          </div>

          <div className="col-12 col-sm-6 col-xl-3">
            <div className="card card-custom p-3">
              <div className="d-flex align-items-center justify-content-between">
                <div>
                  <p className="text-muted small mb-1">Resolved Today</p>
                  <h3 className="fw-bold mb-0">{stats.resolvedToday}</h3>
                  <span className="text-success small d-flex align-items-center gap-1">
                    <ArrowUp size={14} />
                    ↑ +{stats.resolvedGrowth} vs yesterday
                  </span>
                </div>
                <div className="bg-info bg-opacity-10 p-3 rounded-circle">
                  <CheckCircle className="text-info" size={28} />
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Charts Row */}
        <motion.div variants={itemVariants} className="row g-3 mb-4">
          {/* Cases Chart */}
          <div className="col-12 col-lg-7">
            <div className="card card-custom p-3">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h6 className="fw-bold mb-0">Cases — Last 30 Days</h6>
                <div className="d-flex gap-3">
                  <span className="d-flex align-items-center gap-1">
                    <span className="badge bg-primary rounded-circle p-2" />
                    <small>New Cases</small>
                  </span>
                  <span className="d-flex align-items-center gap-1">
                    <span className="badge bg-success rounded-circle p-2" />
                    <small>Resolved</small>
                  </span>
                </div>
              </div>
              {/* Simple bar chart representation */}
              <div className="d-flex align-items-end gap-2" style={{ height: '200px' }}>
                {chartData.labels.map((label, index) => (
                  <div key={index} className="flex-grow-1 d-flex flex-column align-items-center">
                    <div className="w-100 d-flex flex-column align-items-center gap-1">
                      <div 
                        className="bg-primary rounded-top" 
                        style={{ 
                          height: `${(chartData.new[index] / 25) * 150}px`,
                          width: '60%',
                          minHeight: '5px'
                        }}
                      />
                      <div 
                        className="bg-success rounded-top" 
                        style={{ 
                          height: `${(chartData.resolved[index] / 25) * 150}px`,
                          width: '60%',
                          minHeight: '5px'
                        }}
                      />
                    </div>
                    <span className="small text-muted mt-2">{label}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Cases by Status */}
          <div className="col-12 col-lg-5">
            <div className="card card-custom p-3">
              <h6 className="fw-bold mb-3">Cases by Status</h6>
              <div className="d-flex flex-column gap-3">
                <div>
                  <div className="d-flex justify-content-between mb-1">
                    <span>Open</span>
                    <span className="fw-bold">{casesData.new}</span>
                  </div>
                  <div className="progress" style={{ height: '8px' }}>
                    <div 
                      className="progress-bar bg-warning" 
                      style={{ width: `${(casesData.new / 69) * 100}%` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="d-flex justify-content-between mb-1">
                    <span>In Progress</span>
                    <span className="fw-bold">{casesData.inProgress}</span>
                  </div>
                  <div className="progress" style={{ height: '8px' }}>
                    <div 
                      className="progress-bar bg-primary" 
                      style={{ width: `${(casesData.inProgress / 69) * 100}%` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="d-flex justify-content-between mb-1">
                    <span>Resolved</span>
                    <span className="fw-bold">{casesData.resolved}</span>
                  </div>
                  <div className="progress" style={{ height: '8px' }}>
                    <div 
                      className="progress-bar bg-success" 
                      style={{ width: `${(casesData.resolved / 69) * 100}%` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="d-flex justify-content-between mb-1">
                    <span>Closed</span>
                    <span className="fw-bold">{casesData.closed}</span>
                  </div>
                  <div className="progress" style={{ height: '8px' }}>
                    <div 
                      className="progress-bar bg-secondary" 
                      style={{ width: `${(casesData.closed / 69) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Recent Activity */}
        <motion.div variants={itemVariants}>
          <div className="card card-custom p-3">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h6 className="fw-bold mb-0">Recent Activity</h6>
              <button className="btn btn-link text-decoration-none p-0">View All</button>
            </div>
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>User</th>
                    <th>Activity</th>
                    <th>Time</th>
                    <th>Type</th>
                  </tr>
                </thead>
                <tbody>
                  {recentActivities.map((activity) => (
                    <tr key={activity.id}>
                      <td className="fw-semibold">{activity.user}</td>
                      <td>{activity.action}</td>
                      <td className="text-muted">{activity.time}</td>
                      <td>
                        <span className={`badge bg-${activity.type === 'complaint' ? 'warning' : activity.type === 'resolution' ? 'success' : 'info'}`}>
                          {activity.type}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AdminLayout>
  );
};

export default AdminDashboard;