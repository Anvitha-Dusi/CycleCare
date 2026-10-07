/**
 * static/js/auth.js
 * -----------------------------------------------------------------------------
 * Client-side authentication logic for CycleCare.
 * Demonstrates:
 * - HTML5 Form event interception and client-side validation
 * - Asynchronous HTTP communication with fetch() API
 * - JSON serialization and error handling
 * - UI feedback through non-intrusive toast alerts
 * -----------------------------------------------------------------------------
 */

// Toast notification helper
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// -----------------------------------------------------------------------------
// Register Form Handler
// -----------------------------------------------------------------------------
const registerForm = document.getElementById('register-form');
if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const submitBtn = document.getElementById('btn-register-submit');

    // 1. Client-Side Validations
    if (!name) {
      showToast('Please enter your full name.', 'error');
      document.getElementById('name').focus();
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailPattern.test(email)) {
      showToast('Please enter a valid email address.', 'error');
      document.getElementById('email').focus();
      return;
    }

    if (password.length < 6) {
      showToast('Password must be at least 6 characters long.', 'error');
      document.getElementById('password').focus();
      return;
    }

    if (password !== confirmPassword) {
      showToast('Passwords do not match. Please verify.', 'error');
      document.getElementById('confirm_password').focus();
      return;
    }

    // 2. Disable button during request
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating account...';

    try {
      // 3. Make asynchronous POST request to Flask API
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          email: email,
          password: password,
          confirm_password: confirmPassword
        })
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showToast(result.message || 'Registration successful! Redirecting...', 'success');
        setTimeout(() => {
          window.location.href = '/dashboard';
        }, 800);
      } else {
        showToast(result.message || 'Registration failed. Please try again.', 'error');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Create Account';
      }
    } catch (err) {
      console.error('Registration fetch error:', err);
      showToast('Network error. Please check your connection and try again.', 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Create Account';
    }
  });
}

// -----------------------------------------------------------------------------
// Login Form Handler
// -----------------------------------------------------------------------------
const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const submitBtn = document.getElementById('btn-login-submit');

    // 1. Client-Side Validations
    if (!email) {
      showToast('Please enter your email address.', 'error');
      document.getElementById('email').focus();
      return;
    }

    if (!password) {
      showToast('Please enter your password.', 'error');
      document.getElementById('password').focus();
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging in...';

    try {
      // 2. Make asynchronous POST request to Flask API
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showToast(result.message || 'Login successful! Redirecting...', 'success');
        setTimeout(() => {
          window.location.href = '/dashboard';
        }, 700);
      } else {
        showToast(result.message || 'Invalid email or password.', 'error');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Log In';
      }
    } catch (err) {
      console.error('Login fetch error:', err);
      showToast('Network error. Please check your connection and try again.', 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Log In';
    }
  });
}
