$(document).pjax('a:not(.no-pjax)', 'main', {timeout: 2500});

$(document).on('ready', function() {
      $(document).find('.button-collapse').sideNav();
});


$(document).on('submit', 'form[data-pjax-get]', function(event) {
    event.preventDefault()
    $.pjax({'container': 'main', 'url' :this.action + '?' + $(this).serialize()});
})
$(document)
    .on('pjax:start', function() { $('#load_indicator').animate({opacity:1},200,'easeOutExpo').fadeIn(200); })
    .on('pjax:end', function() { $('#load_indicator').stop(true).fadeOut(200); })
    .on('pjax:error', function(xhr, textStatus, error) {  Materialize.toast(error, 10000)});

$(document).on('pjax:beforeReplace', function() {
  $('.drag-target').remove();
  $('#sidenav-overlay').trigger('click');
});

$(document).on('ready pjax:complete', function() {
    $(document).activeNavigation("#nav-mobile");
    $('.modal-trigger').leanModal();
});

$('.collapsible').collapsible({
    accordion : false
});

$(".dropdown-button").dropdown();
