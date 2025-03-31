document.addEventListener("DOMContentLoaded", function () {
    const fullNameField = document.getElementById("fullNameField");
    const emailField = document.getElementById("emailfield");
    const passwordField = document.getElementById("passwordField");
    const confirmPasswordField = document.getElementById("PasswordField2");
    const registerButton = document.querySelector(".submit-button");
    const togglePasswordIcons = document.querySelectorAll(".toggle-password");
  
    // Feedback areas
    const fullNameFeedback = document.querySelector(".fullNameFeedbackArea");
    const emailFeedback = document.querySelector(".emailFeeBackArea");
    const passwordFeedback = document.querySelector(".passwordMessageArea");
  
    // Regex patterns for validation
    const namePattern = /^[a-zA-Z\s]+$/; // Full Name: Letters and spaces only
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Email format
    const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/; // Password requirements
  
    // Disable register button initially
    registerButton.disabled = true;
  
    // Validation state
    const validationState = {
      fullName: false,
      email: false,
      password: false,
      confirmPassword: false,
    };
  
    // Enable or disable the register button based on validation state
    const toggleRegisterButton = () => {
      const allValid = Object.values(validationState).every((isValid) => isValid);
      registerButton.disabled = !allValid;
    };
  
    // Validate Full Name
    fullNameField.addEventListener("input", () => {
      const value = fullNameField.value.trim();
      if (!namePattern.test(value)) {
        fullNameFeedback.textContent = "Full Name must contain only letters and spaces.";
        fullNameFeedback.style.display = "block";
        fullNameField.classList.add("is-invalid");
        validationState.fullName = false;
      } else {
        fullNameFeedback.style.display = "none";
        fullNameField.classList.remove("is-invalid");
        fullNameField.classList.add("is-valid");
        validationState.fullName = true;
      }
      toggleRegisterButton();
    });
  
    // Validate Email
    emailField.addEventListener("input", () => {
      const value = emailField.value.trim();
      if (!emailPattern.test(value)) {
        emailFeedback.textContent = "Enter a valid email address.";
        emailFeedback.style.display = "block";
        emailField.classList.add("is-invalid");
        validationState.email = false;
      } else {
        emailFeedback.style.display = "none";
        emailField.classList.remove("is-invalid");
        emailField.classList.add("is-valid");
        validationState.email = true;
      }
      toggleRegisterButton();
    });
  
    // Validate Password
    passwordField.addEventListener("input", () => {
      const value = passwordField.value.trim();
      if (!passwordPattern.test(value)) {
        passwordFeedback.textContent =
          "Password must be at least 8 characters long, include a capital letter, a number, and a special character.";
        passwordFeedback.style.display = "block";
        passwordField.classList.add("is-invalid");
        validationState.password = false;
      } else {
        passwordFeedback.style.display = "none";
        passwordField.classList.remove("is-invalid");
        passwordField.classList.add("is-valid");
        validationState.password = true;
      }
      toggleRegisterButton();
    });
  
    // Confirm Password Match
    confirmPasswordField.addEventListener("input", () => {
      const passwordValue = passwordField.value.trim();
      const confirmPasswordValue = confirmPasswordField.value.trim();
      if (confirmPasswordValue !== passwordValue) {
        passwordFeedback.textContent = "Passwords do not match.";
        passwordFeedback.style.display = "block";
        confirmPasswordField.classList.add("is-invalid");
        validationState.confirmPassword = false;
      } else {
        passwordFeedback.style.display = "none";
        confirmPasswordField.classList.remove("is-invalid");
        confirmPasswordField.classList.add("is-valid");
        validationState.confirmPassword = true;
      }
      toggleRegisterButton();
    });
  
    // Toggle Password Visibility
    togglePasswordIcons.forEach((icon) => {
      icon.addEventListener("click", () => {
        const target = document.querySelector(icon.dataset.target);
        if (target.type === "password") {
          target.type = "text";
          icon.classList.remove("fa-eye");
          icon.classList.add("fa-eye-slash");
        } else {
          target.type = "password";
          icon.classList.remove("fa-eye-slash");
          icon.classList.add("fa-eye");
        }
      });
    });
  });


  document.addEventListener("DOMContentLoaded", function () {
  const emailField = document.getElementById("login-email");
  const passwordField = document.getElementById("login-password");
  const loginButton = document.getElementById("loginBtn");
  const emailFeedback = document.querySelector(".emailFeeBackArea");
  const passwordFeedback = document.querySelector(".passwordMessageArea");
  const togglePasswordIcon = document.querySelector(".toggle-password");

  // Regular expressions for validation
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Email format
  
  // Disable login button initially
  loginButton.disabled = true;

  // Validation state
  const validationState = {
    email: false,
    password: false,
  };

  // Enable or disable the login button based on validation state
  const toggleLoginButton = () => {
    const allValid = Object.values(validationState).every((isValid) => isValid);
    loginButton.disabled = !allValid;
  };

  // Validate email field
  emailField.addEventListener("input", () => {
    const value = emailField.value.trim();
    if (!emailPattern.test(value)) {
      emailFeedback.textContent = "Please enter a valid email address.";
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
  passwordField.addEventListener("input", () => {
    const value = passwordField.value.trim();
    if (value.length === 0) {
      passwordFeedback.textContent = "Password is required.";
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

  // Toggle password visibility
  togglePasswordIcon.addEventListener("click", () => {
    if (passwordField.type === "password") {
      passwordField.type = "text";
      togglePasswordIcon.classList.remove("fa-eye");
      togglePasswordIcon.classList.add("fa-eye-slash");
    } else {
      passwordField.type = "password";
      togglePasswordIcon.classList.remove("fa-eye-slash");
      togglePasswordIcon.classList.add("fa-eye");
    }
  });
});
