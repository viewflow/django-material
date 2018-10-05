class DataTable extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    var config = JSON.parse(this.getAttribute('config'));
    config['ajax']['data'] = function(data) {
      var keys = Object.keys(data);
      for(var i=0; i<=keys.length; i++) {
        var key = keys[i],
            value = data[key];
        delete data[key];
        data['datatable-' + key] = value;
      }
    };
    config['ajax']['beforeSend'] = function(request) {
      request.setRequestHeader("datatable", true);
    };

    this._datatable = $(this).find('table').DataTable(config);
    new $.fn.dataTable.FixedHeader(this._datatable);

  }

  disconnectedCallback() {
    this._datatable.destroy();
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-datatable', DataTable);
});
