// Billing System JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize billing system
    initializeBillingSystem();
    
    // Auto-hide alerts
    autoHideAlerts();
    
    // Initialize charts if present
    initializeCharts();
    
    // Initialize form calculations
    initializeFormCalculations();
});

function initializeBillingSystem() {
    console.log('Billing System Initialized');
    
    // Add loading states to buttons
    const buttons = document.querySelectorAll('.btn-billing, .btn-billing-outline');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                this.classList.add('loading');
                this.innerHTML = '<span class="spinner"></span> Processing...';
            }
        });
    });
}

function autoHideAlerts() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
}

function initializeCharts() {
    // Initialize revenue chart if present
    const revenueChart = document.getElementById('revenueChart');
    if (revenueChart) {
        const ctx = revenueChart.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Revenue',
                    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#f1f5f9'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
    
    // Initialize status chart if present
    const statusChart = document.getElementById('statusChart');
    if (statusChart) {
        const ctx = statusChart.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Paid', 'Pending', 'Overdue'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: ['#059669', '#d97706', '#dc2626'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

function initializeFormCalculations() {
    // Real-time calculation for invoice forms
    const quantityInputs = document.querySelectorAll('input[name*="quantity"]');
    const priceInputs = document.querySelectorAll('input[name*="price"]');
    const totalInputs = document.querySelectorAll('input[name*="total"]');
    
    function calculateTotal() {
        let grandTotal = 0;
        
        quantityInputs.forEach((quantityInput, index) => {
            const quantity = parseFloat(quantityInput.value) || 0;
            const price = parseFloat(priceInputs[index]?.value) || 0;
            const total = quantity * price;
            
            if (totalInputs[index]) {
                totalInputs[index].value = total.toFixed(2);
            }
            
            grandTotal += total;
        });
        
        // Update grand total
        const grandTotalElement = document.getElementById('grandTotal');
        if (grandTotalElement) {
            grandTotalElement.textContent = '₹' + grandTotal.toFixed(2);
        }
    }
    
    // Add event listeners
    [...quantityInputs, ...priceInputs].forEach(input => {
        input.addEventListener('input', calculateTotal);
    });
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer') || document.body;
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alert);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Export functions for global use
window.billingSystem = {
    formatCurrency,
    showAlert,
    confirmAction
};