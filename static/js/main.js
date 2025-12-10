/**
 * Face Attendance System - Chapter 1 JavaScript
 * Main client-side functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Face Attendance System Chapter 1 loaded');
    
    // Add any Chapter 1 specific JS here
    // For now, we keep it minimal
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// Utility functions for future chapters
window.AttendanceSystem = {
    /**
     * Update UI element text with fade effect
     */
    updateElement: (selector, text) => {
        const element = document.querySelector(selector);
        if (element) {
            element.style.opacity = '0.5';
            setTimeout(() => {
                element.textContent = text;
                element.style.opacity = '1';
            }, 200);
        }
    },
    
    /**
     * Show toast notification
     */
    showToast: (message, type = 'info') => {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
        toast.style.zIndex = '1050';
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => toast.remove(), 3000);
    },
    
    /**
     * Check system health
     */
    checkHealth: async () => {
        try {
            const response = await fetch('/health');
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'error' };
        }
    }
};