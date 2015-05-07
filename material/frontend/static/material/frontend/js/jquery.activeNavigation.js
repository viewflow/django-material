(function( $ ) {
    $.fn.activeNavigation = function(selector) {
        var pathname = window.location.pathname
        var hrefs = []
        $(selector).find("a:not(.no-navigation)").each(function(){
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
            hrefs[0].closest('li.header').find('.collapsible-header').addClass("active");
            //hrefs[0].closest('li.header').find('.collapsible-header').closest('li').addClass("active");
            hrefs[0].closest('li.header').find('.collapsible-body').css("display", "block");
        }
    };
})(jQuery);
