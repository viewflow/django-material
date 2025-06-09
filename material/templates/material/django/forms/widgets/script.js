/**
 * Password field with visibility toggle functionality
 */
up.compiler('[up-password-field]', function (element) {
  const button = element.querySelector('[data-trailing-button]');
  const input = element.querySelector('input[type="password"], input[type="text"]');
  
  if (!button || !input) return;
  
  function togglePasswordVisibility() {
    const isPassword = input.type === 'password';
    
    input.type = isPassword ? 'text' : 'password';
    button.textContent = isPassword ? 'visibility' : 'visibility_off';
    button.title = isPassword ? 'Hide password' : 'Show password';
  }
  
  button.addEventListener('click', togglePasswordVisibility);
  
  // Cleanup function
  return function() {
    button.removeEventListener('click', togglePasswordVisibility);
  };
});