/* eslint-env browser */

import {Controller} from 'stimulus';
import {snackbar} from 'material-components-web';
import Turbolinks from 'turbolinks';

export default class extends Controller {
  initialize() {
    this._textEl = this.element.querySelector('.mdc-snackbar__text');
  }

  connect() {
    this._mdcSnackbar = snackbar.MDCSnackbar.attachTo(this.element);
    window.addEventListener('dmc-snackbar:show', this.onShowSnackbarEvent, false);
    this._showInitialSnackbar();
  }

  disconnect() {
    this._mdcSnackbar.destroy();
    window.removeEventListener('dmc-snackbar:show', this.onShowSnackbarEvent);
  }

  onShowSnackbarEvent = (event) => {
    this._mdcSnackbar.show(event.detail);
  }

  _showInitialSnackbar() {
    let actionText;
    let actionHandler;

    const message = Array.prototype.filter.call(this._textEl.childNodes, (child) => {
      return child.nodeType === Node.TEXT_NODE;
    }).map((child) => {
      return child.textContent.trim();
    }).join(' ');

    const link = this._textEl.querySelector('a');
    if (link && window.location.href !== link.href) {
      actionText = link.textContent;
      actionHandler = () => {
        if (Turbolinks) {
          Turbolinks.visit(link.href);
        } else {
          window.location = link.href;
        }
      };
    }

    if (message) {
      setTimeout( () => {
        this._mdcSnackbar.show({
          message: message,
          actionText: actionText,
          actionHandler: actionHandler,
          multiline: true,
          timeout: 4500,
        });
      }, 300);
    }
  }
}
