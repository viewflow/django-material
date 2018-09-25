/* global $ */

// submit GET forms with turbolinks
$(document).on("submit", "form[data-control-form][method=get]", function(e) {
  Turbolinks.visit(
    this.action +
      (this.action.indexOf('?') == -1 ? '?' : '&') +
      $(this).serialize()
  );
  return false;
});
