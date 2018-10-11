class Modal extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    $(this).find('.modal').modal({preventScrolling: false})
  }

  disconnectedCallback() {
    $(this).find('.modal').modal('destroy');
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-modal', Modal);
});
