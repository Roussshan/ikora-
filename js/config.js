/**
 * IKORA - API Configuration
 *
 * LOCAL DEV  : API_BASE = 'http://localhost:3000/api'
 * PRODUCTION : API_BASE = 'https://your-app.onrender.com/api'
 *
 * Change API_BASE below when you deploy the backend to Render.
 */

const CONFIG = {
    // ── Change this to your Render URL after deploying the backend ──
    API_BASE: 'https://ikora.onrender.com'

    // Fallback to localhost during local development
    // Uncomment the line below and comment the one above while working locally:
    // API_BASE: 'http://localhost:3000/api',
};

// Auto-detect: use localhost if running from localhost
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    CONFIG.API_BASE = 'http://localhost:3000/api';
}

window.IKORA_CONFIG = CONFIG;
