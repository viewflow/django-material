$(document).pjax('a:not(.no-pjax)', 'main');
$(document).on('submit', 'form[data-pjax-get]', function(event) {
    event.preventDefault()
    $.pjax({'container': 'main', 'url' :this.action + '?' + $(this).serialize()});
})
$(document)
    .on('pjax:start', function() { $('#load_indicator').animate({opacity:1},200,'easeOutExpo').fadeIn(200); })
    .on('pjax:success', function() { $('#load_indicator').stop(true).fadeOut(200); })
    .on('pjax:error', function(xhr, textStatus, error) {  Materialize.toast(error, 10000)});

$(document).on('ready pjax:complete', function() {
    $(document).activeNavigation("#nav-mobile");
    $('.modal-trigger').leanModal();
});

$('.collapsible').collapsible({
    accordion : false
});

$(".button-collapse").sideNav();
$(".dropdown-button").dropdown();
