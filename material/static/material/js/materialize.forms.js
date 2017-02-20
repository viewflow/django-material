(function() {
  function initForms ($container) {
    // Formsets
    // https://bitbucket.org/ionata/django-formset-js
    $('.formset-field').formset({
      animateForms: true,
      newFormCallback: initForms
    })
    
    // Select
    // http://materializecss.com/forms.html#select
    $container
      .find('select')
      .not('.disabled')
      .not('.material-ignore')
      .material_select()
    
    // Date/DateTime/Time
    // https://github.com/xdan/datetimepicker
    $container
      .find('[data-form-control="date"]')
      .each(function () {
        $(this).datetimepicker({
          format: this.dataset.dateFormat,
          timepicker: false,
          mask: false,
          scrollInput: false
        })
      })
    $container
      .find('[data-form-control="time"]')
      .each(function () {
        $(this).datetimepicker({
          format: this.dataset.dateFormat,
          datepicker: false,
          timepicker: true,
          mask: false,
          scrollInput: false
        })
      })
    $container.find('[data-form-control="datetime"]').each(
      function () {
        $(this).datetimepicker({
          format: this.dataset.dateFormat,
          datepicker: true,
          timepicker: true,
          mask: false,
          scrollInput: false
        })
      })

    $container.find('.pushpinned').each(
      function() {
        var top = $(this).offset().top;
        var width = $(this).parents('div.card').width();
        var height = $(this).parents('div.card').height() || 0;
        $('.pushpinned')
          .width(width)
          .pushpin({
            top: top,
            bottom: top + height,
            offset: 0
          })
    })

    if ($container.find('.pushpinned').length == 1) {

      var save_dropdown = $('#save-dropdown-admin');
      var save_dropdown_btn = $('[data-activates="save-dropdown-admin"]');

      if (save_dropdown != undefined && save_dropdown_btn != undefined) {

          var save_dropdown_new = $(save_dropdown[0].outerHTML)
                                    .attr('id', 'save-dropdown-admin-pushpinned');

          var save_dropdown_btn_new = $(save_dropdown_btn[0].outerHTML)
                                        .attr('data-activates', 'save-dropdown-admin-pushpinned');

          $container
            .find('#pushpinned-save-dropdown-wrapper')
            .append(save_dropdown_btn_new);

          $container
            .find('#pushpinned-save-dropdown-wrapper')
            .append(save_dropdown_new);

          save_dropdown_btn_new.dropdown();
        
      }

    }
  }

  $(document).on('ready turbolinks:load', function() { initForms($(document)) })
})()
