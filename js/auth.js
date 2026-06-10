// Authentication Logic
const API_URL = (window.IKORA_CONFIG && window.IKORA_CONFIG.API_BASE) || 'http://localhost:3000/api';

// Get form elements
const loginCard = document.getElementById('loginCard');
const signupCard = document.getElementById('signupCard');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const showSignupLink = document.getElementById('showSignup');
const showLoginLink = document.getElementById('showLogin');
const loginError = document.getElementById('loginError');
const signupError = document.getElementById('signupError');

// Debug: Check if elements are found
console.log('Auth.js loaded');
console.log('Login form:', loginForm);
console.log('Signup form:', signupForm);

// Switch between login and signup
if (showSignupLink) {
    showSignupLink.addEventListener('click', (e) => {
        e.preventDefault();
        loginCard.style.display = 'none';
        signupCard.style.display = 'block';
        loginError.textContent = '';
    });
}

if (showLoginLink) {
    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        signupCard.style.display = 'none';
        loginCard.style.display = 'block';
        signupError.textContent = '';
    });
}

// Check if already logged in
const currentToken = localStorage.getItem('ikora_token');
if (currentToken && window.location.pathname.includes('auth.html')) {
    // Verify if token is still valid
    fetch(window.IKORA_CONFIG?.API_BASE?.replace('/api','') + '/health' || 'http://localhost:3000/health')
        .then(response => {
            if (response.ok) {
                // Backend is running, redirect to dashboard
                window.location.href = 'dashboard.html';
            }
        })
        .catch(() => {
            // Backend not running, clear token
            localStorage.removeItem('ikora_token');
            localStorage.removeItem('ikora_user');
        });
}

// Login Form Submit
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Login form submitted');
        
        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;
        
        console.log('Username:', username);
        console.log('Password length:', password.length);
        
        if (!username || !password) {
            showError(loginError, 'Please fill in all fields');
            return;
        }
        
        // Disable submit button
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Signing in...';
        
        try {
            // Check if backend is running
            console.log('Checking backend...');
            let backendAvailable = false;
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 2000); // 2 second timeout
                
                const healthCheck = await fetch('http://localhost:3000/health', { 
                    method: 'GET',
                    signal: controller.signal
                });
                clearTimeout(timeoutId);
                
                if (healthCheck.ok) {
                    backendAvailable = true;
                    console.log('Backend is running');
                }
            } catch (error) {
                console.log('Backend not available, using offline mode');
                backendAvailable = false;
            }
            
            if (backendAvailable) {
                // Use backend authentication
                console.log('Sending login request...');
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                console.log('Login response:', data);
                
                if (!response.ok) {
                    throw new Error(data.error || 'Login failed');
                }
                
                // Save token and user info
                localStorage.setItem('ikora_token', data.token);
                localStorage.setItem('ikora_user', JSON.stringify(data.user));
            } else {
                // Offline mode - simple validation
                console.log('Using offline authentication');
                
                // Get stored users or create demo user
                let users = JSON.parse(localStorage.getItem('ikora_offline_users') || '[]');
                
                // Check if user exists
                const user = users.find(u => u.username === username && u.password === password);
                
                if (!user) {
                    throw new Error('Invalid username or password. Try creating an account first.');
                }
                
                // Create simple token
                const token = 'offline_' + Date.now();
                localStorage.setItem('ikora_token', token);
                localStorage.setItem('ikora_user', JSON.stringify({ username: user.username, id: user.id }));
            }
            
            // Show success message
            showSuccess(loginError, 'Login successful!');
            
            // Show loading screen and redirect
            if (typeof showAuthLoading === 'function') {
                showAuthLoading('Welcome back! Preparing your wellness space...');
            } else {
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);
            }
            
        } catch (error) {
            console.error('Login error:', error);
            showError(loginError, error.message || 'Invalid username or password');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Sign In';
        }
    });
} else {
    console.error('Login form not found!');
}

// Signup Form Submit
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Signup form submitted');
        
        const username = document.getElementById('signupUsername').value.trim();
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        console.log('Username:', username);
        console.log('Password length:', password.length);
        
        // Validation
        if (!username || !password || !confirmPassword) {
            showError(signupError, 'Please fill in all fields');
            return;
        }
        
        if (username.length < 3) {
            showError(signupError, 'Username must be at least 3 characters');
            return;
        }
        
        if (password.length < 6) {
            showError(signupError, 'Password must be at least 6 characters');
            return;
        }
        
        if (password !== confirmPassword) {
            showError(signupError, 'Passwords do not match');
            return;
        }
        
        // Disable submit button
        const submitBtn = signupForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating account...';
        
        try {
            // Check if backend is running
            console.log('Checking backend...');
            let backendAvailable = false;
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 2000); // 2 second timeout
                
                const healthCheck = await fetch('http://localhost:3000/health', {
                    method: 'GET',
                    signal: controller.signal
                });
                clearTimeout(timeoutId);
                
                if (healthCheck.ok) {
                    backendAvailable = true;
                    console.log('Backend is running');
                }
            } catch (error) {
                console.log('Backend not available, using offline mode');
                backendAvailable = false;
            }
            
            if (backendAvailable) {
                // Use backend registration
                console.log('Sending registration request...');
                const response = await fetch(`${API_URL}/auth/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                console.log('Registration response:', data);
                
                if (!response.ok) {
                    throw new Error(data.error || 'Registration failed');
                }
                
                // Save token and user info
                localStorage.setItem('ikora_token', data.token);
                localStorage.setItem('ikora_user', JSON.stringify(data.user));
            } else {
                // Offline mode - store user locally
                console.log('Using offline registration');
                
                // Get stored users
                let users = JSON.parse(localStorage.getItem('ikora_offline_users') || '[]');
                
                // Check if username already exists
                if (users.find(u => u.username === username)) {
                    throw new Error('Username already exists');
                }
                
                // Create new user
                const newUser = {
                    id: Date.now(),
                    username: username,
                    password: password // In real app, this should be hashed
                };
                
                users.push(newUser);
                localStorage.setItem('ikora_offline_users', JSON.stringify(users));
                
                // Create simple token
                const token = 'offline_' + Date.now();
                localStorage.setItem('ikora_token', token);
                localStorage.setItem('ikora_user', JSON.stringify({ username: newUser.username, id: newUser.id }));
            }
            
            // Show success message
            showSuccess(signupError, 'Account created!');
            
            // Show loading screen and redirect
            if (typeof showAuthLoading === 'function') {
                showAuthLoading('Welcome to IKORA! Setting up your wellness journey...');
            } else {
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);
            }
            
        } catch (error) {
            console.error('Signup error:', error);
            showError(signupError, error.message || 'Username already exists or registration failed');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Account';
        }
    });
} else {
    console.error('Signup form not found!');
}

// Helper functions
function showError(element, message) {
    element.textContent = message;
    element.style.color = '#ff6b6b';
    element.style.display = 'block';
}

function showSuccess(element, message) {
    element.textContent = message;
    element.style.color = '#51cf66';
    element.style.display = 'block';
}
