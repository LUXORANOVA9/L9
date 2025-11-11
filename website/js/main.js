/**
 * LUXORANOVA Website - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    initSmoothScrolling();
    
    // Navbar scroll effect
    initNavbarScroll();
    
    // Contact form handling
    initContactForm();
    
    // Intersection Observer for animations
    initScrollAnimations();
});

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Don't prevent default for href="#"
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Add scroll effect to navbar
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.8)';
            navbar.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
}

/**
 * Handle contact form submission
 */
function initContactForm() {
    const form = document.getElementById('contactForm');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Get the submit button
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            // Disable button and show loading state
            submitButton.disabled = true;
            submitButton.textContent = 'Sending...';
            
            try {
                // Simulate API call (replace with actual endpoint)
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                // Log form data (in production, send to API)
                console.log('Form submitted:', data);
                
                // Show success message
                showFormMessage('success', 'Thank you! We\'ll get back to you soon.');
                form.reset();
                
            } catch (error) {
                console.error('Form submission error:', error);
                showFormMessage('error', 'Something went wrong. Please try again.');
            } finally {
                // Re-enable button
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }
        });
    }
}

/**
 * Show form submission message
 */
function showFormMessage(type, message) {
    const form = document.getElementById('contactForm');
    
    // Remove any existing messages
    const existingMessage = form.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create and show new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `form-message form-message-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        padding: 1rem;
        margin-top: 1rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 500;
        background: ${type === 'success' ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)'};
        color: ${type === 'success' ? '#22c55e' : '#ef4444'};
        border: 1px solid ${type === 'success' ? 'rgba(34, 197, 94, 0.3)' : 'rgba(239, 68, 68, 0.3)'};
    `;
    
    form.appendChild(messageDiv);
    
    // Remove message after 5 seconds
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        messageDiv.style.transition = 'opacity 0.3s ease';
        setTimeout(() => messageDiv.remove(), 300);
    }, 5000);
}

/**
 * Initialize scroll-triggered animations
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe feature cards
    document.querySelectorAll('.feature-card, .platform-item, .stat-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

/**
 * Initialize particles background effect (optional)
 */
function initParticles() {
    // This can be expanded with a particle library like particles.js
    // For now, it's a placeholder for future enhancement
    console.log('Particles initialized');
}

/**
 * Handle mobile menu toggle (if mobile menu is added later)
 */
function initMobileMenu() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
}

/**
 * Lazy load images
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

/**
 * Add typing effect to hero title (optional enhancement)
 */
function initTypingEffect() {
    const heroTitle = document.querySelector('.hero-title');
    if (!heroTitle) return;
    
    const text = heroTitle.textContent;
    heroTitle.textContent = '';
    heroTitle.style.opacity = '1';
    
    let i = 0;
    const typingInterval = setInterval(() => {
        if (i < text.length) {
            heroTitle.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(typingInterval);
        }
    }, 50);
}

// Export functions for potential use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initSmoothScrolling,
        initNavbarScroll,
        initContactForm,
        initScrollAnimations
    };
}
