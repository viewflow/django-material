$(function($) {
  function updateLinks() {
    var $this = $(this);
    var siblings = $this.find('.change-related, .delete-related');

    if (!siblings.length) return;

    var value = $this.find('select').val();
    if (value) {
      siblings.each(function() {
        var elm = $(this);
        elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
      });
    } else {
      siblings.removeAttr('href');
    }
  }

  var container = $(document);
  container.on('change', 'select', function() {
    $(this).parents('.related-widget-wrapper').each(updateLinks);
  });
  container.find('.related-widget-wrapper').each(updateLinks);

  container.on('click', '.related-widget-wrapper-link', function(event){
    if (this.href) {
      showRelatedObjectPopup(this);
    }
    event.preventDefault();
  });

  // Update dropdown on Add/Change popup close
  container.on('change', '.related-widget-wrapper select', function() {
    $(this).not('.disabled').not('.material-ignore').material_select();
  });
});
