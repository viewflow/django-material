up.compiler('[up-nav-toggle]', function(element) {
  element.addEventListener('click', function(event) {
    document.body.toggleAttribute('data-nav-open');
  });
});

up.compiler('[up-nav-toggle-off]', function(element) {
  element.addEventListener('click', function(event) {
    document.body.removeAttribute('data-nav-open');
  });
});