class Collapsible extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    $(this).find('.collapsible').collapsible();
  }

  disconnectedCallback() {
    $(this).find('.collapsible').collapsible('destroy');
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-collapsible', Collapsible);
});
