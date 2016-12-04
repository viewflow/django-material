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
                return b.attr("href").length - a.attr("href").length;
            })
            var href = hrefs[0];
            for(var i=1; i< hrefs.length; i++) {
                if(hrefs[i].attr('href') === href.attr('href')) {
                    href = hrefs[i];
                }
            }
            $(selector).find("li").removeClass("active");
            href.parents('li').addClass('active');
            href.parent('li').closest('.collapsible-body').css('display', "block");
            href.parent('li').closest('.collapsible-body').parent('li').addClass('active');
        }
    };
})(jQuery);
