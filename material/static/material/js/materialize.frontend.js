/* global $ */
$(document).on('turbolinks:before-render', function (event) {
  $(event.originalEvent.data.newBody).activeNavigation('#slide-out')
})

$(document).on('turbolinks:load', function () {
  // Sidenav
  // http://materializecss.com/side-nav.html
  $('.sidenav').sidenav()
  $(document).activeNavigation('#slide-out')

  // https://github.com/noraesae/perfect-scrollbar#how-to-use
  $('#slide-out').perfectScrollbar()
})

$(document).on('turbolinks:before-cache', function () {
  // Sidenav
  $('.sidenav').sidenav('destroy')
  $('.sidenav').css('transform', '')
  $('.drag-target').remove()
  $('#slide-out').perfectScrollbar('destroy')

  // Toasts
  $('script#messages').remove()
  M.Toast.dismissAll();
  $('div#toast-container').css('display', 'none')
})

// submit GET forms with turbolinks
$(document).on("submit", "form[data-control-form][method=get]", function(e) {
  Turbolinks.visit(
    this.action +
      (this.action.indexOf('?') == -1 ? '?' : '&') +
      $(this).serialize()
  );
  return false;
});
