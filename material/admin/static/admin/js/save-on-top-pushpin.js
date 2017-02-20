(function($) {
  'use strict';

    // push pinning "card-title"

    $('.pushpinned').each(function() {
      var top = $(this).offset().top;
      var width = $(this).parents('div.card').width();
      var height = $(this).parents('div.card').height() || 0;
      $('.pushpinned')
          .width(width)
          .pushpin({
            top: top,
            bottom: top + height,
            offset: 0
          });
    });

    // copying dropdown from bottom submit line

    var dropdown_wrapper = $('#pushpinned-save-dropdown-wrapper');

    var save_dropdown = $('#save-dropdown-admin');
    var save_dropdown_btn = $('[data-activates="save-dropdown-admin"]');

    if (save_dropdown != undefined && save_dropdown_btn != undefined) {

        var save_dropdown_new = $(save_dropdown[0].outerHTML).attr('id', 'save-dropdown-admin-pushpinned');
        var save_dropdown_btn_new = $(save_dropdown_btn[0].outerHTML).attr('data-activates', 'save-dropdown-admin-pushpinned');

        dropdown_wrapper.append(save_dropdown_btn_new);
        dropdown_wrapper.append(save_dropdown_new);

        save_dropdown_btn_new.dropdown();
      
    }

})(django.jQuery);