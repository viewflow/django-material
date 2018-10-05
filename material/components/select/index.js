class Select extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    $(this)
      .find('select')
      .not('.disabled')
      .not('.material-ignore')
      .not('.browser-default')
      .formSelect();
  }

  disconnectedCallback() {
    $(this)
    .find('select')
    .not('.disabled')
    .not('.material-ignore')
    .not('.browser-default')
    .formSelect('destroy');
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-select', Select);
});
