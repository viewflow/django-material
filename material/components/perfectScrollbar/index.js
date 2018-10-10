class PerfectScrollbar extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    $(this).parent().perfectScrollbar()
  }

  disconnectedCallback() {
    $(this).parent().perfectScrollbar('destroy');
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-scrollbar', PerfectScrollbar);
});
