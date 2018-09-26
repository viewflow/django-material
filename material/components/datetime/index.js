class DateTime extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    var lang = jQuery( ":root" ).attr('lang');
    if(lang) {
      jQuery.datetimepicker.setLocale(lang.substr(0, 2));
    }

    $(this)
      .find('[data-form-control="date"]')
      .each(function () {
        $(this).datetimepicker({
          format: this.dataset.dateFormat,
          timepicker: false,
          mask: false,
          scrollInput: false
        })
      });

    $(this)
      .find('[data-form-control="time"]')
      .each(function () {
        $(this).datetimepicker({
          format: this.dataset.dateFormat,
          datepicker: false,
          timepicker: true,
          mask: false,
          scrollInput: false
        })
      });

    $(this)
      .find('[data-form-control="datetime"]')
      .each(
        function () {
          $(this).datetimepicker({
            format: this.dataset.dateFormat,
            datepicker: true,
            timepicker: true,
            mask: false,
            scrollInput: false
          })
        });
  }

  disconnectedCallback() {
    $(this)
    .find('[data-form-control="date"],[data-form-control="time"],[data-form-control="datetime"]')
    .datetimepicker('destroy');
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-datetime', DateTime);
});
