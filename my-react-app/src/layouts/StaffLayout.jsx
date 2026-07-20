import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Ticket, 
  MessageSquare, 
  Users, 
  Settings, 
  LogOut,
  Menu,
  X,
  Bell,
  ChevronDown
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const StaffLayout = ({ children }) => {
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
    { icon: <LayoutDashboard size={20} />, label: 'Overview', path: '/staff' },
    { icon: <Ticket size={20} />, label: 'Complaints', path: '/staff/complaints' },
    { icon: <MessageSquare size={20} />, label: 'Messages', path: '/staff/messages' },
    { icon: <Users size={20} />, label: 'Customers', path: '/staff/customers' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div className="d-flex min-vh-100">
      {/* Sidebar */}
      <div className={`bg-dark text-white ${sidebarOpen ? 'd-block' : 'd-none d-md-block'}`} 
           style={{ width: '260px', minHeight: '100vh', position: 'fixed', zIndex: 1000 }}>
        <div className="p-3">
          <div className="d-flex align-items-center justify-content-between mb-4">
            <h5 className="fw-bold mb-0">ServiceDesk</h5>
            <button className="btn btn-link text-white d-md-none" onClick={() => setSidebarOpen(false)}>
              <X size={24} />
            </button>
          </div>
          
          <div className="mb-4 p-2 bg-white bg-opacity-10 rounded-3">
            <div className="d-flex align-items-center gap-2">
              <img 
                src={user?.avatar || 'https://ui-avatars.com/api/?name=Staff'} 
                alt="Staff" 
                className="rounded-circle" 
                width={40} 
                height={40}
              />
              <div>
                <p className="fw-semibold mb-0 small">{user?.name || 'Staff Member'}</p>
                <p className="small opacity-75 mb-0">Customer Service</p>
              </div>
            </div>
          </div>

          <nav className="nav flex-column gap-1">
            {menuItems.map((item, index) => (
              <Link
                key={index}
                to={item.path}
                className={`nav-link text-white d-flex align-items-center gap-3 py-2 px-3 rounded-3 ${isActive(item.path) ? 'bg-primary' : ''}`}
                style={{ textDecoration: 'none' }}
              >
                {item.icon}
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>

          <hr className="border-secondary my-3" />
          
          <Link to="/staff/settings" className="nav-link text-white d-flex align-items-center gap-3 py-2 px-3 rounded-3" style={{ textDecoration: 'none' }}>
            <Settings size={20} />
            <span>Settings</span>
          </Link>

          <button 
            onClick={handleLogout}
            className="btn btn-outline-light w-100 d-flex align-items-center justify-content-center gap-2 mt-3"
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
          </div>

          <div className="d-flex align-items-center gap-3">
            <button className="btn btn-link position-relative p-0">
              <Bell size={20} />
              <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style={{ fontSize: '10px' }}>
                5
              </span>
            </button>
            
            <div className="dropdown">
              <button 
                className="btn btn-link p-0 d-flex align-items-center gap-1 text-decoration-none text-white"
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                <img 
                  src={user?.avatar || 'https://ui-avatars.com/api/?name=Staff'} 
                  alt="Profile" 
                  className="rounded-circle" 
                  width={32} 
                  height={32}
                />
                <ChevronDown size={16} />
              </button>
              {dropdownOpen && (
                <div className="dropdown-menu dropdown-menu-end show" style={{ position: 'absolute', top: '100%', right: 0 }}>
                  <Link to="/staff/profile" className="dropdown-item">Profile</Link>
                  <Link to="/staff/settings" className="dropdown-item">Settings</Link>
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

export default StaffLayout;