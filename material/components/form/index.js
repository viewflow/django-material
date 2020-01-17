/* eslint-env browser */
/* global $, Turbolinks */

class Form extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this._clickedButton = null;
    this._formEl = this.querySelector('form');
    this._formEl.addEventListener('submit', this.onSubmit);
    this.querySelectorAll('button[type=submit]').forEach(
      (button) => button.addEventListener('click', this.onClick)
    );
  }

  disconnectedCallback() {
    this._formEl.removeEventListener('submit', this.onSubmit);
    this.querySelectorAll('button[type=submit]').forEach(
      (button) => button.removeEventListener('click', this.onClick)
    );
  }

  onClick = (event) => {
    this._clickedButton = event.target;
  }

  onSubmit = (event) => {
    event.preventDefault();
    this.querySelectorAll('button').forEach(
      (button) => button.disabled=true
    );

    if (this._formEl.method == 'post') {
      this._performPost(event);
    } else {
      this._performGet(event);
    }
  }

  _performPost = (event) => {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.search || '.', true);
    xhr.setRequestHeader('Turbolinks-Referrer', window.location);
    xhr.onload = (event) => {
      let location = xhr.getResponseHeader('turbolinks-location');
      let snapshot = Turbolinks.Snapshot.wrap(xhr.response);

      if (!location) {
        location = window.location.href;
      }

      Turbolinks.controller.adapter.hideProgressBar();
      Turbolinks.controller.cache.put(location, snapshot);
      Turbolinks.visit(location, {action: 'restore'});
      Turbolinks.clearCache();

      if (xhr.status > 299) {
        Turbolinks.controller.disable();
      }
    };

    xhr.onerror = (event) => {
      Turbolinks.controller.adapter.hideProgressBar();
      this.querySelectorAll('button').forEach(
        (button) => button.disabled=false
      );

      let snackbarEvent = new CustomEvent('dmc-snackbar:show', {
        'detail': {message: 'Request error'},
      });
      window.dispatchEvent(snackbarEvent);
    };

    Turbolinks.controller.adapter.showProgressBarAfterDelay();

    let formData = new FormData(this._formEl);
    if (this._clickedButton) {
      if (this._clickedButton.name) {
        formData.append(this._clickedButton.name, this._clickedButton.value);
      }
      this._clickedButton = null;
    }
    xhr.send(formData);
  }

  _performGet = (event) => {
    Turbolinks.visit(
      this.action +
        (this.action.indexOf('?') == -1 ? '?' : '&') +
        $(this._formEl).serialize()
    );
  }

  get action() {
    const action = this._formEl.getAttribute('action');
    if (!action) {
      return window.location.href;
    }
    return action;
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-form', Form);
});
