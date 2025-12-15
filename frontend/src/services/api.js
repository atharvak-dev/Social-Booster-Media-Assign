import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Brands API
export const brandsAPI = {
    getAll: () => api.get('/brands/'),
    get: (id) => api.get(`/brands/${id}/`),
    create: (data) => api.post('/brands/', data),
    update: (id, data) => api.put(`/brands/${id}/`, data),
    delete: (id) => api.delete(`/brands/${id}/`),
};

// Rankings API
export const rankingsAPI = {
    getAll: (params) => api.get('/rankings/', { params }),
    getTrends: (brandId) => api.get(`/rankings/trends/${brandId}/`),
    getSummary: () => api.get('/rankings/summary/'),
    create: (data) => api.post('/rankings/', data),
};

// Citations API
export const citationsAPI = {
    getAll: (params) => api.get('/citations/', { params }),
    getBreakdown: () => api.get('/citations/breakdown/'),
    getSummary: () => api.get('/citations/summary/'),
    getTimeline: (params) => api.get('/citations/timeline/', { params }),
    create: (data) => api.post('/citations/', data),
};

// Reviews API
export const reviewsAPI = {
    getAll: (params) => api.get('/reviews/', { params }),
    getSummary: () => api.get('/reviews/summary/'),
    create: (data) => api.post('/reviews/', data),
};

// Dashboard API
export const dashboardAPI = {
    getOverview: (params) => api.get('/dashboard/overview/', { params }),
    export: (params) => api.get('/dashboard/export/', { params }),
};

// Integrations API
export const integrationsAPI = {
    scrapeRanking: (data) => api.post('/integrations/scrape/', data),
    bulkScrape: (data) => api.post('/integrations/bulk-scrape/', data),
    getUsage: () => api.get('/integrations/usage/'),
};

export default api;
