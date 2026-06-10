// Create floating particles animation - DISABLED
function createParticles() {
    // Disabled for clean design
    return;
}

// Create wellness background animations
function createWellnessBackground() {
    const body = document.body;
    
    // Create wellness background container
    const wellnessBg = document.createElement('div');
    wellnessBg.className = 'wellness-bg';
    body.insertBefore(wellnessBg, body.firstChild);
    
    // Create floating lotus flowers
    for (let i = 0; i < 8; i++) {
        const lotus = document.createElement('div');
        lotus.className = 'lotus';
        lotus.textContent = '🪷';
        lotus.style.left = Math.random() * 100 + '%';
        lotus.style.animationDelay = Math.random() * 20 + 's';
        lotus.style.animationDuration = (15 + Math.random() * 10) + 's';
        wellnessBg.appendChild(lotus);
    }
    
    // Create breathing circles
    for (let i = 0; i < 5; i++) {
        const circle = document.createElement('div');
        circle.className = 'breathing-circle';
        const size = 100 + Math.random() * 200;
        circle.style.width = size + 'px';
        circle.style.height = size + 'px';
        circle.style.left = Math.random() * 100 + '%';
        circle.style.top = Math.random() * 100 + '%';
        circle.style.animationDelay = Math.random() * 6 + 's';
        wellnessBg.appendChild(circle);
    }
    
    // Create zen circles
    for (let i = 0; i < 6; i++) {
        const zenCircle = document.createElement('div');
        zenCircle.className = 'zen-circle';
        const size = 80 + Math.random() * 150;
        zenCircle.style.width = size + 'px';
        zenCircle.style.height = size + 'px';
        zenCircle.style.left = Math.random() * 100 + '%';
        zenCircle.style.top = Math.random() * 100 + '%';
        zenCircle.style.animationDelay = Math.random() * 8 + 's';
        wellnessBg.appendChild(zenCircle);
    }
    
    // Create peaceful dots
    for (let i = 0; i < 30; i++) {
        const dot = document.createElement('div');
        dot.className = 'peace-dot';
        dot.style.left = Math.random() * 100 + '%';
        dot.style.animationDelay = Math.random() * 15 + 's';
        wellnessBg.appendChild(dot);
    }
    
    // Create meditation auras
    for (let i = 0; i < 4; i++) {
        const aura = document.createElement('div');
        aura.className = 'aura';
        const size = 200 + Math.random() * 300;
        aura.style.width = size + 'px';
        aura.style.height = size + 'px';
        aura.style.left = Math.random() * 100 + '%';
        aura.style.top = Math.random() * 100 + '%';
        aura.style.animationDelay = Math.random() * 10 + 's';
        wellnessBg.appendChild(aura);
    }
    
    // Create mandalas
    const mandalaSVG = `
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="0.5"/>
            <circle cx="50" cy="50" r="30" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="0.5"/>
            <circle cx="50" cy="50" r="20" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="0.5"/>
            <circle cx="50" cy="50" r="10" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="0.5"/>
            <line x1="50" y1="10" x2="50" y2="90" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
            <line x1="10" y1="50" x2="90" y2="50" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
            <line x1="20" y1="20" x2="80" y2="80" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
            <line x1="80" y1="20" x2="20" y2="80" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
        </svg>
    `;
    
    for (let i = 0; i < 4; i++) {
        const mandala = document.createElement('div');
        mandala.className = 'mandala';
        mandala.innerHTML = mandalaSVG;
        mandala.style.left = Math.random() * 100 + '%';
        mandala.style.top = Math.random() * 100 + '%';
        mandala.style.animationDelay = Math.random() * 30 + 's';
        wellnessBg.appendChild(mandala);
    }
}

// Initialize animations on page load - DISABLED
// createParticles();
// createWellnessBackground();

// Chat functionality
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const chatMessages = document.getElementById('chatMessages');

// Ikora Chatbot Backend Integration
const API_URL = (window.IKORA_CONFIG && window.IKORA_CONFIG.API_BASE) || 'http://localhost:3000/api';
let authToken = null;
let currentUserId = null;
let backendAvailable = false;

// Initialize chatbot connection
async function initChatbot() {
    // Check if backend is available
    try {
        const healthCheck = await fetch(window.IKORA_CONFIG?.API_BASE?.replace('/api','') + '/health' || 'http://localhost:3000/health');
        if (healthCheck.ok) {
            backendAvailable = true;
            console.log('✅ Backend connected successfully');
        }
    } catch (error) {
        backendAvailable = false;
        console.log('⚠️ Backend not available - using offline mode');
    }
    
    if (backendAvailable) {
        authToken = localStorage.getItem('ikora_token');
        
        if (chatMessages && authToken) {
            await loadChatHistory();
        }
    }
}

// Load chat history from backend
async function loadChatHistory() {
    if (!authToken || !backendAvailable) return;
    
    try {
        const response = await fetch(`${API_URL}/chat/history?limit=20`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!response.ok) {
            // Token expired
            if (response.status === 401) {
                localStorage.removeItem('ikora_token');
                localStorage.removeItem('ikora_user');
                window.location.href = 'auth.html';
                return;
            }
            throw new Error('Failed to load history');
        }
        
        const data = await response.json();
        const messages = data.messages || [];
        
        if (messages.length > 0) {
            // Clear initial message
            chatMessages.innerHTML = '';
            
            messages.forEach(msg => {
                addMessage(msg.content, msg.sender === 'user');
            });
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Sample Gita responses (fallback for offline mode)
const gitaResponses = [
    {
        keywords: ['anxiety', 'anxious', 'worried', 'worry', 'nervous', 'stress', 'stressed'],
        response: 'The Gita teaches us in Chapter 2, Verse 47: "You have the right to perform your prescribed duty, but you are not entitled to the fruits of action." Focus on your actions, not the outcomes. Anxiety often comes from attachment to results. Practice detachment and do your best.'
    },
    {
        keywords: ['purpose', 'meaning', 'why', 'direction', 'lost', 'confused'],
        response: 'Lord Krishna says in Chapter 3, Verse 35: "It is better to engage in one\'s own occupation, even though one may perform it imperfectly, than to accept another\'s occupation and perform it perfectly." Your purpose lies in your unique path. Discover your dharma through self-reflection.'
    },
    {
        keywords: ['loss', 'death', 'died', 'grief', 'sad', 'sadness', 'miss'],
        response: 'In Chapter 2, Verse 20, Krishna teaches: "The soul is neither born, and nor does it die. It is eternal, indestructible, and timeless." What we perceive as loss is transformation. The essence of what we love never truly leaves us.'
    },
    {
        keywords: ['peace', 'calm', 'quiet', 'tranquil', 'serenity'],
        response: 'Chapter 2, Verse 66 states: "One who is not connected with the Supreme can have neither transcendental intelligence nor a steady mind, without which there is no possibility of peace." Inner peace comes from connecting with your higher self through meditation and self-awareness.'
    },
    {
        keywords: ['anger', 'angry', 'mad', 'frustrated', 'irritated'],
        response: 'In Chapter 2, Verse 63, Krishna warns: "From anger comes delusion; from delusion, loss of memory; from loss of memory, destruction of discrimination; from destruction of discrimination, one perishes." Take a moment to breathe and observe your anger without acting on it.'
    },
    {
        keywords: ['fear', 'afraid', 'scared', 'frightened'],
        response: 'Chapter 11, Verse 50 reminds us: "Do not fear what is not real, do not fear what is real." Most fears exist only in our minds. Face them with courage, knowing that your true self is beyond harm.'
    },
    {
        keywords: ['happy', 'happiness', 'joy', 'content'],
        response: 'The Gita teaches in Chapter 5, Verse 21: "One who is not attached to external pleasures but finds joy within, realizes the bliss that is eternal." True happiness comes from within, not from external circumstances.'
    },
    {
        keywords: ['work', 'job', 'career', 'duty'],
        response: 'Chapter 3, Verse 19 says: "Therefore, without attachment, perform always the work that has to be done, for by working without attachment, one attains the Supreme." Do your work with dedication but without attachment to results.'
    }
];

function getGitaResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Find matching response based on keywords
    for (let response of gitaResponses) {
        for (let keyword of response.keywords) {
            if (lowerMessage.includes(keyword)) {
                return response.response;
            }
        }
    }
    
    // Default response
    return 'The Bhagavad Gita teaches us that true wisdom comes from within. In Chapter 6, Verse 5: "Elevate yourself through the power of your mind, and not degrade yourself, for the mind can be the friend and also the enemy of the self." How can I guide you further on your journey?';
}

function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    
    if (isUser) {
        avatar.textContent = '👤';
    } else {
        const img = document.createElement('img');
        img.src = 'assets/ikora.png';
        img.alt = 'Ikora';
        img.className = 'message-avatar-image';
        avatar.appendChild(img);
    }
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const p = document.createElement('p');
    p.textContent = text;
    content.appendChild(p);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show loading indicator
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.id = 'loading-message';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    const img = document.createElement('img');
    img.src = 'assets/ikora.png';
    img.alt = 'Ikora';
    img.className = 'message-avatar-image';
    avatar.appendChild(img);
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const dotsDiv = document.createElement('div');
    dotsDiv.className = 'loading-dots';
    dotsDiv.innerHTML = '<span></span><span></span><span></span>';
    
    content.appendChild(dotsDiv);
    loadingDiv.appendChild(avatar);
    loadingDiv.appendChild(content);
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove loading indicator
function removeLoading() {
    const loading = document.getElementById('loading-message');
    if (loading) {
        loading.remove();
    }
}

if (chatForm) {
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message
        addMessage(message, true);
        chatInput.value = '';
        
        // Show loading
        showLoading();
        
        // Try to send to backend first if available
        if (backendAvailable && authToken) {
            try {
                const response = await fetch(`${API_URL}/chat/message`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`
                    },
                    body: JSON.stringify({ message })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    
                    // Remove loading
                    removeLoading();
                    
                    // Add backend response
                    addMessage(data.response, false);
                    return;
                }

                // Token expired or invalid → force re-login
                if (response.status === 401) {
                    removeLoading();
                    localStorage.removeItem('ikora_token');
                    localStorage.removeItem('ikora_user');
                    alert('Your session has expired. Please log in again.');
                    window.location.href = 'auth.html';
                    return;
                }
                
            } catch (error) {
                console.error('Backend error:', error);
                backendAvailable = false;
            }
        }
        
        // Fallback to offline mode with varied responses
        setTimeout(() => {
            removeLoading();
            const response = getGitaResponse(message);
            addMessage(response, false);
        }, 800);
    });
}

// Initialize chatbot when on dashboard page
if (window.location.pathname.includes('dashboard.html')) {
    // Check if user is logged in
    const token = localStorage.getItem('ikora_token');
    const user = JSON.parse(localStorage.getItem('ikora_user') || '{}');
    
    if (!token) {
        // Redirect to auth page if not logged in
        alert('Please login to access the chatbot');
        window.location.href = 'auth.html';
    } else {
        // Display user greeting
        const userGreeting = document.getElementById('userGreeting');
        if (userGreeting && user.username) {
            userGreeting.textContent = `Welcome, ${user.username}`;
        }
        
        // Setup logout button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                localStorage.removeItem('ikora_token');
                localStorage.removeItem('ikora_user');
                alert('Logged out successfully!');
                window.location.href = 'auth.html';
            });
        }
        
        // Initialize chatbot
        initChatbot();
    }
}

// Quick topic buttons
function sendQuickMessage(message) {
    if (chatInput) {
        chatInput.value = message;
        chatForm.dispatchEvent(new Event('submit'));
    }
}

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});


// Create soft blinking stars
function createBlinkingStars() {
    const starsContainer = document.getElementById('starsContainer');
    if (!starsContainer) return;
    
    const starCount = 80; // Number of stars
    const sizes = ['star-small', 'star-medium', 'star-large'];
    const speeds = ['', 'star-slow', 'star-gentle'];
    
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        
        // Random size
        const sizeClass = sizes[Math.floor(Math.random() * sizes.length)];
        star.classList.add(sizeClass);
        
        // Random animation speed
        const speedClass = speeds[Math.floor(Math.random() * speeds.length)];
        if (speedClass) star.classList.add(speedClass);
        
        // Random position
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        
        // Random animation delay for variety
        star.style.animationDelay = Math.random() * 4 + 's';
        
        starsContainer.appendChild(star);
    }
}

// Initialize blinking stars on homepage
if (document.getElementById('starsContainer')) {
    createBlinkingStars();
}

// Create galaxy animation
function createGalaxy() {
    const galaxyContainer = document.getElementById('galaxyContainer');
    if (!galaxyContainer) return;
    
    // Create twinkling stars
    const starCount = 150;
    const sizes = ['galaxy-star-small', 'galaxy-star-medium', 'galaxy-star-large'];
    
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'galaxy-star';
        
        // Random size
        const sizeClass = sizes[Math.floor(Math.random() * sizes.length)];
        star.classList.add(sizeClass);
        
        // Random position
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        
        // Random animation delay
        star.style.animationDelay = Math.random() * 3 + 's';
        star.style.animationDuration = (2 + Math.random() * 3) + 's';
        
        galaxyContainer.appendChild(star);
    }
    
    // Create stardust particles
    const stardustCount = 50;
    
    for (let i = 0; i < stardustCount; i++) {
        const dust = document.createElement('div');
        dust.className = 'stardust';
        
        // Random position
        dust.style.left = Math.random() * 100 + '%';
        dust.style.bottom = '0';
        
        // Random animation delay and duration
        dust.style.animationDelay = Math.random() * 15 + 's';
        dust.style.animationDuration = (10 + Math.random() * 10) + 's';
        
        galaxyContainer.appendChild(dust);
    }
}

// Initialize galaxy animation
if (document.getElementById('galaxyContainer')) {
    createGalaxy();
}

// Create Twinkling Stars
function createTwinklingStars() {
    const starsContainer = document.getElementById('starsContainer');
    if (!starsContainer) return;
    
    const starCount = 40; // Reduced number of stars
    const sizes = ['star-tiny', 'star-small'];
    
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'twinkle-star';
        
        // Random size - only tiny and small
        const sizeClass = Math.random() < 0.7 ? sizes[0] : sizes[1];
        star.classList.add(sizeClass);
        
        // Random position
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        
        // Random animation delay and duration for varied twinkling
        star.style.animationDelay = Math.random() * 3 + 's';
        star.style.animationDuration = (2 + Math.random() * 2) + 's';
        
        starsContainer.appendChild(star);
    }
}

// Initialize twinkling stars
if (document.getElementById('starsContainer')) {
    createTwinklingStars();
}





// Scroll Animations with Different Effects per Section
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add animation when scrolling into view
                entry.target.classList.add('animate-in');
            } else {
                // Remove animation when scrolling out of view (so it can animate again)
                entry.target.classList.remove('animate-in');
            }
        });
    }, observerOptions);
    
    // Different animations for different sections
    const animationMap = {
        '.content-title': 'fade-up',
        '.intro-section': 'fade-left',
        '.how-it-works': 'zoom-in',
        '.step-card': 'bounce-in',
        '.inspiration-section': 'fade-right',
        '.why-gita': 'flip-in',
        '.benefit-item': 'rotate-in',
        '.cta-final': 'slide-bounce',
        '.feature-card': 'zoom-in',
        // Wisdom page animations
        '.about-hero': 'fade-up',
        '.wisdom-card-transparent': 'zoom-in',
        '.key-teachings': 'fade-up',
        '.teaching-flow-card': 'bounce-in',
        '.flow-arrow': 'fade-up',
        '.cta-section-transparent': 'slide-bounce',
        // New features animations
        '.quote-of-day': 'zoom-in',
        '.testimonials-section': 'fade-up',
        '.breathing-exercise': 'fade-up'
    };
    
    // Apply animations to each section type
    Object.keys(animationMap).forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach((element, index) => {
            element.classList.add('scroll-animate', animationMap[selector]);
            // Stagger animation for multiple items
            element.style.transitionDelay = (index * 0.1) + 's';
            observer.observe(element);
        });
    });
}

// Initialize scroll animations on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollAnimations);
} else {
    initScrollAnimations();
}


// ========================================
// LOADING SCREEN (Removed from page load)
// ========================================
// Loading screen now only shows after login/signup

// Function to show loading screen with custom message
function showAuthLoading(message) {
    const loadingScreen = document.getElementById('authLoadingScreen');
    const loadingMessage = document.getElementById('loadingMessage');
    
    if (loadingScreen) {
        if (loadingMessage && message) {
            loadingMessage.textContent = message;
        }
        loadingScreen.style.display = 'flex';
        
        // Redirect after 2.5 seconds
        setTimeout(function() {
            window.location.href = 'dashboard.html';
        }, 2500);
    }
}

// Make function globally available
window.showAuthLoading = showAuthLoading;

// ========================================
// PAGE TRANSITIONS
// ========================================
function initPageTransitions() {
    const pageLinks = document.querySelectorAll('.page-link');
    const transition = document.querySelector('.page-transition');
    
    if (!transition) return;
    
    pageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Don't transition if it's the current page
            if (href && href !== '#' && !href.startsWith('javascript:')) {
                e.preventDefault();
                
                // Start transition
                transition.classList.add('active');
                
                // Navigate after animation
                setTimeout(function() {
                    window.location.href = href;
                }, 400);
            }
        });
    });
}

// ========================================
// DARK MODE TOGGLE
// ========================================
function initDarkMode() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('ikora-theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }
    
    themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        
        // Save preference
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('ikora-theme', 'dark');
        } else {
            localStorage.setItem('ikora-theme', 'light');
        }
    });
}

// ========================================
// PARALLAX SCROLLING
// ========================================
function initParallax() {
    const orbs = document.querySelectorAll('.color-orb-bg');
    
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        
        orbs.forEach((orb, index) => {
            const speed = 0.1 + (index * 0.05); // Different speeds for each orb
            const yPos = -(scrolled * speed);
            orb.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// ========================================
// QUOTE OF THE DAY
// ========================================
const bhagavadGitaQuotes = [
    {
        text: "You have the right to perform your prescribed duty, but you are not entitled to the fruits of action. Never consider yourself to be the cause of the results of your activities, nor be attached to inaction.",
        reference: "Bhagavad Gita 2.47"
    },
    {
        text: "The soul is neither born, and nor does it die. It is eternal, indestructible, and timeless.",
        reference: "Bhagavad Gita 2.20"
    },
    {
        text: "One who is not disturbed in mind even amidst the threefold miseries or elated when there is happiness, and who is free from attachment, fear and anger, is called a sage of steady mind.",
        reference: "Bhagavad Gita 2.56"
    },
    {
        text: "It is better to engage in one's own occupation, even though one may perform it imperfectly, than to accept another's occupation and perform it perfectly.",
        reference: "Bhagavad Gita 3.35"
    },
    {
        text: "One who sees inaction in action, and action in inaction, is intelligent among men.",
        reference: "Bhagavad Gita 4.18"
    },
    {
        text: "A person is said to be elevated in yoga when, having renounced all material desires, he neither acts for sense gratification nor engages in fruitive activities.",
        reference: "Bhagavad Gita 6.4"
    },
    {
        text: "For one who has conquered the mind, the mind is the best of friends; but for one who has failed to do so, his mind will remain the greatest enemy.",
        reference: "Bhagavad Gita 6.6"
    },
    {
        text: "The humble sages, by virtue of true knowledge, see with equal vision a learned and gentle brahmana, a cow, an elephant, a dog and a dog-eater.",
        reference: "Bhagavad Gita 5.18"
    },
    {
        text: "When meditation is mastered, the mind is unwavering like the flame of a lamp in a windless place.",
        reference: "Bhagavad Gita 6.19"
    },
    {
        text: "One who is equal to friends and enemies, who is equipoised in honor and dishonor, heat and cold, happiness and distress, fame and infamy, is very dear to Me.",
        reference: "Bhagavad Gita 12.18"
    },
    {
        text: "Abandon all varieties of religion and just surrender unto Me. I shall deliver you from all sinful reactions. Do not fear.",
        reference: "Bhagavad Gita 18.66"
    },
    {
        text: "The mind is restless, turbulent, obstinate and very strong. To subdue it is more difficult than controlling the wind.",
        reference: "Bhagavad Gita 6.34"
    },
    {
        text: "Whatever action a great man performs, common men follow. And whatever standards he sets by exemplary acts, all the world pursues.",
        reference: "Bhagavad Gita 3.21"
    },
    {
        text: "From anger comes delusion; from delusion, loss of memory; from loss of memory, destruction of discrimination; from destruction of discrimination, one perishes.",
        reference: "Bhagavad Gita 2.63"
    },
    {
        text: "One who is not envious but is a kind friend to all living entities, who does not think himself a proprietor and is free from false ego, who is equal in both happiness and distress, is very dear to Me.",
        reference: "Bhagavad Gita 12.13"
    }
];

function initQuoteOfDay() {
    const quoteText = document.getElementById('quoteText');
    const quoteReference = document.getElementById('quoteReference');
    const refreshBtn = document.getElementById('refreshQuote');
    
    if (!quoteText || !quoteReference) return;
    
    function displayRandomQuote() {
        const randomIndex = Math.floor(Math.random() * bhagavadGitaQuotes.length);
        const quote = bhagavadGitaQuotes[randomIndex];
        
        // Fade out
        quoteText.style.opacity = '0';
        quoteReference.style.opacity = '0';
        
        setTimeout(() => {
            quoteText.textContent = quote.text;
            quoteReference.textContent = quote.reference;
            
            // Fade in
            quoteText.style.opacity = '1';
            quoteReference.style.opacity = '1';
        }, 300);
    }
    
    // Display initial quote
    displayRandomQuote();
    
    // Refresh button
    if (refreshBtn) {
        refreshBtn.addEventListener('click', displayRandomQuote);
    }
}

// ========================================
// TESTIMONIALS CAROUSEL
// ========================================
function initTestimonialsCarousel() {
    const container = document.getElementById('testimonialsContainer');
    const prevBtn = document.getElementById('prevTestimonial');
    const nextBtn = document.getElementById('nextTestimonial');
    const dotsContainer = document.getElementById('carouselDots');
    
    if (!container || !prevBtn || !nextBtn) return;
    
    const cards = container.querySelectorAll('.testimonial-card');
    let currentIndex = 0;
    
    // Create dots
    cards.forEach((_, index) => {
        const dot = document.createElement('span');
        dot.className = 'carousel-dot';
        if (index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => goToSlide(index));
        dotsContainer.appendChild(dot);
    });
    
    const dots = dotsContainer.querySelectorAll('.carousel-dot');
    
    function updateCarousel() {
        cards.forEach((card, index) => {
            card.classList.remove('active');
            if (index === currentIndex) {
                card.classList.add('active');
            }
        });
        
        dots.forEach((dot, index) => {
            dot.classList.remove('active');
            if (index === currentIndex) {
                dot.classList.add('active');
            }
        });
    }
    
    function goToSlide(index) {
        currentIndex = index;
        updateCarousel();
    }
    
    function nextSlide() {
        currentIndex = (currentIndex + 1) % cards.length;
        updateCarousel();
    }
    
    function prevSlide() {
        currentIndex = (currentIndex - 1 + cards.length) % cards.length;
        updateCarousel();
    }
    
    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);
    
    // Auto-advance every 5 seconds
    setInterval(nextSlide, 5000);
}

// ========================================
// BREATHING EXERCISE
// ========================================
function initBreathingExercise() {
    const breathingCircle = document.getElementById('breathingCircle');
    const breathingText = document.getElementById('breathingText');
    const breathingToggle = document.getElementById('breathingToggle');
    
    if (!breathingCircle || !breathingText || !breathingToggle) return;
    
    let isActive = false;
    let breathingInterval;
    
    const breathingCycle = [
        { text: 'Breathe In', duration: 4000, phase: 'inhale' },
        { text: 'Hold', duration: 4000, phase: 'hold' },
        { text: 'Breathe Out', duration: 4000, phase: 'exhale' },
        { text: 'Hold', duration: 4000, phase: 'hold' }
    ];
    
    let currentPhase = 0;
    
    function startBreathing() {
        isActive = true;
        breathingToggle.textContent = 'Stop Exercise';
        breathingCircle.classList.add('active');
        
        function runCycle() {
            const phase = breathingCycle[currentPhase];
            breathingText.textContent = phase.text;
            breathingCircle.className = 'breathing-circle-animated active ' + phase.phase;
            
            breathingInterval = setTimeout(() => {
                currentPhase = (currentPhase + 1) % breathingCycle.length;
                if (isActive) {
                    runCycle();
                }
            }, phase.duration);
        }
        
        runCycle();
    }
    
    function stopBreathing() {
        isActive = false;
        breathingToggle.textContent = 'Start Exercise';
        breathingCircle.classList.remove('active', 'inhale', 'exhale', 'hold');
        breathingText.textContent = 'Breathe In';
        currentPhase = 0;
        clearTimeout(breathingInterval);
    }
    
    breathingToggle.addEventListener('click', () => {
        if (isActive) {
            stopBreathing();
        } else {
            startBreathing();
        }
    });
}

// ========================================
// INITIALIZE ALL FEATURES
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    initPageTransitions();
    initDarkMode();
    initParallax();
    initQuoteOfDay();
    initTestimonialsCarousel();
    initBreathingExercise();
});
