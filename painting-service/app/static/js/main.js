document.addEventListener('DOMContentLoaded', function() {
    console.log('Welcome to the Painting Service!');
    
    // Initialize application
    initializeApp();
    
    // Mobile menu toggle
    initializeMobileMenu();
    
    // Auto-hide flash messages
    autoHideFlashMessages();
    
    // Image lazy loading
    lazyLoadImages();
    
    // Form validation
    initializeFormValidation();
    
    // Animate elements on scroll
    initializeScrollAnimations();
});

function initializeApp() {
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add loading state to buttons
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                this.classList.add('loading');
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                
                setTimeout(() => {
                    this.classList.remove('loading');
                    this.innerHTML = originalText;
                }, 2000);
            }
        });
    });
}

function initializeMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = mobileMenuBtn.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
}

function autoHideFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                if (alert.parentElement) {
                    alert.remove();
                }
            }, 300);
        }, 5000);
    });
}

function lazyLoadImages() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('invalid');
                    
                    // Add error message if it doesn't exist
                    let errorMessage = field.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('div');
                        errorMessage.classList.add('error-message');
                        errorMessage.textContent = 'This field is required';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                } else {
                    field.classList.remove('invalid');
                    
                    // Remove error message if it exists
                    const errorMessage = field.nextElementSibling;
                    if (errorMessage && errorMessage.classList.contains('error-message')) {
                        errorMessage.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        // Clear error styling on input
        form.querySelectorAll('input, textarea, select').forEach(field => {
            field.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('invalid');
                    
                    // Remove error message if it exists
                    const errorMessage = this.nextElementSibling;
                    if (errorMessage && errorMessage.classList.contains('error-message')) {
                        errorMessage.remove();
                    }
                }
            });
        });
    });
}

function initializeScrollAnimations() {
    if ('IntersectionObserver' in window) {
        const options = {
            threshold: 0.1
        };
        
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    observer.unobserve(entry.target);
                }
            });
        }, options);
        
        const elements = document.querySelectorAll('.project-card, .section-title, .hero-content');
        elements.forEach(el => {
            observer.observe(el);
        });
    }
}

// Enhanced Flash Message Functions
function closeFlashMessage(button) {
    const message = button.closest('.flash-message');
    if (message) {
        message.style.animation = 'slideOutRight 0.3s ease-out forwards';
        setTimeout(() => {
            if (message.parentNode) {
                message.remove();
                
                // Remove container if no more messages
                const container = document.getElementById('flashContainer');
                if (container && container.children.length === 0) {
                    container.remove();
                }
            }
        }, 300);
    }
}

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach((message, index) => {
        // Stagger the entrance animations
        message.style.animationDelay = `${index * 0.1}s`;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (message.parentNode) {
                closeFlashMessage(message.querySelector('.flash-close'));
            }
        }, 5000 + (index * 100)); // Stagger the auto-hide too
    });
});

// Enhanced notification function for JavaScript use
function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('flashContainer') || createFlashContainer();
    
    const notification = document.createElement('div');
    notification.className = `flash-message flash-${type}`;
    notification.innerHTML = `
        <div class="flash-content">
            <div class="flash-icon">
                <i class="fas fa-${getIconForType(type)}"></i>
            </div>
            <div class="flash-text">
                <strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong>
                <span>${message}</span>
            </div>
        </div>
        <button class="flash-close" onclick="closeFlashMessage(this)" aria-label="Close message">
            <i class="fas fa-times"></i>
        </button>
        <div class="flash-progress"></div>
    `;
    
    container.appendChild(notification);
    
    // Auto-hide
    setTimeout(() => {
        if (notification.parentNode) {
            closeFlashMessage(notification.querySelector('.flash-close'));
        }
    }, duration);
    
    return notification;
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.id = 'flashContainer';
    container.className = 'flash-messages-container';
    container.setAttribute('role', 'alert');
    container.setAttribute('aria-live', 'polite');
    document.body.appendChild(container);
    return container;
}

function getIconForType(type) {
    const icons = {
        success: 'check-circle',
        danger: 'exclamation-triangle',
        error: 'exclamation-triangle',
        info: 'info-circle',
        warning: 'exclamation-circle'
    };
    return icons[type] || 'info-circle';
}

// Utility functions
function showLoader() {
    const loader = document.createElement('div');
    loader.className = 'page-loader';
    loader.innerHTML = '<div class="spinner"><i class="fas fa-paint-roller fa-spin"></i></div>';
    document.body.appendChild(loader);
}

function hideLoader() {
    const loader = document.querySelector('.page-loader');
    if (loader) {
        loader.classList.add('fade-out');
        setTimeout(() => {
            loader.remove();
        }, 300);
    }
}

// Add these additional styles for animations and footer
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        /* Footer Styles */
        .main-footer {
            background: var(--primary-color);
            color: var(--white);
            padding: 4rem 0 2rem;
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .footer-logo h2 {
            font-size: 1.8rem;
            margin-bottom: 1rem;
            color: var(--white);
        }
        
        .footer-logo p {
            color: rgba(255, 255, 255, 0.8);
        }
        
        .footer-links h3,
        .footer-contact h3 {
            color: var(--white);
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }
        
        .footer-links ul {
            list-style: none;
        }
        
        .footer-links ul li {
            margin-bottom: 0.5rem;
        }
        
        .footer-links ul li a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: var(--transition);
        }
        
        .footer-links ul li a:hover {
            color: var(--white);
            padding-left: 5px;
        }
        
        .footer-contact p {
            margin-bottom: 0.5rem;
            color: rgba(255, 255, 255, 0.8);
        }
        
        .footer-contact p i {
            margin-right: 0.5rem;
            color: var(--accent-color);
        }
        
        .footer-bottom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .social-links {
            display: flex;
            gap: 1rem;
        }
        
        .social-link {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            background: rgba(255, 255, 255, 0.1);
            color: var(--white);
            border-radius: 50%;
            transition: var(--transition);
        }
        
        .social-link:hover {
            background: var(--accent-color);
            transform: translateY(-3px);
        }
        
        /* Animations */
        .project-card, .section-title, .hero-content {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .project-card.animated, .section-title.animated, .hero-content.animated {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Loader Styles */
        .page-loader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: opacity 0.3s ease;
        }
        
        .page-loader.fade-out {
            opacity: 0;
        }
        
        .spinner {
            font-size: 3rem;
            color: var(--primary-color);
            animation: spin 2s infinite linear;
        }
        
        .error-message {
            color: var(--danger-color);
            font-size: 0.85rem;
            margin-top: 0.25rem;
        }
        
        .invalid {
            border-color: var(--danger-color) !important;
        }
        
        @keyframes spin {
            0% {
                transform: rotate(0deg);
            }
            100% {
                transform: rotate(360deg);
            }
        }
        
        @media (max-width: 768px) {
            .footer-bottom {
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }
        }
    `;
    document.head.appendChild(style);
});