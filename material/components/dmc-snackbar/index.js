/* eslint-env browser */

import {Controller} from 'stimulus';
import {snackbar} from 'material-components-web';
import Turbolinks from 'turbolinks';

export default class extends Controller {
  static targets = ['text']

  connect() {
    this.snackbar = snackbar.MDCSnackbar.attachTo(this.element);
    window.addEventListener('dmc-snackbar:show', this.showSnackbar, false);
    this.showInitialSnackbar();
  }

  disconnect() {
    this.snackbar.destroy();
    window.removeEventListener('dmc-snackbar:show', this.showSnackbar);
  }

  showSnackbar = (event) => {
    this.snackbar.show(event.detail);
  }

  showInitialSnackbar() {
    let actionText;
    let actionHandler;

    const message = Array.prototype.filter.call(this.textTarget.childNodes, (child) => {
      return child.nodeType === Node.TEXT_NODE;
    }).map((child) => {
      return child.textContent.trim();
    }).join(' ');

    const link = this.textTarget.querySelector('a');
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
        this.snackbar.show({
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
