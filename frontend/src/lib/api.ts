import axios from 'axios';

// Ensure the API URL is properly formatted
let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Ensure the URL has the proper protocol
if (!API_BASE_URL.startsWith('http://') && !API_BASE_URL.startsWith('https://')) {
  // If it doesn't start with http/https, assume it's a domain and prepend https
  if (!API_BASE_URL.startsWith('//')) {
    API_BASE_URL = 'https://' + API_BASE_URL;
  } else {
    // If it starts with //, it's a protocol-relative URL, prepend https
    API_BASE_URL = 'https:' + API_BASE_URL;
  }
}

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