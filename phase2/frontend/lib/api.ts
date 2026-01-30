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

  create: (taskData: {
    title: string;
    description?: string;
    priority?: string;
    tags?: string[];
    due_date?: string;
    recurring?: boolean;
    recurrence_pattern?: string;
    parent_task_id?: number;
  }) =>
    apiRequest('/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    }),

  update: (id: number, taskData: {
    title?: string;
    description?: string;
    completed?: boolean;
    priority?: string;
    tags?: string[];
    due_date?: string;
    recurring?: boolean;
    recurrence_pattern?: string;
    parent_task_id?: number;
    reminder_sent?: boolean;
  }) =>
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

  // Additional API functions for advanced features
  getDueSoon: (daysAhead: number = 3) => apiRequest(`/tasks/due-soon/?days_ahead=${daysAhead}`),

  getRecurring: () => apiRequest(`/tasks/recurring/`),

  filter: (params: {
    completed?: boolean;
    priority?: string;
    tags?: string[];
    due_date_from?: string;
    due_date_to?: string;
    search_query?: string;
    sort_by?: string;
    sort_order?: string;
  }) => {
    const queryParams = new URLSearchParams();
    if (params.completed !== undefined) queryParams.append('completed', params.completed.toString());
    if (params.priority) queryParams.append('priority', params.priority);
    if (params.tags) queryParams.append('tags', params.tags.join(','));
    if (params.due_date_from) queryParams.append('due_date_from', params.due_date_from);
    if (params.due_date_to) queryParams.append('due_date_to', params.due_date_to);
    if (params.search_query) queryParams.append('search_query', params.search_query);
    if (params.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params.sort_order) queryParams.append('sort_order', params.sort_order);

    return apiRequest(`/tasks/?${queryParams.toString()}`);
  },
};