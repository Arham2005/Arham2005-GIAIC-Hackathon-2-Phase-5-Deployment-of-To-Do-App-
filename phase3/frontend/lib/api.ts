// frontend/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Helper function to get auth token from localStorage
const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
};

// Generic API request function
const apiRequest = async (endpoint: string, options: RequestInit = {}) => {
  // Ensure we get the token in the browser environment
  let token = null;
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('auth_token');
  }

  console.log(`API Request: ${endpoint}, Token exists: ${!!token}`);

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  console.log(`API Request Headers:`, headers);

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  console.log(`API Response: ${response.status} for ${endpoint}`);

  if (!response.ok) {
    if (response.status === 401) {
      // Clear invalid token if unauthorized
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
      }
    }
    const errorText = await response.text();
    console.error(`API Error: ${response.status} - ${errorText}`);
    throw new Error(`API request failed: ${response.status} - ${response.statusText}`);
  }

  return response.json();
};

// Authentication API functions
export const authAPI = {
  register: async (userData: { email: string; password: string }) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Registration failed' }));
      throw new Error(errorData.detail || 'Registration failed');
    }

    return response.json();
  },

  login: async (credentials: { email: string; password: string }) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
      throw new Error(errorData.detail || 'Login failed');
    }

    return response.json();
  },
};

// Task API functions
export const taskAPI = {
  getAll: () => apiRequest('/tasks/'),

  getById: (id: number) => apiRequest(`/tasks/${id}/`),

  create: (taskData: { title: string; description?: string }) =>
    apiRequest('/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    }),

  update: (id: number, taskData: { title?: string; description?: string; completed?: boolean }) =>
    apiRequest(`/tasks/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    }),

  delete: (id: number) =>
    apiRequest(`/tasks/${id}/`, {
      method: 'DELETE',
    }),

  complete: (id: number) =>
    apiRequest(`/tasks/${id}/complete/`, {
      method: 'POST',
    }),
};