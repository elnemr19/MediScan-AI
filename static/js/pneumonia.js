document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const fileInput = form?.querySelector('input[type="file"]');
    const previewContainer = document.getElementById('image-preview');
    const submitBtn = form?.querySelector('button[type="submit"]');
    
    if (!form || !fileInput) return;

    // Client-side validation with better UX
    form.addEventListener('submit', function(e) {
        // Disable submit button during processing
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Processing...';
        }

        if (fileInput.files.length === 0) {
            showAlert('Please select a file first.', 'danger');
            e.preventDefault();
            resetSubmitButton();
            return;
        }
        
        const file = fileInput.files[0];
        const maxSize = 5 * 1024 * 1024; // 5MB
        
        // Size validation
        if (file.size > maxSize) {
            showAlert(`File too large (${(file.size/1024/1024).toFixed(2)}MB). Max 5MB allowed.`, 'danger');
            e.preventDefault();
            resetSubmitButton();
            return;
        }
        
        // Type validation
        const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            showAlert('Only JPG, PNG, and WebP images are allowed.', 'danger');
            e.preventDefault();
            resetSubmitButton();
            return;
        }
    });
    
    // Real-time preview and feedback
    fileInput.addEventListener('change', function() {
        resetSubmitButton();
        
        if (this.files.length > 0) {
            const file = this.files[0];
            
            // Show file info
            const fileInfo = `Selected: ${file.name} (${(file.size/1024).toFixed(2)}KB)`;
            console.log(fileInfo);
            
            // Display preview
            if (previewContainer) {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        previewContainer.innerHTML = `
                            <div class="mt-3">
                                <img src="${e.target.result}" class="img-thumbnail" style="max-height: 200px;">
                                <p class="text-muted mt-2">${fileInfo}</p>
                            </div>
                        `;
                    };
                    reader.readAsDataURL(file);
                } else {
                    previewContainer.innerHTML = `<div class="alert alert-warning mt-3">${fileInfo}</div>`;
                }
            }
        } else if (previewContainer) {
            previewContainer.innerHTML = '';
        }
    });

    // Helper functions
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

    function resetSubmitButton() {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Upload & Analyze';
        }
    }
});