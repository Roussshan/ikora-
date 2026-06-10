// Mood Tracker JavaScript

let selectedMood = null;
let currentDate = new Date();

// Mood selection
const moodBtns = document.querySelectorAll('.mood-btn');
const saveMoodBtn = document.getElementById('saveMoodBtn');
const moodNoteInput = document.getElementById('moodNote');

moodBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        // Remove active class from all buttons
        moodBtns.forEach(b => b.classList.remove('active'));
        
        // Add active class to clicked button
        this.classList.add('active');
        selectedMood = this.getAttribute('data-mood');
    });
});

// Save mood
if (saveMoodBtn) {
    saveMoodBtn.addEventListener('click', saveMood);
}

function saveMood() {
    if (!selectedMood) {
        alert('Please select a mood first!');
        return;
    }
    
    const today = new Date().toISOString().split('T')[0];
    const note = moodNoteInput.value;
    
    // Get user token
    const token = localStorage.getItem('ikora_token');
    
    if (token && !token.startsWith('offline_')) {
        // Save to MongoDB via backend
        fetch('http://localhost:3000/api/mood/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                mood: selectedMood,
                note: note,
                date: new Date()
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Also save to localStorage as backup
            let moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
            moods[today] = {
                mood: selectedMood,
                note: note,
                timestamp: new Date().toISOString()
            };
            localStorage.setItem('mood_data', JSON.stringify(moods));
            
            // Reset form and update UI
            resetMoodForm();
            showNotification('Mood saved to database! 🎉');
        })
        .catch(error => {
            console.error('Error saving mood:', error);
            // Fallback to localStorage
            saveToLocalStorage();
        });
    } else {
        // Offline mode - save to localStorage only
        saveToLocalStorage();
    }
    
    function saveToLocalStorage() {
        let moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
        moods[today] = {
            mood: selectedMood,
            note: note,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('mood_data', JSON.stringify(moods));
        resetMoodForm();
        showNotification('Mood saved locally! 🎉');
    }
    
    function resetMoodForm() {
        moodBtns.forEach(b => b.classList.remove('active'));
        moodNoteInput.value = '';
        selectedMood = null;
        updateStats();
        renderCalendar();
        renderHistory();
        updateInsights();
    }
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, var(--soft-purple), var(--soft-pink));
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Update statistics
function updateStats() {
    const moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
    const moodEntries = Object.entries(moods);
    
    // Total entries
    document.getElementById('totalEntries').textContent = moodEntries.length;
    
    // Current streak
    const streak = calculateStreak(moods);
    document.getElementById('currentStreak').textContent = `${streak} days`;
    
    // Most common mood
    if (moodEntries.length > 0) {
        const moodCounts = {};
        moodEntries.forEach(([date, data]) => {
            moodCounts[data.mood] = (moodCounts[data.mood] || 0) + 1;
        });
        const mostCommon = Object.keys(moodCounts).reduce((a, b) => 
            moodCounts[a] > moodCounts[b] ? a : b
        );
        document.getElementById('commonMood').textContent = getMoodEmoji(mostCommon);
    }
    
    // This week's mood
    const weekMood = getWeekMood(moods);
    document.getElementById('weekMood').textContent = weekMood;
}

function calculateStreak(moods) {
    const dates = Object.keys(moods).sort().reverse();
    let streak = 0;
    const today = new Date();
    
    for (let i = 0; i < dates.length; i++) {
        const checkDate = new Date(today);
        checkDate.setDate(today.getDate() - i);
        const dateStr = checkDate.toISOString().split('T')[0];
        
        if (dates.includes(dateStr)) {
            streak++;
        } else {
            break;
        }
    }
    
    return streak;
}

function getWeekMood(moods) {
    const today = new Date();
    const weekAgo = new Date(today);
    weekAgo.setDate(today.getDate() - 7);
    
    const weekMoods = Object.entries(moods).filter(([date]) => {
        const moodDate = new Date(date);
        return moodDate >= weekAgo && moodDate <= today;
    });
    
    if (weekMoods.length === 0) return '-';
    
    const moodCounts = {};
    weekMoods.forEach(([date, data]) => {
        moodCounts[data.mood] = (moodCounts[data.mood] || 0) + 1;
    });
    
    const mostCommon = Object.keys(moodCounts).reduce((a, b) => 
        moodCounts[a] > moodCounts[b] ? a : b
    );
    
    return getMoodEmoji(mostCommon);
}

function getMoodEmoji(mood) {
    const emojis = {
        'amazing': '😄',
        'good': '😊',
        'okay': '😐',
        'sad': '😔',
        'anxious': '😰'
    };
    return emojis[mood] || '-';
}

// Render calendar
function renderCalendar() {
    const calendar = document.getElementById('moodCalendar');
    const monthDisplay = document.getElementById('currentMonth');
    
    if (!calendar) return;
    
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    // Update month display
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December'];
    monthDisplay.textContent = `${monthNames[month]} ${year}`;
    
    // Get first day of month and number of days
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    // Clear calendar
    calendar.innerHTML = '';
    
    // Add day headers
    const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    dayHeaders.forEach(day => {
        const header = document.createElement('div');
        header.className = 'calendar-day-header';
        header.textContent = day;
        calendar.appendChild(header);
    });
    
    // Add empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day empty';
        calendar.appendChild(emptyDay);
    }
    
    // Get mood data
    const moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
    
    // Add days of month
    for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.className = 'calendar-day';
        
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        
        if (moods[dateStr]) {
            dayCell.classList.add('has-mood', moods[dateStr].mood);
            dayCell.title = `${getMoodEmoji(moods[dateStr].mood)} ${moods[dateStr].note || ''}`;
        }
        
        // Highlight today
        const today = new Date();
        if (year === today.getFullYear() && month === today.getMonth() && day === today.getDate()) {
            dayCell.classList.add('today');
        }
        
        dayCell.textContent = day;
        calendar.appendChild(dayCell);
    }
}

// Calendar navigation
document.getElementById('prevMonth')?.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

document.getElementById('nextMonth')?.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

// Render history
function renderHistory() {
    const historyList = document.getElementById('moodHistoryList');
    if (!historyList) return;
    
    const moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
    const entries = Object.entries(moods).sort((a, b) => b[0].localeCompare(a[0])).slice(0, 10);
    
    if (entries.length === 0) {
        historyList.innerHTML = `
            <div class="mood-history-item">
                <div class="history-date">No entries yet</div>
                <p class="history-note">Start tracking your mood to see your history here!</p>
            </div>
        `;
        return;
    }
    
    historyList.innerHTML = entries.map(([date, data]) => {
        const dateObj = new Date(date);
        const formattedDate = dateObj.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        
        return `
            <div class="mood-history-item">
                <div class="history-mood">${getMoodEmoji(data.mood)}</div>
                <div class="history-content">
                    <div class="history-date">${formattedDate}</div>
                    <p class="history-note">${data.note || 'No note added'}</p>
                </div>
            </div>
        `;
    }).join('');
}

// Update insights
function updateInsights() {
    const moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
    const entries = Object.entries(moods);
    
    if (entries.length === 0) return;
    
    // Count positive days
    const positiveMoods = entries.filter(([date, data]) => 
        data.mood === 'amazing' || data.mood === 'good'
    ).length;
    const percentage = Math.round((positiveMoods / entries.length) * 100);
    document.getElementById('positiveDays').textContent = 
        `${percentage}% of your tracked days were positive!`;
    
    // Find best day
    const amazingDays = entries.filter(([date, data]) => data.mood === 'amazing');
    if (amazingDays.length > 0) {
        const lastAmazing = amazingDays[amazingDays.length - 1][0];
        const date = new Date(lastAmazing).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        document.getElementById('bestDay').textContent = `Your last amazing day was ${date}!`;
    }
    
    // Recommendation
    const recentMoods = entries.slice(-7);
    const recentNegative = recentMoods.filter(([date, data]) => 
        data.mood === 'sad' || data.mood === 'anxious'
    ).length;
    
    if (recentNegative > 3) {
        document.getElementById('recommendation').textContent = 
            'Consider trying our breathing exercises or chatting with Ikora for support.';
    } else if (percentage > 70) {
        document.getElementById('recommendation').textContent = 
            'You\'re doing great! Keep up the positive momentum!';
    } else {
        document.getElementById('recommendation').textContent = 
            'Try daily meditation and explore the Gita Library for wisdom.';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateStats();
    renderCalendar();
    renderHistory();
    updateInsights();
});


// ========================================
// COMPACT MOOD TRACKER FOR DASHBOARD
// ========================================

// Check if we're on the dashboard page (compact version)
const isCompactMode = document.getElementById('saveMoodBtnCompact') !== null;

if (isCompactMode) {
    let selectedMoodCompact = null;
    let currentDateCompact = new Date();

    // Mood selection for compact version
    const moodBtnsCompact = document.querySelectorAll('.mood-btn-compact');
    const saveMoodBtnCompact = document.getElementById('saveMoodBtnCompact');
    const moodNoteInputCompact = document.getElementById('moodNoteCompact');

    moodBtnsCompact.forEach(btn => {
        btn.addEventListener('click', function() {
            moodBtnsCompact.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            selectedMoodCompact = this.getAttribute('data-mood');
        });
    });

    // Save mood for compact version
    if (saveMoodBtnCompact) {
        saveMoodBtnCompact.addEventListener('click', saveMoodCompact);
    }

    function saveMoodCompact() {
        if (!selectedMoodCompact) {
            alert('Please select a mood first!');
            return;
        }
        
        const today = new Date().toISOString().split('T')[0];
        const note = moodNoteInputCompact.value;
        
        // Get user token
        const token = localStorage.getItem('ikora_token');
        
        if (token && !token.startsWith('offline_')) {
            // Save to MongoDB via backend
            fetch('http://localhost:3000/api/mood/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    mood: selectedMoodCompact,
                    note: note,
                    date: new Date()
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Also save to localStorage as backup
                let moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
                moods[today] = {
                    mood: selectedMoodCompact,
                    note: note,
                    timestamp: new Date().toISOString()
                };
                localStorage.setItem('mood_data', JSON.stringify(moods));
                
                // Reset form and update UI
                resetMoodFormCompact();
                showNotificationCompact('Mood saved to database! 🎉');
            })
            .catch(error => {
                console.error('Error saving mood:', error);
                // Fallback to localStorage
                saveToLocalStorageCompact();
            });
        } else {
            // Offline mode - save to localStorage only
            saveToLocalStorageCompact();
        }
        
        function saveToLocalStorageCompact() {
            let moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
            moods[today] = {
                mood: selectedMoodCompact,
                note: note,
                timestamp: new Date().toISOString()
            };
            localStorage.setItem('mood_data', JSON.stringify(moods));
            resetMoodFormCompact();
            showNotificationCompact('Mood saved locally! 🎉');
        }
        
        function resetMoodFormCompact() {
            moodBtnsCompact.forEach(b => b.classList.remove('active'));
            moodNoteInputCompact.value = '';
            selectedMoodCompact = null;
            updateStatsCompact();
            renderCalendarCompact();
            renderHistoryCompact();
        }
    }

    function showNotificationCompact(message) {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-pink));
            color: white;
            padding: 1rem 2rem;
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Update statistics for compact version
    function updateStatsCompact() {
        const moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
        const moodEntries = Object.entries(moods);
        
        // Current streak
        const streak = calculateStreak(moods);
        document.getElementById('streakCompact').textContent = `${streak} days`;
        
        // Total entries
        document.getElementById('totalCompact').textContent = moodEntries.length;
        
        // This week's mood
        const weekMood = getWeekMood(moods);
        document.getElementById('weekMoodCompact').textContent = weekMood;
    }

    // Render calendar for compact version
    function renderCalendarCompact() {
        const calendar = document.getElementById('calendarGridCompact');
        const monthDisplay = document.getElementById('currentMonthCompact');
        
        if (!calendar) return;
        
        const year = currentDateCompact.getFullYear();
        const month = currentDateCompact.getMonth();
        
        const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        monthDisplay.textContent = `${monthNames[month]} ${year}`;
        
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        calendar.innerHTML = '';
        
        // Add day headers
        const dayHeaders = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
        dayHeaders.forEach(day => {
            const header = document.createElement('div');
            header.style.cssText = `
                text-align: center;
                color: rgba(255, 255, 255, 0.7);
                font-weight: 600;
                font-size: 0.7rem;
                padding: 0.3rem;
            `;
            header.textContent = day;
            calendar.appendChild(header);
        });
        
        // Add empty cells
        for (let i = 0; i < firstDay; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day-compact empty';
            calendar.appendChild(emptyDay);
        }
        
        const moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
        
        // Add days
        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement('div');
            dayCell.className = 'calendar-day-compact';
            
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            
            if (moods[dateStr]) {
                dayCell.classList.add('has-mood', moods[dateStr].mood);
                dayCell.title = `${getMoodEmoji(moods[dateStr].mood)} ${moods[dateStr].note || ''}`;
            }
            
            const today = new Date();
            if (year === today.getFullYear() && month === today.getMonth() && day === today.getDate()) {
                dayCell.classList.add('today');
            }
            
            dayCell.textContent = day;
            calendar.appendChild(dayCell);
        }
    }

    // Calendar navigation for compact version
    document.getElementById('prevMonthCompact')?.addEventListener('click', () => {
        currentDateCompact.setMonth(currentDateCompact.getMonth() - 1);
        renderCalendarCompact();
    });

    document.getElementById('nextMonthCompact')?.addEventListener('click', () => {
        currentDateCompact.setMonth(currentDateCompact.getMonth() + 1);
        renderCalendarCompact();
    });

    // Render history for compact version
    function renderHistoryCompact() {
        const historyList = document.getElementById('historyListCompact');
        if (!historyList) return;
        
        const moods = JSON.parse(localStorage.getItem('mood_data') || '{}');
        const entries = Object.entries(moods).sort((a, b) => b[0].localeCompare(a[0])).slice(0, 5);
        
        if (entries.length === 0) {
            historyList.innerHTML = '<p class="no-entries">No entries yet. Start tracking!</p>';
            return;
        }
        
        historyList.innerHTML = entries.map(([date, data]) => {
            const dateObj = new Date(date);
            const formattedDate = dateObj.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric'
            });
            
            return `
                <div class="history-item-compact">
                    <div class="history-mood-compact">${getMoodEmoji(data.mood)}</div>
                    <div class="history-content-compact">
                        <div class="history-date-compact">${formattedDate}</div>
                        <p class="history-note-compact">${data.note || 'No note'}</p>
                    </div>
                </div>
            `;
        }).join('');
    }

    // Initialize compact version
    updateStatsCompact();
    renderCalendarCompact();
    renderHistoryCompact();
}
