/* eslint-env browser */
/* global $ */

class Dropdown extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    $(this).find('.dropdown-button').dropdown();
  }

  disconnectedCallback() {
    $(this).find('.dropdown-button').dropdown('destroy');
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-dropdown', Dropdown);
});
