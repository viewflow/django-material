$(document).pjax('a:not(.no-pjax)', 'main');
$(document)
  .on('pjax:start', function() { $('#load_indicator').fadeIn(200); })
  .on('pjax:end',   function() { $('#load_indicator').fadeOut(200); })
$(document).on('ready pjax:complete', function() {
    $(document).activeNavigation("#nav-mobile");
    $('.modal-trigger').leanModal();
});

$('.collapsible').collapsible({
    accordion : false
});

$(".button-collapse").sideNav();
$(".dropdown-button").dropdown();

