import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from '../context/AuthContext';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import RoleProtectedRoute from '../components/auth/RoleProtectedRoute';

// Public Pages
import LandingPage from '../pages/LandingPage';
import RegisterPage from '../pages/RegisterPage';

// Customer Pages
import CustomerDashboard from '../pages/CustomerDashboard';
import MyComplaints from '../pages/customer/MyComplaints';
import SubmitComplaint from '../pages/customer/SubmitComplaint';
import ServiceRequests from '../pages/customer/ServiceRequests';
import SubmitRequest from '../pages/customer/SubmitRequest';
import Messages from '../pages/customer/Messages';
import GiveFeedback from '../pages/customer/GiveFeedback';
import MyProfile from '../pages/customer/MyProfile';

// Admin Pages
import AdminDashboard from '../pages/AdminDashboard';

// Staff Pages
import StaffDashboard from '../pages/StaffDashboard';

const AppRoutes = () => {
  return (
    <AuthProvider>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LandingPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected Routes - Any authenticated user */}
        <Route element={<ProtectedRoute />}>
          {/* Customer Routes - All authenticated users can access */}
          <Route path="/dashboard" element={<CustomerDashboard />} />
          <Route path="/customer/complaints" element={<MyComplaints />} />
          <Route path="/customer/complaints/new" element={<SubmitComplaint />} />
          <Route path="/customer/requests" element={<ServiceRequests />} />
          <Route path="/customer/requests/new" element={<SubmitRequest />} />
          <Route path="/customer/messages" element={<Messages />} />
          <Route path="/customer/feedback" element={<GiveFeedback />} />
          <Route path="/customer/profile" element={<MyProfile />} />
        </Route>

        {/* Admin Routes - Only users with 'admin' role */}
        <Route element={<RoleProtectedRoute allowedRoles={['admin']} />}>
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/*" element={<AdminDashboard />} />
        </Route>

        {/* Staff Routes - Only users with 'staff' or 'admin' role */}
        <Route element={<RoleProtectedRoute allowedRoles={['staff', 'admin']} />}>
          <Route path="/staff" element={<StaffDashboard />} />
          <Route path="/staff/*" element={<StaffDashboard />} />
        </Route>

        {/* 404 Redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
};

export default AppRoutes;