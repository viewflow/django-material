class PerfectScrollbarEl extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.scrollbar = new PerfectScrollbar($(this).parent().get(0));
  }

  disconnectedCallback() {
    this.scrollbar.destroy();
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-scrollbar', PerfectScrollbarEl);
});
