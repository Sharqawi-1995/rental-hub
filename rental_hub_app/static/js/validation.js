// Register Form Validation with Real-time Validation - v2.0
// All IDs are properly set up for frontend and backend validation

function validateLoginForm() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    let isValid = true;
    
    emailError.textContent = '';
    passwordError.textContent = '';
    
    if (!email) {
        emailError.textContent = 'Email is required.';
        isValid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        emailError.textContent = 'Please enter a valid email address.';
        isValid = false;
    }
    
    if (!password) {
        passwordError.textContent = 'Password is required.';
        isValid = false;
    }
    
    return isValid;
}

function validateRegisterForm() {
    const first_name = document.getElementById('first_name').value.trim();
    const last_name = document.getElementById('last_name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;
    const phone_1 = document.getElementById('phone_1').value.trim();
    const phone_2 = document.getElementById('phone_2').value.trim();
    const address = document.getElementById('address').value.trim();
    const role = document.getElementById('role').value;
    
    let isValid = true;
    
    // Clear only client-side error messages (those with IDs), preserve server-side errors
    document.querySelectorAll('.error-message').forEach(el => {
        // Only clear error messages that have IDs (client-side validation targets)
        // Server-side errors don't have IDs and should be preserved
        if (el.id && !el.classList.contains('server-error')) {
            el.textContent = '';
        }
    });
    
    if (!first_name) {
        document.getElementById('first_name-error').textContent = 'First name is required.';
        isValid = false;
    }
    
    if (!last_name) {
        document.getElementById('last_name-error').textContent = 'Last name is required.';
        isValid = false;
    }
    
    if (!email) {
        document.getElementById('email-error').textContent = 'Email is required.';
        isValid = false;
    } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
        document.getElementById('email-error').textContent = 'Please enter a valid email address (e.g., example@domain.com).';
        isValid = false;
    }
    
    if (!password) {
        document.getElementById('password-error').textContent = 'Password is required.';
        isValid = false;
    } else if (password.length < 8) {
        document.getElementById('password-error').textContent = 'Password must be at least 8 characters long.';
        isValid = false;
    }
    
    if (!confirm_password) {
        document.getElementById('confirm_password-error').textContent = 'Please confirm your password.';
        isValid = false;
    } else if (password !== confirm_password) {
        document.getElementById('confirm_password-error').textContent = 'Passwords do not match.';
        isValid = false;
    }
    
    if (!phone_1) {
        document.getElementById('phone_1-error').textContent = 'Phone 1 is required.';
        isValid = false;
    } else {
        const phoneDigits = phone_1.replace(/\D/g, '');
        if (phoneDigits.length < 10) {
            document.getElementById('phone_1-error').textContent = 'Phone number must be at least 10 digits.';
            isValid = false;
        }
    }
    
    if (phone_2) {
        const phone2Digits = phone_2.replace(/\D/g, '');
        if (phone2Digits.length < 10) {
            document.getElementById('phone_2-error').textContent = 'Phone number must be at least 10 digits.';
            isValid = false;
        }
    }
    
    if (!address) {
        document.getElementById('address-error').textContent = 'Address is required.';
        isValid = false;
    }
    
    if (!role) {
        document.getElementById('role-error').textContent = 'Please select a role.';
        isValid = false;
    }
    
    return isValid;
}

// Real-time validation for register form
function setupRegisterFormValidation() {
    const registerForm = document.getElementById('registerForm');
    if (!registerForm) return;
    
    // Get all input fields
    const fields = {
        first_name: document.getElementById('first_name'),
        last_name: document.getElementById('last_name'),
        email: document.getElementById('email'),
        password: document.getElementById('password'),
        confirm_password: document.getElementById('confirm_password'),
        phone_1: document.getElementById('phone_1'),
        phone_2: document.getElementById('phone_2'),
        address: document.getElementById('address'),
        role: document.getElementById('role')
    };
    
    // Real-time validation on blur (when user leaves field)
    if (fields.first_name) {
        fields.first_name.addEventListener('blur', function() {
            const errorEl = document.getElementById('first_name-error');
            if (!this.value.trim()) {
                errorEl.textContent = 'First name is required.';
            } else {
                errorEl.textContent = '';
            }
        });
    }
    
    if (fields.last_name) {
        fields.last_name.addEventListener('blur', function() {
            const errorEl = document.getElementById('last_name-error');
            if (!this.value.trim()) {
                errorEl.textContent = 'Last name is required.';
            } else {
                errorEl.textContent = '';
            }
        });
    }
    
    if (fields.email) {
        fields.email.addEventListener('blur', function() {
            const errorEl = document.getElementById('email-error');
            const email = this.value.trim();
            if (!email) {
                errorEl.textContent = 'Email is required.';
            } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
                errorEl.textContent = 'Please enter a valid email address (e.g., example@domain.com).';
            } else {
                errorEl.textContent = '';
            }
        });
    }
    
    if (fields.password) {
        fields.password.addEventListener('blur', function() {
            const errorEl = document.getElementById('password-error');
            if (!this.value) {
                errorEl.textContent = 'Password is required.';
            } else if (this.value.length < 8) {
                errorEl.textContent = 'Password must be at least 8 characters long.';
            } else {
                errorEl.textContent = '';
            }
        });
    }
    
    if (fields.confirm_password) {
        fields.confirm_password.addEventListener('blur', function() {
            const errorEl = document.getElementById('confirm_password-error');
            const password = fields.password ? fields.password.value : '';
            if (!this.value) {
                errorEl.textContent = 'Please confirm your password.';
            } else if (this.value !== password) {
                errorEl.textContent = 'Passwords do not match.';
            } else {
                errorEl.textContent = '';
            }
        });
    }
    
    if (fields.phone_1) {
        fields.phone_1.addEventListener('blur', function() {
            const errorEl = document.getElementById('phone_1-error');
            if (!this.value.trim()) {
                errorEl.textContent = 'Phone 1 is required.';
            } else {
                const phoneDigits = this.value.replace(/\D/g, '');
                if (phoneDigits.length < 10) {
                    errorEl.textContent = 'Phone number must be at least 10 digits.';
                } else {
                    errorEl.textContent = '';
                }
            }
        });
    }
    
    if (fields.phone_2) {
        fields.phone_2.addEventListener('blur', function() {
            const errorEl = document.getElementById('phone_2-error');
            if (this.value.trim()) {
                const phone2Digits = this.value.replace(/\D/g, '');
                if (phone2Digits.length < 10) {
                    errorEl.textContent = 'Phone number must be at least 10 digits.';
                } else {
                    errorEl.textContent = '';
                }
            } else {
                errorEl.textContent = '';
            }
        });
    }
    
    if (fields.address) {
        fields.address.addEventListener('blur', function() {
            const errorEl = document.getElementById('address-error');
            if (!this.value.trim()) {
                errorEl.textContent = 'Address is required.';
            } else {
                errorEl.textContent = '';
            }
        });
    }
    
    if (fields.role) {
        fields.role.addEventListener('change', function() {
            const errorEl = document.getElementById('role-error');
            if (!this.value) {
                errorEl.textContent = 'Please select a role.';
            } else {
                errorEl.textContent = '';
            }
        });
    }
    
    // Form submission validation
    registerForm.addEventListener('submit', function(e) {
        if (!validateRegisterForm()) {
            e.preventDefault();
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Login form validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            if (!validateLoginForm()) {
                e.preventDefault();
            }
        });
    }
    
    // Register form validation (with real-time validation)
    setupRegisterFormValidation();
});

