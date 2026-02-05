import axios from 'axios';

// Use the deployed backend URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://irajfatima-phase2-backend.hf.space';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('better-auth-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle responses globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Redirect to login or clear auth state
      localStorage.removeItem('better-auth-token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;