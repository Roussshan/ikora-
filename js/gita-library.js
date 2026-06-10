// Gita Library JavaScript

// Sample verses data (in production, load from database/API)
const gitaVerses = [
    // Add more verses here as needed
];

// Search functionality
const searchInput = document.getElementById('verseSearch');
const searchBtn = document.getElementById('searchBtn');
const chapterFilter = document.getElementById('chapterFilter');
const versesContainer = document.getElementById('versesContainer');

if (searchBtn) {
    searchBtn.addEventListener('click', performSearch);
}

if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

if (chapterFilter) {
    chapterFilter.addEventListener('change', filterByChapter);
}

function performSearch() {
    const searchTerm = searchInput.value.toLowerCase();
    const verseCards = document.querySelectorAll('.verse-card');
    
    verseCards.forEach(card => {
        const translation = card.querySelector('.verse-translation').textContent.toLowerCase();
        const tags = Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent.toLowerCase()).join(' ');
        
        if (translation.includes(searchTerm) || tags.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function filterByChapter() {
    const selectedChapter = chapterFilter.value;
    const verseCards = document.querySelectorAll('.verse-card');
    
    verseCards.forEach(card => {
        const cardChapter = card.getAttribute('data-chapter');
        
        if (selectedChapter === 'all' || cardChapter === selectedChapter) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Bookmark functionality
const bookmarkBtns = document.querySelectorAll('.bookmark-btn');

bookmarkBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        const verseCard = this.closest('.verse-card');
        const verseNumber = verseCard.querySelector('.verse-number').textContent;
        
        // Toggle bookmark
        if (this.classList.contains('bookmarked')) {
            this.classList.remove('bookmarked');
            this.textContent = '⭐';
            removeBookmark(verseNumber);
        } else {
            this.classList.add('bookmarked');
            this.textContent = '⭐';
            addBookmark(verseNumber);
        }
    });
});

function addBookmark(verseNumber) {
    let bookmarks = JSON.parse(localStorage.getItem('gita_bookmarks') || '[]');
    if (!bookmarks.includes(verseNumber)) {
        bookmarks.push(verseNumber);
        localStorage.setItem('gita_bookmarks', JSON.stringify(bookmarks));
    }
}

function removeBookmark(verseNumber) {
    let bookmarks = JSON.parse(localStorage.getItem('gita_bookmarks') || '[]');
    bookmarks = bookmarks.filter(b => b !== verseNumber);
    localStorage.setItem('gita_bookmarks', JSON.stringify(bookmarks));
}

// Load bookmarks on page load
function loadBookmarks() {
    const bookmarks = JSON.parse(localStorage.getItem('gita_bookmarks') || '[]');
    const verseCards = document.querySelectorAll('.verse-card');
    
    verseCards.forEach(card => {
        const verseNumber = card.querySelector('.verse-number').textContent;
        const bookmarkBtn = card.querySelector('.bookmark-btn');
        
        if (bookmarks.includes(verseNumber)) {
            bookmarkBtn.classList.add('bookmarked');
            bookmarkBtn.textContent = '⭐';
        }
    });
}

// Load more verses
const loadMoreBtn = document.getElementById('loadMoreBtn');
if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', () => {
        // In production, load more verses from API
        alert('More verses will be loaded from the database in the full version!');
    });
}

// Initialize
loadBookmarks();
