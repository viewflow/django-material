$(document).on("turbolinks:load", function() {

  // Sidenav
  // http://materializecss.com/side-nav.html
  // https://github.com/noraesae/perfect-scrollbar#how-to-use
  $(".button-collapse").sideNav();
  $(document).activeNavigation("#slide-out");
  $('#slide-out').perfectScrollbar();

  // Dropdowns
  // http://materializecss.com/dropdown.html
  $container
    .find('.dropdown-button.constrain_width')
    .dropdown({hover: false, constrain_width: true});

  $container
    .find('.dropdown-button')
    .not('.constrain_width')
    .dropdown({hover: false, constrain_width: false});
});

$(document).on("turbolinks:before-cache", function() {
  // Sidenav
  $('#sidenav-overlay').remove();
  $('.drag-target').remove();
  $('#slide-out').perfectScrollbar('destroy');
});
