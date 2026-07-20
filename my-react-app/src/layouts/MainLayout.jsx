import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  Send, 
  MessageSquare, 
  Star, 
  User,
  Menu,
  X,
  Bell,
  ChevronDown,
  LogOut
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const MainLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { icon: <LayoutDashboard size={20} />, label: 'Overview', path: '/dashboard' },
    { icon: <FileText size={20} />, label: 'My Complaints', path: '/customer/complaints' },
    { icon: <Send size={20} />, label: 'Service Requests', path: '/customer/requests' },
    { icon: <MessageSquare size={20} />, label: 'Messages', path: '/customer/messages' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div className="d-flex min-vh-100">
      {/* Sidebar */}
      <div className={`bg-white border-end ${sidebarOpen ? 'd-block' : 'd-none d-md-block'}`} 
           style={{ width: '260px', minHeight: '100vh', position: 'fixed', zIndex: 1000 }}>
        <div className="p-3">
          <div className="d-flex align-items-center justify-content-between mb-4">
            <h5 className="fw-bold text-primary mb-0">ServiceDesk</h5>
            <button className="btn btn-link d-md-none" onClick={() => setSidebarOpen(false)}>
              <X size={24} />
            </button>
          </div>
          
          <div className="mb-4 p-2 bg-light rounded-3">
            <div className="d-flex align-items-center gap-2">
              <img 
                src={user?.avatar || 'https://ui-avatars.com/api/?name=Customer'} 
                alt="Profile" 
                className="rounded-circle" 
                width={40} 
                height={40}
              />
              <div>
                <p className="fw-semibold mb-0 small">{user?.name || 'Customer'}</p>
                <p className="small text-muted mb-0">Customer</p>
              </div>
            </div>
          </div>

          <nav className="nav flex-column gap-1">
            {menuItems.map((item, index) => (
              <Link
                key={index}
                to={item.path}
                className={`nav-link d-flex align-items-center gap-3 py-2 px-3 rounded-3 ${isActive(item.path) ? 'bg-primary text-white' : 'text-dark'}`}
                style={{ textDecoration: 'none' }}
              >
                {item.icon}
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>

          <hr className="my-3" />
          
          <div className="nav flex-column gap-1">
            <Link to="/customer/feedback" className="nav-link d-flex align-items-center gap-3 py-2 px-3 rounded-3 text-dark" style={{ textDecoration: 'none' }}>
              <Star size={20} />
              <span>Give Feedback</span>
            </Link>
            <Link to="/customer/profile" className="nav-link d-flex align-items-center gap-3 py-2 px-3 rounded-3 text-dark" style={{ textDecoration: 'none' }}>
              <User size={20} />
              <span>My Profile</span>
            </Link>
          </div>

          <hr className="my-3" />
          
          <button 
            onClick={handleLogout}
            className="btn btn-outline-danger w-100 d-flex align-items-center justify-content-center gap-2"
          >
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ marginLeft: '260px', flex: 1 }}>
        {/* Top Navbar */}
        <nav className="navbar navbar-light bg-white border-bottom px-3 px-md-4" style={{ height: '60px' }}>
          <div className="d-flex align-items-center gap-3">
            <button 
              className="btn btn-link p-0 d-md-none" 
              onClick={() => setSidebarOpen(true)}
            >
              <Menu size={24} />
            </button>
            <span className="fw-semibold d-none d-sm-block">Dashboard</span>
          </div>

          <div className="d-flex align-items-center gap-3">
            <button className="btn btn-link position-relative p-0">
              <Bell size={20} />
              <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style={{ fontSize: '10px' }}>
                2
              </span>
            </button>
            
            <div className="dropdown">
              <button 
                className="btn btn-link p-0 d-flex align-items-center gap-1 text-decoration-none"
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                <img 
                  src={user?.avatar || 'https://ui-avatars.com/api/?name=Customer'} 
                  alt="Profile" 
                  className="rounded-circle" 
                  width={32} 
                  height={32}
                />
                <ChevronDown size={16} />
              </button>
              {dropdownOpen && (
                <div className="dropdown-menu dropdown-menu-end show" style={{ position: 'absolute', top: '100%', right: 0 }}>
                  <Link to="/customer/profile" className="dropdown-item">Profile</Link>
                  <Link to="/customer/feedback" className="dropdown-item">Give Feedback</Link>
                  <hr className="dropdown-divider" />
                  <button onClick={handleLogout} className="dropdown-item text-danger">Logout</button>
                </div>
              )}
            </div>
          </div>
        </nav>

        {/* Page Content */}
        <div style={{ backgroundColor: '#f0f2f5', minHeight: 'calc(100vh - 60px)' }}>
          {children}
        </div>
      </div>
    </div>
  );
};

export default MainLayout;