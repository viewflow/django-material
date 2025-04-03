(() => {
  // material/templates/cotton/nav/script.js
  up.compiler("[up-nav-toggle]", function(element) {
    element.addEventListener("click", function(event) {
      event.preventDefault();
      document.body.toggleAttribute("data-nav-open");
    });
  });
})();
