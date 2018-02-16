/* eslint-env browser */

import {Controller} from 'stimulus';
import Turbolinks from 'turbolinks';

export default class extends Controller {
  connect() {
    this.element.addEventListener('submit', this.onSubmit);
    this.element.querySelectorAll('button[type=submit]').forEach(
      (button) => {
        button.addEventListener('click', this.onButtonClick);
      }
    );
  }

  disconnect() {
    this.element.querySelectorAll('button[type=submit]').forEach(
      (button) => {
        button.removeEventListener('click', this.onButtonClick);
      }
    );
  }

  onButtonClick = (event) => {
    if (!Turbolinks) {
      return true;
    } else {
      event.preventDefault();
      event.target.classList.add('dmc-action-button--active');
      this.element.querySelectorAll('button').forEach(
        (button) => button.disabled=true
      );
      if (this.element.method == 'post') {
        this._performPost();
      } else {
        this._performGet();
      }
    }
  }

  _performPost() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.search, true);
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
      this.element.querySelectorAll('button').forEach(
        (button) => button.disabled=false
      );

      let snackbarEvent = new CustomEvent('dmc-snackbar:show', {
        'detail': {message: 'Request error'},
      });
      window.dispatchEvent(snackbarEvent);
    };

    Turbolinks.controller.adapter.showProgressBarAfterDelay();
    xhr.send(new FormData(this.element));
  }

  _performGet() {
    const formData = Array.from(
      new FormData(this.element).entries(),
      (entry) => entry.map(encodeURIComponent).join('=')
    ).join('&');

    Turbolinks.visit(
      this.element.action +
        (this.element.action.indexOf('?') == -1 ? '?' : '&') +
        formData
    );
  }
}
