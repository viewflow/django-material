(function( $ ) {
    function getUrlParameter(sParam)
    {
        var sPageURL = window.location.search.substring(1);
        var sURLVariables = sPageURL.split('&');
        for (var i = 0; i < sURLVariables.length; i++)
        {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == sParam)
            {
                return decodeURIComponent(sParameterName[1]);
            }
        }
    }

    $.fn.activeNavigation = function(selector) {
        var pathname = getUrlParameter('back') || window.location.pathname;

        var hrefs = [];
        $(selector).find("a:not(.no-navigation)").each(function() {
            if (pathname.indexOf($(this).attr("href")) > -1)
                hrefs.push($(this));
        })

        if (hrefs.length) {
            hrefs.sort(function(a,b){
                return a.attr("href").length < b.attr("href").length;
            })
            $(selector).find("li").removeClass("active");
            $(selector).find("a").removeClass("active");
            hrefs[0].closest('li').addClass("active");
            hrefs[0].closest('div').closest('li').addClass('active');
            hrefs[0].parents('li').addClass('active');
            hrefs[0].closest('li.header').find('.collapsible-header:first').addClass("active");
            hrefs[0].closest('li.header').find('.collapsible-body:first').css("display", "block");
        }
    };
})(jQuery);
