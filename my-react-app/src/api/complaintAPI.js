import axiosInstance from './axiosConfig';

export const complaintAPI = {
  // Customer endpoints
  getMyComplaints: async () => {
    const response = await axiosInstance.get('/complaints/my');
    return response.data;
  },

  getMyRequests: async () => {
    const response = await axiosInstance.get('/complaints/my-requests');
    return response.data;
  },

  createComplaint: async (data) => {
    const response = await axiosInstance.post('/complaints', data);
    return response.data;
  },

  createRequest: async (data) => {
    const response = await axiosInstance.post('/complaints/request', data);
    return response.data;
  },

  getComplaintById: async (id) => {
    const response = await axiosInstance.get(`/complaints/${id}`);
    return response.data;
  },

  updateComplaint: async (id, data) => {
    const response = await axiosInstance.put(`/complaints/${id}`, data);
    return response.data;
  },

  // Staff endpoints
  getAssignedComplaints: async () => {
    const response = await axiosInstance.get('/complaints/assigned');
    return response.data;
  },

  updateComplaintStatus: async (id, status) => {
    const response = await axiosInstance.patch(`/complaints/${id}/status`, { status });
    return response.data;
  },

  addResponse: async (id, data) => {
    const response = await axiosInstance.post(`/complaints/${id}/response`, data);
    return response.data;
  },

  // Admin endpoints
  getAllComplaints: async (params) => {
    const response = await axiosInstance.get('/complaints', { params });
    return response.data;
  },

  getStats: async () => {
    const response = await axiosInstance.get('/complaints/stats');
    return response.data;
  },

  generateReport: async (params) => {
    const response = await axiosInstance.get('/complaints/report', { params });
    return response.data;
  },

  // Feedback
  submitFeedback: async (data) => {
    const response = await axiosInstance.post('/feedback', data);
    return response.data;
  },

  getFeedback: async () => {
    const response = await axiosInstance.get('/feedback');
    return response.data;
  }
};