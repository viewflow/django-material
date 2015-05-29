if (navigator.appVersion.indexOf('Win') != -1) {
    document.write('<link rel="stylesheet" type="text/css" href="{% static "material/css/robotofix.css" %}">');
}

$(document).on('ready pjax:complete', function() {
    $('.dropdown-button').dropdown({hover: false});
    $('.button-collapse').sideNav();
    $('select').not('.disabled').not('.material-ignore').material_select();

    $('[data-form-control="date"]').each(function() {
        var input = $(this);
        input.datetimepicker({format: input.data('date-format'), timepicker:false, mask:false});
    });
    $('[data-form-control="time"]').each(function() {
        var input = $(this);
        input.datetimepicker({format: input.data('date-format'), datepicker: false, timepicker:true, mask:false});
    });
    $('[data-form-control="datetime"]').each(function() {
        var input = $(this);
        input.datetimepicker({format: input.data('date-format'), datepicker: true, timepicker:true, mask:false});
    });
    $('.formset-field').formset({
        animateForms: true
    });

    /*
      In chrome, there is no way to get to know is autofill
      fills the password field until user is interacted. Assume
      that it is
    */
    if($('input[type=password]').length) {
        function autofix() {
            $('input[type=password]').addClass('active');
            $('input[type=password]').next('label').addClass('active');
            $('input[type=password]').prev('i').addClass('active');
            userInteracted();
        }

        function userInteracted() {
            $('body').off('input propertychange', 'input[type=text]', autofix);
            $('body').off('input propertychange', 'input[type=email]', autofix);
            $('body,html').unbind('scroll mousedown DOMMouseScroll mousewheel keyup', userInteracted);
        }

        $('body').on('input propertychange', 'input[type=text]', autofix);
        $('body').on('input propertychange', 'input[type=email]', autofix);
        $('body,html').bind('scroll mousedown DOMMouseScroll mousewheel keyup', userInteracted);
    }
});
