/* eslint-env browser */
/* global $, M */

class Textarea extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    M.textareaAutoResize($(this).find('textarea'));
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-textarea', Textarea);
});
