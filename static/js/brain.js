// Enhanced version if you want separate JS file
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('brain-upload-form');
    const fileInput = document.getElementById('brain-file-input');
    const preview = document.getElementById('brain-preview');
    
    if (!form || !fileInput) return;
    
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            
            // Check file type
            if (!file.type.match('image.*')) {
                preview.innerHTML = `
                    <div class="alert alert-warning">
                        Unsupported file type. Please upload an image.
                    </div>
                `;
                return;
            }
            
            // Display preview
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.innerHTML = `
                    <div class="card border-primary">
                        <div class="card-header bg-primary text-white">
                            Scan Preview
                        </div>
                        <div class="card-body">
                            <img src="${e.target.result}" class="img-fluid">
                            <div class="mt-2">
                                <span class="badge bg-secondary">
                                    ${file.name}
                                </span>
                                <span class="badge bg-info ms-2">
                                    ${(file.size/1024).toFixed(1)} KB
                                </span>
                            </div>
                        </div>
                    </div>
                `;
            };
            reader.readAsDataURL(file);
        }
    });
});