document.addEventListener('DOMContentLoaded', function() {
    // Get all form elements
    const form = document.getElementById('registerForm');
    const fullName = document.getElementById('fullNameField');
    const email = document.getElementById('emailfield');
    const password = document.getElementById('passwordField');
    const confirmPassword = document.getElementById('PasswordField2');
    const terms = document.getElementById('terms');
    const registerBtn = document.getElementById('registerBtn');

    // Validation state object
    let validationState = {
        fullName: false,
        email: false,
        password: false,
        confirmPassword: false,
        terms: false
    };

    // Disable button initially
    registerBtn.disabled = true;

    // Function to check if all validations pass
    function checkAllValidations() {
        const allValid = Object.values(validationState).every(value => value === true);
        registerBtn.disabled = !allValid;
        return allValid;
    }

    // Full Name Validation
    fullName.addEventListener('input', function() {
        const value = this.value.trim();
        const nameRegex = /^[a-zA-Z\s]{3,}$/;
        const isValid = nameRegex.test(value);

        this.classList.remove('is-valid', 'is-invalid');
        this.classList.add(isValid ? 'is-valid' : 'is-invalid');

        const feedback = document.querySelector('.fullNameFeedbackArea');
        if (!isValid) {
            feedback.textContent = value.length < 3 ? 
                'Name must be at least 3 characters long' : 
                'Name can only contain letters and spaces';
            feedback.style.display = 'block';
        } else {
            feedback.style.display = 'none';
        }

        validationState.fullName = isValid;
        checkAllValidations();
    });

    // Email Validation
    email.addEventListener('input', function() {
        const value = this.value.trim();
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        const isValid = emailRegex.test(value);

        this.classList.remove('is-valid', 'is-invalid');
        this.classList.add(isValid ? 'is-valid' : 'is-invalid');

        const feedback = document.querySelector('.emailFeeBackArea');
        if (!isValid) {
            feedback.textContent = 'Please enter a valid email address';
            feedback.style.display = 'block';
        } else {
            feedback.style.display = 'none';
        }

        validationState.email = isValid;
        checkAllValidations();
    });

    // Password Validation
    password.addEventListener('input', function() {
        const value = this.value.trim();
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        const isValid = passwordRegex.test(value);

        this.classList.remove('is-valid', 'is-invalid');
        this.classList.add(isValid ? 'is-valid' : 'is-invalid');

        const feedback = document.querySelector('.passwordMessageArea');
        if (!isValid) {
            feedback.textContent = 'Password must be at least 8 characters and include uppercase, lowercase, number, and special character';
            feedback.style.display = 'block';
        } else {
            feedback.style.display = 'none';
        }

        validationState.password = isValid;
        
        // Revalidate confirm password if it has a value
        if (confirmPassword.value.trim() !== '') {
            confirmPassword.dispatchEvent(new Event('input'));
        }
        
        checkAllValidations();
    });

    // Confirm Password Validation
    confirmPassword.addEventListener('input', function() {
        const value = this.value.trim();
        const isValid = value === password.value.trim() && value !== '';

        this.classList.remove('is-valid', 'is-invalid');
        this.classList.add(isValid ? 'is-valid' : 'is-invalid');

        const feedback = this.nextElementSibling.nextElementSibling;
        if (!isValid) {
            feedback.textContent = value === '' ? 
                'Please confirm your password' : 
                'Passwords do not match';
            feedback.style.display = 'block';
        } else {
            feedback.style.display = 'none';
        }

        validationState.confirmPassword = isValid;
        checkAllValidations();
    });

    // Terms Checkbox Validation
    terms.addEventListener('change', function() {
        validationState.terms = this.checked;
        checkAllValidations();
    });

    // Password Visibility Toggle
    document.querySelectorAll('.password-toggle').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // Form Submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Trigger validation on all fields
        fullName.dispatchEvent(new Event('input'));
        email.dispatchEvent(new Event('input'));
        password.dispatchEvent(new Event('input'));
        confirmPassword.dispatchEvent(new Event('input'));

        // Only submit if all validations pass
        if (checkAllValidations()) {
            this.submit();
        }
    });

    // Initial validation check
    checkAllValidations();
});

// Keep the existing login validation code
document.addEventListener("DOMContentLoaded", function () {
    const emailField = document.getElementById("login-email");
    const passwordField = document.getElementById("login-password");
    const loginButton = document.getElementById("loginBtn");
    const emailFeedback = document.querySelector(".emailFeeBackArea");
    const passwordFeedback = document.querySelector(".passwordMessageArea");
    const togglePasswordIcon = document.querySelector(".toggle-password");

    // Regular expressions for validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Validation state
    const validationState = {
        email: false,
        password: false,
    };

    // Enable or disable the login button based on validation state
    const toggleLoginButton = () => {
        const allValid = Object.values(validationState).every((isValid) => isValid);
        if (loginButton) {
            loginButton.disabled = !allValid;
        }
    };

    // Validate email field
    emailField?.addEventListener("input", () => {
        const value = emailField.value.trim();
        if (!emailPattern.test(value)) {
            emailFeedback.textContent = "Please enter a valid email address";
            emailFeedback.style.display = "block";
            emailField.classList.add("is-invalid");
            validationState.email = false;
        } else {
            emailFeedback.style.display = "none";
            emailField.classList.remove("is-invalid");
            emailField.classList.add("is-valid");
            validationState.email = true;
        }
        toggleLoginButton();
    });

    // Validate password field
    passwordField?.addEventListener("input", () => {
        const value = passwordField.value.trim();
        if (value.length === 0) {
            passwordFeedback.textContent = "Password is required";
            passwordFeedback.style.display = "block";
            passwordField.classList.add("is-invalid");
            validationState.password = false;
        } else {
            passwordFeedback.style.display = "none";
            passwordField.classList.remove("is-invalid");
            passwordField.classList.add("is-valid");
            validationState.password = true;
        }
        toggleLoginButton();
    });

    // Initially disable login button if it exists
    if (loginButton) {
        loginButton.disabled = true;
    }
});
