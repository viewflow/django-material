django.jQuery(function($){
    function updateLinks() {
        var $this = $(this);
        var siblings = $this.closest('.related-widget-wrapper > .col').nextAll('.change-related, .delete-related');
        if (!siblings.length) return;
        var value = $this.val();
        if (value) {
            siblings.each(function(){
                var elm = $(this);
                elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
            });
        } else siblings.removeAttr('href');
    }
    var container = $(document);
    container.on('change', '.related-widget-wrapper select', updateLinks);
    // Materialize use its own jquery declared in global scope. Listen on it.
    jQuery('.related-widget-wrapper select').on('change', updateLinks);
    container.find('.related-widget-wrapper select').each(updateLinks);
    container.on('click', '.related-widget-wrapper-link', function(event){
        if (this.href) {
            showRelatedObjectPopup(this);
        }
        event.preventDefault();
    });
});
