// Enhanced Billing System JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize billing system
    initializeBillingSystem();
    
    // Auto-hide alerts
    autoHideAlerts();
    
    // Initialize charts if present
    initializeCharts();
    
    // Initialize form calculations
    initializeFormCalculations();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize data tables
    initializeDataTables();
});

function initializeBillingSystem() {
    console.log('Enhanced Billing System Initialized');
    
    // Add loading states to buttons
    const buttons = document.querySelectorAll('.btn-billing, .btn-billing-outline');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                this.classList.add('loading');
                const originalText = this.innerHTML;
                this.innerHTML = '<span class="spinner"></span> Processing...';
                
                // Reset after 3 seconds if no response
                setTimeout(() => {
                    this.classList.remove('loading');
                    this.innerHTML = originalText;
                }, 3000);
            }
        });
    });
    
    // Add hover effects to cards
    const cards = document.querySelectorAll('.billing-card, .stats-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

function autoHideAlerts() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
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
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#6366f1',
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#f3f4f6',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#6b7280',
                            font: {
                                size: 12
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#6b7280',
                            font: {
                                size: 12
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
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
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#6366f1',
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                cutout: '60%'
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
            grandTotalElement.textContent = formatCurrency(grandTotal);
        }
        
        // Update tax calculations
        const taxRate = parseFloat(document.getElementById('taxRate')?.value) || 0;
        const taxAmount = grandTotal * (taxRate / 100);
        const finalTotal = grandTotal + taxAmount;
        
        const taxAmountElement = document.getElementById('taxAmount');
        if (taxAmountElement) {
            taxAmountElement.textContent = formatCurrency(taxAmount);
        }
        
        const finalTotalElement = document.getElementById('finalTotal');
        if (finalTotalElement) {
            finalTotalElement.textContent = formatCurrency(finalTotal);
        }
    }
    
    // Add event listeners
    [...quantityInputs, ...priceInputs].forEach(input => {
        input.addEventListener('input', calculateTotal);
        input.addEventListener('blur', calculateTotal);
    });
    
    // Tax rate change
    const taxRateInput = document.getElementById('taxRate');
    if (taxRateInput) {
        taxRateInput.addEventListener('input', calculateTotal);
    }
}

function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.billing-card, .stats-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add pulse animation to important elements
    const importantElements = document.querySelectorAll('.stats-card .stat-number');
    importantElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.animation = 'pulse 1s ease-in-out';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.animation = 'none';
        });
    });
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeDataTables() {
    // Add sorting functionality to tables
    const tables = document.querySelectorAll('.billing-table');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            if (header.textContent.trim() !== '') {
                header.style.cursor = 'pointer';
                header.style.userSelect = 'none';
                header.addEventListener('click', () => sortTable(table, index));
            }
        });
    });
}

function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const isNumeric = !isNaN(parseFloat(rows[0].cells[columnIndex].textContent));
    
    rows.sort((a, b) => {
        const aVal = a.cells[columnIndex].textContent.trim();
        const bVal = b.cells[columnIndex].textContent.trim();
        
        if (isNumeric) {
            return parseFloat(aVal) - parseFloat(bVal);
        } else {
            return aVal.localeCompare(bVal);
        }
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.getElementById('alertContainer') || document.body;
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        <i class="fas fa-${getAlertIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alert);
    
    // Auto-hide after duration
    setTimeout(() => {
        alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            alert.remove();
        }, 500);
    }, duration);
}

function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        const debouncedSearch = debounce((value) => {
            const table = input.closest('.billing-card').querySelector('.billing-table');
            if (table) {
                filterTable(table, value);
            }
        }, 300);
        
        input.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
    });
}

function filterTable(table, searchTerm) {
    const rows = table.querySelectorAll('tbody tr');
    const term = searchTerm.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
    });
}

// Export functions for global use
window.billingSystem = {
    formatCurrency,
    showAlert,
    confirmAction,
    showLoading,
    hideLoading,
    debounce,
    throttle,
    initializeSearch,
    filterTable
};

// Initialize search on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
});

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add keyboard navigation
document.addEventListener('keydown', function(e) {
    // Escape key to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
    
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// Add print functionality
function printPage() {
    window.print();
}

// Add export functionality
function exportToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tr');
    const csv = [];
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td, th');
        const rowData = Array.from(cells).map(cell => `"${cell.textContent.trim()}"`);
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Add to global scope
window.printPage = printPage;
window.exportToCSV = exportToCSV;