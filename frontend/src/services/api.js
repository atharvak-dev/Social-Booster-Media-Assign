import axios from 'axios';

const API_BASE_URL = '/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// =============================================================================
// Auth Token Management
// =============================================================================
const TOKEN_KEY = 'access_token';
const REFRESH_KEY = 'refresh_token';

export const authUtils = {
    getAccessToken: () => localStorage.getItem(TOKEN_KEY),
    getRefreshToken: () => localStorage.getItem(REFRESH_KEY),
    setTokens: (access, refresh) => {
        localStorage.setItem(TOKEN_KEY, access);
        localStorage.setItem(REFRESH_KEY, refresh);
    },
    clearTokens: () => {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(REFRESH_KEY);
    },
    isAuthenticated: () => !!localStorage.getItem(TOKEN_KEY),
};

// =============================================================================
// Request Interceptor - Add Auth Header
// =============================================================================
api.interceptors.request.use(
    (config) => {
        const token = authUtils.getAccessToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// =============================================================================
// Response Interceptor - Handle Token Refresh
// =============================================================================
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If 401 and we haven't tried to refresh yet
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const refreshToken = authUtils.getRefreshToken();
            if (refreshToken) {
                try {
                    const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
                        refresh: refreshToken
                    });
                    const { access } = response.data;
                    authUtils.setTokens(access, refreshToken);
                    originalRequest.headers.Authorization = `Bearer ${access}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    authUtils.clearTokens();
                    window.location.href = '/login';
                }
            }
        }
        return Promise.reject(error);
    }
);

// =============================================================================
// Auth API
// =============================================================================
export const authAPI = {
    login: async (username, password) => {
        const response = await api.post('/auth/token/', { username, password });
        const { access, refresh } = response.data;
        authUtils.setTokens(access, refresh);
        return response;
    },
    register: (data) => api.post('/auth/register/', data),
    logout: () => {
        authUtils.clearTokens();
    },
    getProfile: () => api.get('/auth/profile/'),
};

// =============================================================================
// Brands API
// =============================================================================
export const brandsAPI = {
    getAll: () => api.get('/brands/'),
    get: (id) => api.get(`/brands/${id}/`),
    create: (data) => api.post('/brands/', data),
    update: (id, data) => api.put(`/brands/${id}/`, data),
    delete: (id) => api.delete(`/brands/${id}/`),
};

// =============================================================================
// Rankings API
// =============================================================================
export const rankingsAPI = {
    getAll: (params) => api.get('/rankings/', { params }),
    getTrends: (brandId) => api.get(`/rankings/trends/${brandId}/`),
    getSummary: () => api.get('/rankings/summary/'),
    create: (data) => api.post('/rankings/', data),
};

// =============================================================================
// Citations API
// =============================================================================
export const citationsAPI = {
    getAll: (params) => api.get('/citations/', { params }),
    getBreakdown: () => api.get('/citations/breakdown/'),
    getSummary: () => api.get('/citations/summary/'),
    getTimeline: (params) => api.get('/citations/timeline/', { params }),
    create: (data) => api.post('/citations/', data),
};

// =============================================================================
// Reviews API
// =============================================================================
export const reviewsAPI = {
    getAll: (params) => api.get('/reviews/', { params }),
    getSummary: () => api.get('/reviews/summary/'),
    create: (data) => api.post('/reviews/', data),
};

// =============================================================================
// Dashboard API
// =============================================================================
export const dashboardAPI = {
    getOverview: (params) => api.get('/dashboard/overview/', { params }),
    export: (params) => api.get('/dashboard/export/', { params }),
};

// =============================================================================
// Integrations API
// =============================================================================
export const integrationsAPI = {
    scrapeRanking: (data) => api.post('/integrations/scrape/', data),
    bulkScrape: (data) => api.post('/integrations/bulk-scrape/', data),
    getUsage: () => api.get('/integrations/usage/'),
};

export default api;
