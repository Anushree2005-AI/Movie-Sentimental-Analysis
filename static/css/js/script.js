document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const reviewInput = document.getElementById('reviewInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const charCount = document.getElementById('charCount');
    const resultSection = document.getElementById('resultSection');
    const form = document.querySelector('form');
    
    // Initialize the application
    initApp();
    
    function initApp() {
        setupEventListeners();
        updateSubmitButton();
        console.log('🎬 Movie Sentiment Analyzer initialized');
    }
    
    function setupEventListeners() {
        // Character count and auto-resize
        if (reviewInput && charCount) {
            reviewInput.addEventListener('input', function() {
                updateCharacterCount();
                autoResizeTextarea();
                updateSubmitButton();
            });
            
            // Initial count
            updateCharacterCount();
        }
        
        // Form submission handling
        if (form) {
            form.addEventListener('submit', function(e) {
                handleFormSubmission(e);
            });
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            handleKeyboardShortcuts(e);
        });
    }
    
    function updateCharacterCount() {
        if (reviewInput && charCount) {
            const count = reviewInput.value.length;
            charCount.textContent = `${count} characters`;
            
            // Visual feedback for length
            if (count > 500) {
                charCount.style.color = 'var(--positive)';
            } else if (count > 100) {
                charCount.style.color = 'var(--neutral)';
            } else {
                charCount.style.color = 'var(--light)';
            }
        }
    }
    
    function autoResizeTextarea() {
        if (reviewInput) {
            reviewInput.style.height = 'auto';
            reviewInput.style.height = Math.min(reviewInput.scrollHeight, 300) + 'px';
        }
    }
    
    function updateSubmitButton() {
        if (analyzeBtn && reviewInput) {
            const hasText = reviewInput.value.trim().length > 0;
            analyzeBtn.disabled = !hasText;
            
            if (hasText) {
                analyzeBtn.style.opacity = '1';
            } else {
                analyzeBtn.style.opacity = '0.7';
            }
        }
    }
    
    function handleFormSubmission(e) {
        const text = reviewInput.value.trim();
        
        if (!text) {
            e.preventDefault();
            showNotification('Please enter a movie review to analyze.', 'error');
            reviewInput.focus();
            return;
        }
        
        if (text.length < 10) {
            e.preventDefault();
            showNotification('Please enter a longer review for better analysis.', 'warning');
            return;
        }
        
        // Show loading state
        setLoadingState(true);
        
        // Add loading animation to results
        if (resultSection) {
            resultSection.classList.add('loading-state');
        }
    }
    
    function handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + Enter to submit
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (reviewInput && reviewInput === document.activeElement) {
                e.preventDefault();
                analyzeBtn.click();
            }
        }
        
        // Escape to clear input
        if (e.key === 'Escape') {
            if (reviewInput && reviewInput === document.activeElement) {
                reviewInput.value = '';
                updateCharacterCount();
                updateSubmitButton();
                autoResizeTextarea();
                showNotification('Input cleared', 'info');
            }
        }
    }
    
    function setLoadingState(loading) {
        if (analyzeBtn) {
            if (loading) {
                analyzeBtn.classList.add('loading');
                analyzeBtn.innerHTML = '<i class="fas fa-spinner"></i> Analyzing...';
                analyzeBtn.disabled = true;
            } else {
                analyzeBtn.classList.remove('loading');
                analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Review';
                updateSubmitButton();
                
                // Remove loading state from results
                if (resultSection) {
                    resultSection.classList.remove('loading-state');
                }
            }
        }
    }
    
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        removeExistingNotifications();
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        `;
        
        // Add to document
        document.body.appendChild(notification);
        
        // Add close functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            removeNotification(notification);
        });
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            removeNotification(notification);
        }, 5000);
        
        // Add styles if not already added
        addNotificationStyles();
    }
    
    function removeExistingNotifications() {
        const notifications = document.querySelectorAll('.notification');
        notifications.forEach(notification => {
            removeNotification(notification);
        });
    }
    
    function removeNotification(notification) {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
    
    function addNotificationStyles() {
        if (!document.getElementById('notification-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-styles';
            style.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: var(--primary);
                    color: white;
                    padding: 15px 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    z-index: 1000;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    animation: slideInRight 0.3s ease;
                    max-width: 400px;
                }
                .notification.error {
                    background: var(--negative);
                }
                .notification.info {
                    background: var(--primary);
                }
                .notification.warning {
                    background: var(--neutral);
                }
                .notification-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 18px;
                    cursor: pointer;
                    padding: 0;
                    width: 20px;
                    height: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOutRight {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    // Utility function to scroll to results
    function scrollToResults() {
        if (resultSection) {
            resultSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }
    }
    
    // Add some example reviews on click (optional feature)
    function addExampleReviews() {
        const examples = [
            "The cinematography was absolutely stunning and the acting was superb, but the plot felt somewhat predictable.",
            "A masterpiece of storytelling with brilliant performances that kept me engaged from start to finish.",
            "Disappointing and boring. The characters were poorly developed and the story made no sense.",
            "The visual effects were amazing, but the weak script and terrible acting ruined the experience."
        ];
        
        // You can add buttons for these examples in your HTML later
    }
    
    // Initialize example reviews
    addExampleReviews();
});
