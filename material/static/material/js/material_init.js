$(document).on('ready pjax:complete', function() {
    function material_init($container) {
        $container.find('.dropdown-button.constrain_width').dropdown({hover: false, constrain_width: true});
        $container.find('.dropdown-button').not('.constrain_width').dropdown({hover: false, constrain_width: false});
        $container.find('select').not('.disabled').not('.material-ignore').material_select();

        $container.find('[data-form-control="date"]').each(function() {
            var input = $(this);
            input.datetimepicker({format: input.data('date-format'), timepicker:false, mask:false, scrollInput:false});
        });
        $container.find('[data-form-control="time"]').each(function() {
            var input = $(this);
            input.datetimepicker({format: input.data('date-format'), datepicker: false, timepicker:true, mask:false, scrollInput:false});
        });
        $container.find('[data-form-control="datetime"]').each(function() {
            var input = $(this);
            input.datetimepicker({format: input.data('date-format'), datepicker: true, timepicker:true, mask:false, scrollInput:false});
        });
    }
    $('.formset-field').formset({
        animateForms: true,
        newFormCallback: material_init
    });

    material_init($(document));
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
