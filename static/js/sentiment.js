document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('sentiment-form');
    const textarea = document.getElementById('feedback-text');
    const charCounter = document.getElementById('char-counter');
    const submitBtn = form?.querySelector('button[type="submit"]');
    
    if (!form || !textarea) return;

    // Real-time character counter
    textarea.addEventListener('input', function() {
        const currentLength = this.value.length;
        charCounter.textContent = `${currentLength}/1000`;
        
        // Visual feedback
        if (currentLength < 10) {
            charCounter.classList.add('text-danger');
            charCounter.classList.remove('text-success');
        } else {
            charCounter.classList.remove('text-danger');
            charCounter.classList.add('text-success');
        }
    });

    // Form submission handling
    form.addEventListener('submit', function(e) {
        const text = textarea.value.trim();
        
        // Client-side validation
        if (text.length < 10) {
            e.preventDefault();
            showAlert('Please enter at least 10 characters for analysis', 'danger');
            return;
        }
        
        // Disable button during processing
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Analyzing...';
        }
    });

    // AJAX analysis for real-time feedback (optional)
    textarea.addEventListener('blur', function() {
        const text = this.value.trim();
        if (text.length >= 10 && text.length <= 1000) {
            // Could implement real-time analysis here if desired
        }
    });

    // Helper function to show alerts
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show mt-3`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const flashContainer = document.getElementById('flash-messages') || form;
        flashContainer.prepend(alertDiv);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 5000);
    }
});