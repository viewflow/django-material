up.compiler('[up-auto-grow]', function(element) {
  // Initial adjustment on load
  adjustHeight(element);

  // Listen for input events to adjust height as content changes
  element.addEventListener('input', function() {
    adjustHeight(element);
  });

  // Function to adjust height based on content
  function adjustHeight(el) {
    // Reset height to auto to get the right scrollHeight
    el.style.height = 'auto';
    
    // Set the height to scrollHeight to fit all content
    el.style.height = (el.scrollHeight) + 'px';
  }
});