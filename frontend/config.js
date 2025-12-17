// Frontend Configuration
// Update API_BASE_URL based on environment

// Development (local)
const DEV_API_URL = 'http://127.0.0.1:5000/api';

// Production (update with your deployed backend URL)
const PROD_API_URL = 'https://your-app.onrender.com/api';

// Auto-detect environment
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.hostname === '';

// Export API URL
const API_BASE_URL = isDevelopment ? DEV_API_URL : PROD_API_URL;

// Make it available globally
if (typeof window !== 'undefined') {
    window.API_BASE_URL = API_BASE_URL;
}

