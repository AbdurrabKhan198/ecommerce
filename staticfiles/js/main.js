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
        
        btn._clickHandler = (e) => {
            e.preventDefault();
            btn.innerHTML = '<i class="fas fa-check me-2"></i>Added!';
            btn.classList.add('btn-success');
            updateCartCounter();
            showNotification('Product added to cart!', 'success');
            
            setTimeout(() => {
                btn.innerHTML = '<i class="fas fa-shopping-cart me-2"></i>Add to Cart';
                btn.classList.remove('btn-success');
            }, 2000);
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
        
        btn._wishlistClickHandler = (e) => {
            e.preventDefault();
            const icon = btn.querySelector('i');
            if (!icon) return;
            
            btn.classList.toggle('active');
            
            if (btn.classList.contains('active')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                showNotification('Added to wishlist!', 'success');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                showNotification('Removed from wishlist', 'info');
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
function updateCartCounter() {
    const counter = document.querySelector('.cart-badge');
    if (!counter) return;
    
    const current = parseInt(counter.textContent) || 0;
    counter.textContent = current + 1;
    counter.style.transform = 'scale(1.3)';
    setTimeout(() => { counter.style.transform = 'scale(1)'; }, 200);
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

// Newsletter subscription - with duplicate prevention
if (!window.newsletterHandlerAdded) {
    window.newsletterHandlerAdded = true;
    document.addEventListener('submit', (e) => {
        if (e.target.classList.contains('newsletter-form')) {
            e.preventDefault();
            const emailInput = e.target.querySelector('input[type="email"]');
            if (emailInput && emailInput.value) {
                showNotification('Thank you for subscribing! Check your email for a discount.', 'success');
                e.target.reset();
            }
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