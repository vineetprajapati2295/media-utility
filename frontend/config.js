// Frontend Configuration
// Update API_BASE_URL based on environment

// Development (local)
const DEV_API_URL = 'http://127.0.0.1:5000/api';

// Production - UPDATE THIS WITH YOUR ACTUAL RENDER URL
// Example: https://media-utility.onrender.com/api
// Get your URL from Render dashboard after deployment
const PROD_API_URL = window.location.origin + '/api'; // Use same origin if served from backend

// Auto-detect environment
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.hostname === '';

// If served from Render backend, use same origin
// If frontend is separate, you need to set PROD_API_URL above
let API_BASE_URL;
if (isDevelopment) {
    API_BASE_URL = DEV_API_URL;
} else {
    // Check if we're on Render (or same origin)
    if (window.location.hostname.includes('onrender.com') || 
        window.location.hostname.includes('railway.app') ||
        window.location.hostname.includes('fly.dev')) {
        // Backend serves frontend, so use same origin
        API_BASE_URL = window.location.origin + '/api';
    } else {
        // Frontend is separate, use PROD_API_URL (update this!)
        API_BASE_URL = PROD_API_URL;
    }
}

// Make it available globally
if (typeof window !== 'undefined') {
    window.API_BASE_URL = API_BASE_URL;
    console.log('API Base URL:', API_BASE_URL);
}

