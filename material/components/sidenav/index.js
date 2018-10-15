class Sidenav extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    $(this).find('.sidenav').sidenav();
    $(document).activeNavigation('#slide-out');
    $('#slide-out').perfectScrollbar();
  }

  disconnectedCallback() {
    $(this).find('.sidenav').sidenav('destroy');
    $('#slide-out').perfectScrollbar('destroy');
  }

}

window.addEventListener('load', () => {
  window.customElements.define('dmc-sidenav', Sidenav);
});
