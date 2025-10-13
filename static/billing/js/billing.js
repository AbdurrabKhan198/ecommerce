/**
 * Billing System Standalone JavaScript
 */

// Global billing system object
window.BillingSystem = {
    // Configuration
    config: {
        currency: '₹',
        dateFormat: 'DD/MM/YYYY',
        apiEndpoints: {
            calculateTotals: '/bill/api/calculate-totals/',
            addInvoiceItem: '/bill/api/add-item/'
        }
    },
    
    // Initialize the billing system
    init: function() {
        this.setupEventListeners();
        this.initializeCharts();
        this.setupFormValidation();
        this.setupAutoSave();
    },
    
    // Setup event listeners
    setupEventListeners: function() {
        // Auto-hide alerts
        this.autoHideAlerts();
        
        // Loading states for buttons
        this.setupButtonLoadingStates();
        
        // Table row click handlers
        this.setupTableRowClicks();
        
        // Form auto-save
        this.setupFormAutoSave();
        
        // Real-time calculations
        this.setupRealTimeCalculations();
    },
    
    // Auto-hide alerts after 5 seconds
    autoHideAlerts: function() {
        setTimeout(function() {
            const alerts = document.querySelectorAll('.billing-alert');
            alerts.forEach(function(alert) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 500);
            });
        }, 5000);
    },
    
    // Setup button loading states
    setupButtonLoadingStates: function() {
        document.querySelectorAll('.btn-billing').forEach(function(btn) {
            btn.addEventListener('click', function() {
                if (this.type === 'submit' || this.href) {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<span class="billing-spinner me-2"></span>Loading...';
                    this.disabled = true;
                    
                    // Re-enable after 3 seconds if still disabled
                    setTimeout(function() {
                        if (btn.disabled) {
                            btn.innerHTML = originalText;
                            btn.disabled = false;
                        }
                    }, 3000);
                }
            });
        });
    },
    
    // Setup table row clicks
    setupTableRowClicks: function() {
        document.querySelectorAll('.billing-table tbody tr').forEach(function(row) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function() {
                const link = this.querySelector('a');
                if (link) {
                    window.location.href = link.href;
                }
            });
        });
    },
    
    // Setup form auto-save
    setupFormAutoSave: function() {
        const forms = document.querySelectorAll('.billing-form');
        forms.forEach(function(form) {
            const formId = form.id || 'billing-form';
            const savedData = localStorage.getItem(`billing-form-${formId}`);
            
            if (savedData) {
                try {
                    const data = JSON.parse(savedData);
                    Object.keys(data).forEach(function(key) {
                        const field = form.querySelector(`[name="${key}"]`);
                        if (field) {
                            field.value = data[key];
                        }
                    });
                } catch (e) {
                    console.warn('Could not restore form data:', e);
                }
            }
            
            // Save form data on input change
            form.addEventListener('input', function() {
                const formData = new FormData(form);
                const data = {};
                for (let [key, value] of formData.entries()) {
                    data[key] = value;
                }
                localStorage.setItem(`billing-form-${formId}`, JSON.stringify(data));
            });
            
            // Clear saved data on successful submit
            form.addEventListener('submit', function() {
                localStorage.removeItem(`billing-form-${formId}`);
            });
        });
    },
    
    // Setup real-time calculations
    setupRealTimeCalculations: function() {
        const calculationFields = document.querySelectorAll('[data-calculate]');
        calculationFields.forEach(function(field) {
            field.addEventListener('input', function() {
                BillingSystem.calculateTotals();
            });
        });
    },
    
    // Calculate totals for invoice
    calculateTotals: function() {
        const items = [];
        const itemRows = document.querySelectorAll('.invoice-item-row');
        
        itemRows.forEach(function(row) {
            const quantity = parseFloat(row.querySelector('[name*="quantity"]')?.value || 0);
            const unitPrice = parseFloat(row.querySelector('[name*="unit_price"]')?.value || 0);
            const discount = parseFloat(row.querySelector('[name*="discount"]')?.value || 0);
            const taxRate = parseFloat(row.querySelector('[name*="tax_rate"]')?.value || 18);
            
            if (quantity > 0 && unitPrice > 0) {
                items.push({
                    quantity: quantity,
                    unit_price: unitPrice,
                    discount_percentage: discount,
                    tax_rate: taxRate
                });
            }
        });
        
        if (items.length > 0) {
            this.ajaxCalculateTotals(items);
        }
    },
    
    // AJAX calculate totals
    ajaxCalculateTotals: function(items) {
        const invoiceDiscount = parseFloat(document.querySelector('[name="discount_percentage"]')?.value || 0);
        
        fetch(this.config.apiEndpoints.calculateTotals, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                items: items,
                invoice_discount_percentage: invoiceDiscount
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.updateTotalsDisplay(data);
            }
        })
        .catch(error => {
            console.error('Calculation error:', error);
        });
    },
    
    // Update totals display
    updateTotalsDisplay: function(data) {
        const subtotalEl = document.querySelector('#subtotal');
        const discountEl = document.querySelector('#discount');
        const taxEl = document.querySelector('#tax');
        const totalEl = document.querySelector('#total');
        
        if (subtotalEl) subtotalEl.textContent = this.formatCurrency(data.subtotal);
        if (discountEl) discountEl.textContent = this.formatCurrency(data.discount);
        if (taxEl) taxEl.textContent = this.formatCurrency(data.tax);
        if (totalEl) totalEl.textContent = this.formatCurrency(data.total);
    },
    
    // Format currency
    formatCurrency: function(amount) {
        return this.config.currency + ' ' + parseFloat(amount).toFixed(2);
    },
    
    // Get CSRF token
    getCSRFToken: function() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    },
    
    // Initialize charts
    initializeCharts: function() {
        // Revenue chart
        const revenueCtx = document.getElementById('revenueChart');
        if (revenueCtx) {
            this.createRevenueChart(revenueCtx);
        }
        
        // Customer chart
        const customerCtx = document.getElementById('customerChart');
        if (customerCtx) {
            this.createCustomerChart(customerCtx);
        }
    },
    
    // Create revenue chart
    createRevenueChart: function(ctx) {
        const data = JSON.parse(ctx.dataset.chartData || '[]');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(item => item.month),
                datasets: [{
                    label: 'Revenue',
                    data: data.map(item => item.revenue),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    },
    
    // Create customer chart
    createCustomerChart: function(ctx) {
        const data = JSON.parse(ctx.dataset.chartData || '[]');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(item => item.status),
                datasets: [{
                    data: data.map(item => item.count),
                    backgroundColor: [
                        '#10b981',
                        '#f59e0b',
                        '#ef4444'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    },
    
    // Setup form validation
    setupFormValidation: function() {
        const forms = document.querySelectorAll('.billing-form');
        forms.forEach(function(form) {
            form.addEventListener('submit', function(e) {
                if (!BillingSystem.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    },
    
    // Validate form
    validateForm: function(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(function(field) {
            if (!field.value.trim()) {
                BillingSystem.showFieldError(field, 'This field is required');
                isValid = false;
            } else {
                BillingSystem.clearFieldError(field);
            }
        });
        
        return isValid;
    },
    
    // Show field error
    showFieldError: function(field, message) {
        this.clearFieldError(field);
        field.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    },
    
    // Clear field error
    clearFieldError: function(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    },
    
    // Setup auto-save
    setupAutoSave: function() {
        setInterval(function() {
            BillingSystem.saveFormData();
        }, 30000); // Auto-save every 30 seconds
    },
    
    // Save form data
    saveFormData: function() {
        const forms = document.querySelectorAll('.billing-form');
        forms.forEach(function(form) {
            const formId = form.id || 'billing-form';
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            localStorage.setItem(`billing-form-${formId}`, JSON.stringify(data));
        });
    },
    
    // Utility functions
    utils: {
        // Format date
        formatDate: function(date) {
            return new Date(date).toLocaleDateString('en-IN');
        },
        
        // Format currency
        formatCurrency: function(amount) {
            return '₹' + parseFloat(amount).toLocaleString('en-IN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        },
        
        // Generate invoice number
        generateInvoiceNumber: function() {
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
            return `INV-${year}${month}${day}-${random}`;
        },
        
        // Copy to clipboard
        copyToClipboard: function(text) {
            navigator.clipboard.writeText(text).then(function() {
                BillingSystem.showNotification('Copied to clipboard!', 'success');
            });
        },
        
        // Show notification
        showNotification: function(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `billing-alert billing-alert-${type}`;
            notification.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : 'info-circle'} me-2"></i>
                ${message}
            `;
            
            document.querySelector('.billing-container').insertBefore(
                notification, 
                document.querySelector('.billing-container').firstChild
            );
            
            setTimeout(function() {
                notification.remove();
            }, 5000);
        }
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    BillingSystem.init();
});

// Export for global access
window.BillingSystem = BillingSystem;
