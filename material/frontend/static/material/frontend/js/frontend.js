$(document).on("turbolinks:load", function() {
  $(".button-collapse").sideNav();
  $(document).activeNavigation("#slide-out");
  $('#slide-out').perfectScrollbar();
});

$(document).on("turbolinks:before-cache", function() {
  $('#sidenav-overlay').remove();
  $('.drag-target').remove();
  $('#slide-out').perfectScrollbar('destroy');
});

/*
$(document).on('submit', 'form[data-pjax-get]', function(event) {
    event.preventDefault()
    $.pjax({'container': 'main', 'url' :this.action + '?' + $(this).serialize()});
})
*/
