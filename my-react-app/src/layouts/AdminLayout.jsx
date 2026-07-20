import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  Ticket, 
  BarChart3, 
  Settings, 
  LogOut,
  Menu,
  X,
  ChevronDown,
  Bell,
  Search
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const AdminLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { icon: <LayoutDashboard size={20} />, label: 'Overview', path: '/admin' },
    { icon: <Ticket size={20} />, label: 'Complaints', path: '/admin/complaints' },
    { icon: <Users size={20} />, label: 'Users', path: '/admin/users' },
    { icon: <BarChart3 size={20} />, label: 'Reports', path: '/admin/reports' },
    { icon: <Settings size={20} />, label: 'Settings', path: '/admin/settings' },
  ];

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
                src={user?.avatar || 'https://ui-avatars.com/api/?name=Admin'} 
                alt="Admin" 
                className="rounded-circle" 
                width={40} 
                height={40}
              />
              <div>
                <p className="fw-semibold mb-0 small">{user?.name || 'Admin'}</p>
                <p className="small opacity-75 mb-0">Administrator</p>
              </div>
            </div>
          </div>

          <nav className="nav flex-column gap-1">
            {menuItems.map((item, index) => (
              <Link
                key={index}
                to={item.path}
                className="nav-link text-white d-flex align-items-center gap-3 py-2 px-3 rounded-3 hover-lift"
                style={{ textDecoration: 'none' }}
              >
                {item.icon}
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>

          <hr className="border-secondary my-3" />
          
          <button 
            onClick={handleLogout}
            className="btn btn-outline-light w-100 d-flex align-items-center justify-content-center gap-2"
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
            <div className="position-relative d-none d-sm-block">
              <Search size={18} className="position-absolute text-muted" style={{ left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
              <input 
                type="text" 
                className="form-control form-control-sm ps-5" 
                placeholder="Search..." 
                style={{ width: '250px' }}
              />
            </div>
          </div>

          <div className="d-flex align-items-center gap-3">
            <button className="btn btn-link position-relative p-0">
              <Bell size={20} />
              <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style={{ fontSize: '10px' }}>
                3
              </span>
            </button>
            
            <div className="dropdown">
              <button 
                className="btn btn-link p-0 d-flex align-items-center gap-1 text-decoration-none"
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                <img 
                  src={user?.avatar || 'https://ui-avatars.com/api/?name=Admin'} 
                  alt="Profile" 
                  className="rounded-circle" 
                  width={32} 
                  height={32}
                />
                <ChevronDown size={16} />
              </button>
              {dropdownOpen && (
                <div className="dropdown-menu dropdown-menu-end show" style={{ position: 'absolute', top: '100%', right: 0 }}>
                  <Link to="/admin/profile" className="dropdown-item">Profile</Link>
                  <Link to="/admin/settings" className="dropdown-item">Settings</Link>
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

export default AdminLayout;