document.addEventListener("DOMContentLoaded", function () {
    // Register form elements
    const fullNameField = document.getElementById("fullNameField");
    const emailField = document.getElementById("emailfield");
    const passwordField = document.getElementById("passwordField");
    const confirmPasswordField = document.getElementById("PasswordField2");
    const registerButton = document.getElementById("registerBtn");
    const togglePasswordIcons = document.querySelectorAll(".toggle-password");
  
    // Feedback areas
    const fullNameFeedback = document.querySelector(".fullNameFeedbackArea");
    const emailFeedback = document.querySelector(".emailFeeBackArea");
    const passwordFeedback = document.querySelector(".passwordMessageArea");
  
    // Validation patterns
    const namePattern = /^[a-zA-Z\s]{3,}$/;
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  
    // Validation state
    const validationState = {
        fullName: false,
        email: false,
        password: false,
        confirmPassword: false
    };
  
    // Enable or disable register button based on validation state
    const toggleRegisterButton = () => {
        const allValid = Object.values(validationState).every(isValid => isValid);
        if (registerButton) {
            registerButton.disabled = !allValid;
        }
    };
  
    // Validate Full Name
    fullNameField?.addEventListener("input", () => {
        const value = fullNameField.value.trim();
        fullNameField.classList.add("is-invalid");
        
        if (value.length === 0) {
            fullNameFeedback.textContent = "Full name is required";
            validationState.fullName = false;
        } else if (!namePattern.test(value)) {
            fullNameFeedback.textContent = "Name must contain at least 3 letters (only letters and spaces allowed)";
            validationState.fullName = false;
        } else {
            fullNameField.classList.remove("is-invalid");
            fullNameField.classList.add("is-valid");
            fullNameFeedback.style.display = "none";
            validationState.fullName = true;
        }
        
        fullNameFeedback.style.display = validationState.fullName ? "none" : "block";
        toggleRegisterButton();
    });
  
    // Validate Email
    emailField?.addEventListener("input", () => {
        const value = emailField.value.trim();
        emailField.classList.add("is-invalid");
        
        if (value.length === 0) {
            emailFeedback.textContent = "Email is required";
            validationState.email = false;
        } else if (!emailPattern.test(value)) {
            emailFeedback.textContent = "Please enter a valid email address (e.g., user@example.com)";
            validationState.email = false;
        } else {
            emailField.classList.remove("is-invalid");
            emailField.classList.add("is-valid");
            emailFeedback.style.display = "none";
            validationState.email = true;
        }
        
        emailFeedback.style.display = validationState.email ? "none" : "block";
        toggleRegisterButton();
    });
  
    // Validate Password
    passwordField?.addEventListener("input", () => {
        const value = passwordField.value.trim();
        passwordField.classList.add("is-invalid");
        
        if (value.length === 0) {
            passwordFeedback.textContent = "Password is required";
            validationState.password = false;
        } else if (!passwordPattern.test(value)) {
            passwordFeedback.textContent = "Password must be at least 8 characters and include uppercase, lowercase, number, and special character";
            validationState.password = false;
        } else {
            passwordField.classList.remove("is-invalid");
            passwordField.classList.add("is-valid");
            passwordFeedback.style.display = "none";
            validationState.password = true;
        }
        
        passwordFeedback.style.display = validationState.password ? "none" : "block";
        
        // Check confirm password when password changes
        if (confirmPasswordField.value.trim()) {
            validateConfirmPassword();
        }
        toggleRegisterButton();
    });
  
    // Validate Confirm Password
    const validateConfirmPassword = () => {
        const passwordValue = passwordField.value.trim();
        const confirmValue = confirmPasswordField.value.trim();
        const confirmFeedback = confirmPasswordField.nextElementSibling.nextElementSibling;
        
        confirmPasswordField.classList.add("is-invalid");

        if (confirmValue.length === 0) {
            confirmFeedback.textContent = "Please confirm your password";
            validationState.confirmPassword = false;
        } else if (confirmValue !== passwordValue) {
            confirmFeedback.textContent = "Passwords do not match";
            validationState.confirmPassword = false;
        } else {
            confirmPasswordField.classList.remove("is-invalid");
            confirmPasswordField.classList.add("is-valid");
            confirmFeedback.style.display = "none";
            validationState.confirmPassword = true;
        }
        
        confirmFeedback.style.display = validationState.confirmPassword ? "none" : "block";
        toggleRegisterButton();
    };
  
    confirmPasswordField?.addEventListener("input", validateConfirmPassword);
  
    // Toggle password visibility
    togglePasswordIcons.forEach(icon => {
        icon.addEventListener("click", () => {
            const inputField = icon.closest('.password-group').querySelector('input');
            if (inputField.type === "password") {
                inputField.type = "text";
                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");
            } else {
                inputField.type = "password";
                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");
            }
        });
    });
  
    // Initially disable register button and trigger validation for any pre-filled fields
    if (registerButton) {
        registerButton.disabled = true;
    }

    // Initial validation for pre-filled fields
    if (fullNameField?.value) fullNameField.dispatchEvent(new Event('input'));
    if (emailField?.value) emailField.dispatchEvent(new Event('input'));
    if (passwordField?.value) passwordField.dispatchEvent(new Event('input'));
    if (confirmPasswordField?.value) confirmPasswordField.dispatchEvent(new Event('input'));
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
