$(document).pjax('a:not(.no-pjax)', 'main');
$(document).on('ready pjax:complete', function() {
    $(document).activeNavigation("#nav-mobile");
    $('.modal-trigger').leanModal();
});

$('.collapsible').collapsible({
    accordion : false
});

$(".button-collapse").sideNav();
$(".dropdown-button").dropdown();

