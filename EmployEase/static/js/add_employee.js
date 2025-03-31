function previewImage() {
    const fileInput = document.getElementById('profile-image');
    const fileSizeError = document.getElementById('image-size-error');
    const imagePreview = document.getElementById('image-preview');
    const file = fileInput.files[0];

    // Clear previous image preview
    imagePreview.style.backgroundImage = '';

    if (file) {
        // Check if the file is less than 4MB
        if (file.size > 4 * 1024 * 1024) {
            fileSizeError.style.display = 'block';
            fileInput.value = '';  // Clear the file input
        } else {
            fileSizeError.style.display = 'none';

            // Create a preview of the image
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.style.backgroundImage = `url(${e.target.result})`;
            };
            reader.readAsDataURL(file);
        }
    }
}

// Function to toggle password visibility
function togglePasswordVisibility(fieldId, iconId) {
    const field = document.getElementById(fieldId);
    const icon = document.getElementById(iconId);
    const type = field.type === "password" ? "text" : "password";
    field.type = type;

    // Toggle eye icon (crossed when password is visible)
    if (field.type === "password") {
        icon.innerHTML = '<i class="fas fa-eye"></i>';  // Show eye
    } else {
        icon.innerHTML = '<i class="fas fa-eye-slash"></i>';  // Show crossed eye
    }
}
