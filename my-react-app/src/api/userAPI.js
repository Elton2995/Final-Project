import axiosInstance from './axiosConfig';

export const userAPI = {
  // Admin endpoints
  getUsers: async (params) => {
    const response = await axiosInstance.get('/users', { params });
    return response.data;
  },

  getUserById: async (id) => {
    const response = await axiosInstance.get(`/users/${id}`);
    return response.data;
  },

  createUser: async (data) => {
    const response = await axiosInstance.post('/users', data);
    return response.data;
  },

  updateUser: async (id, data) => {
    const response = await axiosInstance.put(`/users/${id}`, data);
    return response.data;
  },

  deleteUser: async (id) => {
    const response = await axiosInstance.delete(`/users/${id}`);
    return response.data;
  },

  updateUserRole: async (id, role) => {
    const response = await axiosInstance.patch(`/users/${id}/role`, { role });
    return response.data;
  },

  // Customer endpoints
  updateProfile: async (data) => {
    const response = await axiosInstance.put('/users/profile', data);
    return response.data;
  },

  changePassword: async (data) => {
    const response = await axiosInstance.put('/users/change-password', data);
    return response.data;
  }
};