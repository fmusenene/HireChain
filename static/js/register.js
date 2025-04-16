document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const form = document.getElementById('registerForm');
    const submitButton = document.getElementById('registerBtn');
    const companyName = document.getElementById('company_name');
    const fullName = document.getElementById('full_name');
    const email = document.getElementById('email');
    const phone = document.getElementById('phone');
    const password = document.getElementById('password');
    const password2 = document.getElementById('password2');
    const terms = document.getElementById('terms');

    // Validation state object
    const validationState = {
        company_name: false,
        full_name: false,
        email: false,
        phone: false,
        password: false,
        password2: false,
        terms: false
    };

    // Validation functions
    const validators = {
        company_name: (value) => {
            return value.length >= 2;
        },
        full_name: (value) => {
            return value.length >= 2 && /^[a-zA-Z\s]*$/.test(value);
        },
        email: (value) => {
            return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value);
        },
        phone: (value) => {
            return /^\+?[\d\s-]{10,}$/.test(value);
        },
        password: (value) => {
            return value.length >= 8 &&
                   /[A-Z]/.test(value) &&
                   /[a-z]/.test(value) &&
                   /[0-9]/.test(value) &&
                   /[^A-Za-z0-9]/.test(value);
        },
        password2: (value) => {
            return value === password.value;
        },
        terms: (checked) => {
            return checked;
        }
    };

    // Error messages
    const errorMessages = {
        company_name: 'Company name must be at least 2 characters long',
        full_name: 'Full name must be at least 2 characters and contain only letters and spaces',
        email: 'Please enter a valid email address',
        phone: 'Please enter a valid phone number (at least 10 digits)',
        password: 'Password must be at least 8 characters and include uppercase, lowercase, number, and special character',
        password2: 'Passwords do not match',
        terms: 'You must accept the terms and conditions'
    };

    // Function to validate a field
    function validateField(fieldName, element) {
        const value = element.type === 'checkbox' ? element.checked : element.value.trim();
        const isValid = validators[fieldName](value);
        const feedbackElement = document.getElementById(fieldName + 'Feedback');

        if (isValid) {
            element.classList.remove('is-invalid');
            element.classList.add('is-valid');
            if (feedbackElement) {
                feedbackElement.textContent = '';
            }
            validationState[fieldName] = true;
        } else {
            element.classList.add('is-invalid');
            element.classList.remove('is-valid');
            if (feedbackElement) {
                feedbackElement.textContent = errorMessages[fieldName];
            }
            validationState[fieldName] = false;
        }

        updateSubmitButton();
    }

    // Function to update submit button state
    function updateSubmitButton() {
        const isFormValid = Object.values(validationState).every(state => state === true);
        submitButton.disabled = !isFormValid;
    }

    // Add event listeners to all fields
    if (companyName) {
        companyName.addEventListener('input', () => validateField('company_name', companyName));
        companyName.addEventListener('blur', () => validateField('company_name', companyName));
    }

    if (fullName) {
        fullName.addEventListener('input', () => validateField('full_name', fullName));
        fullName.addEventListener('blur', () => validateField('full_name', fullName));
    }

    if (email) {
        email.addEventListener('input', () => validateField('email', email));
        email.addEventListener('blur', () => validateField('email', email));
    }

    if (phone) {
        phone.addEventListener('input', () => validateField('phone', phone));
        phone.addEventListener('blur', () => validateField('phone', phone));
    }

    if (password) {
        password.addEventListener('input', () => {
            validateField('password', password);
            if (password2.value) {
                validateField('password2', password2);
            }
        });
        password.addEventListener('blur', () => validateField('password', password));
    }

    if (password2) {
        password2.addEventListener('input', () => validateField('password2', password2));
        password2.addEventListener('blur', () => validateField('password2', password2));
    }

    if (terms) {
        terms.addEventListener('change', () => validateField('terms', terms));
    }

    // Password toggle functionality
    document.querySelectorAll('.btn-toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            const icon = this.querySelector('i');

            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // Form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Validate all fields before submission
            validateField('company_name', companyName);
            validateField('full_name', fullName);
            validateField('email', email);
            validateField('phone', phone);
            validateField('password', password);
            validateField('password2', password2);
            validateField('terms', terms);

            const isFormValid = Object.values(validationState).every(state => state === true);
            if (isFormValid) {
                this.submit();
            }
        });
    }

    // Login form validation
    const loginForm = document.getElementById('loginForm');
    const loginButton = document.getElementById('loginBtn');
    const loginEmail = document.getElementById('login-email');
    const loginPassword = document.getElementById('login-password');
    const emailFeedback = document.querySelector('.emailFeeBackArea');
    const passwordFeedback = document.querySelector('.passwordMessageArea');

    if (loginForm) {
        const loginFields = {
            email: {
                element: loginEmail,
                feedback: emailFeedback,
                validate: (value) => {
                    if (!value) return 'Email is required';
                    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                    if (!emailRegex.test(value)) return 'Please enter a valid email address';
                    return '';
                }
            },
            password: {
                element: loginPassword,
                feedback: passwordFeedback,
                validate: (value) => {
                    if (!value) return 'Password is required';
                    return '';
                }
            }
        };

        Object.keys(loginFields).forEach(fieldName => {
            const field = loginFields[fieldName];
            if (field.element) {
                field.element.addEventListener('input', () => {
                    validateLoginField(fieldName);
                    updateLoginButton();
                });

                field.element.addEventListener('blur', () => {
                    validateLoginField(fieldName);
                    updateLoginButton();
                });
            }
        });

        function validateLoginField(fieldName) {
            const field = loginFields[fieldName];
            if (!field.element) return true;

            const value = field.element.value.trim();
            const error = field.validate(value);

            if (error) {
                field.element.classList.add('is-invalid');
                field.element.classList.remove('is-valid');
                if (field.feedback) {
                    field.feedback.textContent = error;
                    field.feedback.style.display = 'block';
                }
                return false;
            } else {
                field.element.classList.remove('is-invalid');
                field.element.classList.add('is-valid');
                if (field.feedback) {
                    field.feedback.textContent = '';
                    field.feedback.style.display = 'none';
                }
                return true;
            }
        }

        function updateLoginButton() {
            if (!loginButton) return;

            const isValid = Object.keys(loginFields).every(fieldName => {
                const field = loginFields[fieldName];
                if (!field.element) return true;
                const value = field.element.value.trim();
                return !field.validate(value);
            });

            loginButton.disabled = !isValid;
        }

        // Initial state
        if (loginButton) {
            loginButton.disabled = true;
        }
    }
});
