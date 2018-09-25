class Sidenav extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    $('.sidenav').sidenav();
    $(document).activeNavigation('#slide-out');
    $('#slide-out').perfectScrollbar();

    $(document).on('turbolinks:before-render', function (event) {
      $(event.originalEvent.data.newBody).activeNavigation('#slide-out')
    })
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-sidenav', Sidenav);
});
