$(document).pjax('a:not(.no-pjax)', 'main');
$(document).on('ready pjax:complete', function() {
    $(document).activeNavigation("#nav-mobile");
});

$('.collapsible').collapsible({
    accordion : false
});

$(".button-collapse").sideNav();
$(".dropdown-button").dropdown();
