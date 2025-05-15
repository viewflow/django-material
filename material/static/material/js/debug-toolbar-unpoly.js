/**
 * Integration between Django Debug Toolbar and Unpoly.js
 * 
 * Reinitializes the debug toolbar after Unpoly fragment updates
 */
up.on('up:fragment:inserted', function() {
  if (window.djdt && typeof window.djdt.init === 'function') {
    window.djdt.init();
  }
});