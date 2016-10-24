(function($) {
  $(document).on('ready turbolinks:load', function() {
    $('[data-form-control="date-today-shortcut"]').click(function() {
        var now = Date(),
            datePicker = $(this).closest('.input-group').find('[data-form-control="date"]').data('xdsoft_datetimepicker'),
            timePicker = $(this).closest('.input-group').find('[data-form-control="time"]').data('xdsoft_datetimepicker'),
            datetimePicker = $(this).closest('.input-group').find('[data-form-control="datetime"]').data('xdsoft_datetimepicker');
        
        if(datePicker != undefined) {
            datePicker.setOptions({'value': now});
        };
        if(timePicker != undefined) {
            timePicker.setOptions({'value': now});
        };
        if(datetimePicker != undefined) {
            datetimePicker.setOptions({'value': now});
        };
        $(this).closest('.input-group').find('label').css('class', 'active');
        
        return false;
    });
  });
})(django.jQuery);
