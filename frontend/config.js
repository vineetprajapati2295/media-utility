// Frontend Configuration
// Update API_BASE_URL based on environment

(function() {
    'use strict';
    
    // Development (local)
    const DEV_API_URL = 'http://127.0.0.1:5000/api';

    // Auto-detect environment
    const isDevelopment = window.location.hostname === 'localhost' || 
                         window.location.hostname === '127.0.0.1' ||
                         window.location.hostname === '';

    // Determine API URL
    let apiBaseUrl;
    if (isDevelopment) {
        apiBaseUrl = DEV_API_URL;
    } else {
        // Production: Use same origin (backend serves frontend)
        apiBaseUrl = window.location.origin + '/api';
    }

    // Make it available globally
    window.API_BASE_URL = apiBaseUrl;
    console.log('API Base URL:', apiBaseUrl);
})();

