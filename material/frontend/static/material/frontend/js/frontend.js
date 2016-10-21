$(document).on("turbolinks:load", function() {
  $(".button-collapse").sideNav();
  $(document).activeNavigation("#slide-out");
});

$(document).on("turbolinks:before-cache", function() {
  $('#sidenav-overlay').remove();
  $('.drag-target').remove();
});

/*
$(document).on('submit', 'form[data-pjax-get]', function(event) {
    event.preventDefault()
    $.pjax({'container': 'main', 'url' :this.action + '?' + $(this).serialize()});
})
*/
