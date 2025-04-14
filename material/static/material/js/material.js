(() => {
  // material/templates/cotton/nav/script.js
  up.compiler("[up-nav-toggle]", function(element) {
    element.addEventListener("click", function() {
      document.body.toggleAttribute("data-nav-open");
    });
  });
  up.compiler("[up-nav-toggle-off]", function(element) {
    element.addEventListener("click", function() {
      document.body.removeAttribute("data-nav-open");
    });
  });

  // material/templates/cotton/forms/textarea/script.js
  up.compiler("[up-auto-grow]", function(element) {
    requestAnimationFrame(function() {
      adjustHeight(element);
    });
    element.addEventListener("input", function() {
      adjustHeight(element);
    });
    function adjustHeight(el) {
      el.style.height = "auto";
      el.style.height = el.scrollHeight + 2 + "px";
    }
  });

  // material/templates/cotton/button/script.js
  up.compiler("[up-ripple]", function(elementWithRipple) {
    elementWithRipple.addEventListener("pointerdown", (mouseEvent) => {
      elementWithRipple.style.setProperty("--ripple-x", `${mouseEvent.offsetX}px`);
      elementWithRipple.style.setProperty("--ripple-y", `${mouseEvent.offsetY}px`);
    });
  });
})();
