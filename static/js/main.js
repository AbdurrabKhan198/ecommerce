// Women's Wear E-commerce - Beautiful Interactive JavaScript
// Prevent multiple initializations
if (window.womensWearAppInitialized) {
    console.log('App already initialized, skipping...');
} else {
    window.womensWearAppInitialized = true;
    
    document.addEventListener('DOMContentLoaded', function() {
        initializeApp();
    });
}

function initializeApp() {
    // Prevent multiple initializations
    if (window.appInitialized) return;
    window.appInitialized = true;
    
    initializeScrollAnimations();
    initializeNavbarEffects();
    initializeProductInteractions();
    initializeCartFeatures();
    initializeWishlistFeatures();
    initializeScrollToTop();
    initializeNotifications();
    console.log('🛍️ Beautiful design loaded!');
}

// Scroll Animations
function initializeScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll, .counter');
    if (elements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                if (entry.target.classList.contains('counter')) {
                    animateCounter(entry.target);
                }
            }
        });
    }, { threshold: 0.1 });
    
    elements.forEach(el => {
        observer.observe(el);
    });
}

function animateCounter(element) {
    if (!element) return;
    
    const target = parseInt(element.dataset.target) || 100;
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };
    
    updateCounter();
}

// Navbar Effects
function initializeNavbarEffects() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    // Remove existing event listeners to prevent duplicates
    if (window.navbarScrollHandler) {
        window.removeEventListener('scroll', window.navbarScrollHandler);
    }
    
    window.navbarScrollHandler = () => {
        if (window.pageYOffset > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };
    
    window.addEventListener('scroll', window.navbarScrollHandler);
}

// Product Interactions
function initializeProductInteractions() {
    const productCards = document.querySelectorAll('.product-card');
    if (productCards.length === 0) return;
    
    productCards.forEach(card => {
        // Remove existing listeners to prevent duplicates
        card.removeEventListener('mouseenter', card._mouseEnterHandler);
        card.removeEventListener('mouseleave', card._mouseLeaveHandler);
        
        card._mouseEnterHandler = () => {
            card.style.transform = 'translateY(-8px) scale(1.02)';
        };
        
        card._mouseLeaveHandler = () => {
            card.style.transform = 'translateY(0) scale(1)';
        };
        
        card.addEventListener('mouseenter', card._mouseEnterHandler);
        card.addEventListener('mouseleave', card._mouseLeaveHandler);
    });
}

// Cart Features
function initializeCartFeatures() {
    const cartButtons = document.querySelectorAll('.add-to-cart-btn');
    if (cartButtons.length === 0) return;
    
    cartButtons.forEach(btn => {
        // Remove existing listeners to prevent duplicates
        btn.removeEventListener('click', btn._clickHandler);
        
        btn._clickHandler = async (e) => {
            e.preventDefault();
            const productId = btn.dataset.productId;
            if (!productId) return;
            
            // Check if user is authenticated
            const isAuthenticated = document.body.classList.contains('authenticated') || 
                                   document.querySelector('meta[name="user-authenticated"]');
            
            if (!isAuthenticated) {
                showNotification('Please login to add items to cart', 'warning');
                return;
            }
            
            try {
                // Show loading state
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Adding...';
                btn.disabled = true;
                
                const response = await fetch('/cart/ajax/add/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ 
                        product_id: productId,
                        quantity: 1
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    btn.innerHTML = '<i class="fas fa-check me-2"></i>Added!';
                    btn.classList.add('btn-success');
                    updateCartCounter();
                    showNotification(data.message, 'success');
                    
                    setTimeout(() => {
                        btn.innerHTML = originalText;
                        btn.classList.remove('btn-success');
                        btn.disabled = false;
                    }, 2000);
                } else {
                    showNotification(data.error || 'Failed to add to cart', 'error');
                    btn.innerHTML = originalText;
                    btn.disabled = false;
                }
            } catch (error) {
                console.error('Cart error:', error);
                showNotification('Network error. Please try again.', 'error');
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        };
        
        btn.addEventListener('click', btn._clickHandler);
    });
}

// Wishlist Features
function initializeWishlistFeatures() {
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    if (wishlistButtons.length === 0) return;
    
    wishlistButtons.forEach(btn => {
        // Remove existing listeners to prevent duplicates
        btn.removeEventListener('click', btn._wishlistClickHandler);
        
        btn._wishlistClickHandler = async (e) => {
            e.preventDefault();
            const productId = btn.dataset.productId;
            if (!productId) return;
            
            const icon = btn.querySelector('i');
            if (!icon) return;
            
            // Check if user is authenticated
            const isAuthenticated = document.body.classList.contains('authenticated') || 
                                   document.querySelector('meta[name="user-authenticated"]');
            
            if (!isAuthenticated) {
                showNotification('Please login to add items to wishlist', 'warning');
                return;
            }
            
            const isActive = btn.classList.contains('active');
            const url = isActive ? '/ajax/remove-from-wishlist/' : '/ajax/add-to-wishlist/';
            
            try {
                // Show loading state
                const originalIcon = icon.className;
                icon.className = 'fas fa-spinner fa-spin';
                btn.disabled = true;
                
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ product_id: productId })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    btn.classList.toggle('active');
                    
                    if (btn.classList.contains('active')) {
                        icon.className = 'fas fa-heart';
                        showNotification(data.message, 'success');
                        updateWishlistCounter(1); // Increment counter
                    } else {
                        icon.className = 'far fa-heart';
                        showNotification(data.message, 'info');
                        updateWishlistCounter(-1); // Decrement counter
                    }
                } else {
                    showNotification(data.error || 'Something went wrong', 'error');
                }
            } catch (error) {
                console.error('Wishlist error:', error);
                showNotification('Network error. Please try again.', 'error');
            } finally {
                btn.disabled = false;
            }
        };
        
        btn.addEventListener('click', btn._wishlistClickHandler);
    });
}

// Scroll to Top
function initializeScrollToTop() {
    let scrollBtn = document.querySelector('.scroll-to-top');
    if (!scrollBtn) {
        scrollBtn = document.createElement('button');
        scrollBtn.className = 'scroll-to-top';
        scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        document.body.appendChild(scrollBtn);
    }
    
    // Remove existing event listeners to prevent duplicates
    if (window.scrollToTopScrollHandler) {
        window.removeEventListener('scroll', window.scrollToTopScrollHandler);
    }
    if (scrollBtn._clickHandler) {
        scrollBtn.removeEventListener('click', scrollBtn._clickHandler);
    }
    
    window.scrollToTopScrollHandler = () => {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    };
    
    scrollBtn._clickHandler = () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };
    
    window.addEventListener('scroll', window.scrollToTopScrollHandler);
    scrollBtn.addEventListener('click', scrollBtn._clickHandler);
}

// Notifications
function initializeNotifications() {
    if (!document.querySelector('.notification-container')) {
        const container = document.createElement('div');
        container.className = 'notification-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
}

// Helper Functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateCartCounter() {
    const counter = document.querySelector('.cart-badge');
    if (!counter) return;
    
    const current = parseInt(counter.textContent) || 0;
    counter.textContent = current + 1;
    counter.style.transform = 'scale(1.3)';
    setTimeout(() => { counter.style.transform = 'scale(1)'; }, 200);
}

function updateWishlistCounter(change) {
    // Find wishlist counter in navbar
    const wishlistCounter = document.querySelector('a[href*="wishlist"] .cart-badge');
    if (!wishlistCounter) return;
    
    const current = parseInt(wishlistCounter.textContent) || 0;
    const newCount = Math.max(0, current + change);
    wishlistCounter.textContent = newCount;
    
    if (change > 0) {
        wishlistCounter.style.transform = 'scale(1.3)';
        setTimeout(() => { wishlistCounter.style.transform = 'scale(1)'; }, 200);
    }
}

function showNotification(message, type = 'info') {
    const container = document.querySelector('.notification-container');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `toast show bg-${type === 'error' ? 'danger' : type} text-white`;
    notification.innerHTML = `
        <div class="toast-body d-flex align-items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close btn-close-white ms-auto" onclick="this.closest('.toast').remove()"></button>
        </div>
    `;
    
    container.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }
    }, 3000);
}

// WhatsApp subscription - with duplicate prevention
if (!window.whatsappHandlerAdded) {
    window.whatsappHandlerAdded = true;
    document.addEventListener('submit', (e) => {
        if (e.target.id === 'whatsappForm' || e.target.id === 'whatsappFooterForm') {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const submitButton = e.target.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            // Show loading state
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            submitButton.disabled = true;
            
            fetch(e.target.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Success! ' + data.message, 'success');
                    e.target.reset();
                } else {
                    showNotification('Error: ' + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Something went wrong. Please try again.', 'error');
            })
            .finally(() => {
                // Reset button state
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            });
        }
    });
}

// Smooth scrolling for anchor links - with duplicate prevention
if (!window.smoothScrollHandlerAdded) {
    window.smoothScrollHandlerAdded = true;
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// Dynamic styles - with duplicate prevention
if (!window.dynamicStylesAdded) {
    window.dynamicStylesAdded = true;
    const styles = document.createElement('style');
    styles.textContent = `
.wishlist-btn.active { color: #e91e63 !important; }
.notification-container .toast { margin-bottom: 0.5rem; transition: all 0.3s ease; }
`;
    document.head.appendChild(styles);
}