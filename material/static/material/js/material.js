(() => {
  // material/templates/cotton/nav/script.js
  up.compiler("[up-nav-toggle]", function(element) {
    element.addEventListener("click", function(event) {
      document.body.toggleAttribute("data-nav-open");
    });
  });
  up.compiler("[up-nav-toggle-off]", function(element) {
    element.addEventListener("click", function(event) {
      document.body.removeAttribute("data-nav-open");
    });
  });

  // material/templates/cotton/forms/textarea/script.js
  up.compiler("[up-auto-grow]", function(element) {
    adjustHeight(element);
    element.addEventListener("input", function() {
      adjustHeight(element);
    });
    function adjustHeight(el) {
      el.style.height = "auto";
      el.style.height = el.scrollHeight + "px";
    }
  });
})();
