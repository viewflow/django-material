/* eslint-env browser */

import {Controller} from 'stimulus';
import Turbolinks from 'turbolinks';

export default class extends Controller {
  connect() {
    window.addEventListener('turbolinks:request-end', this.onRequestEnd);
  }

  disconnect() {
    window.removeEventListener('turbolinks:request-end', this.onRequestEnd);
  }

  onRequestEnd = (event) => {
    if (event.data.xhr.status>=400) {
      Turbolinks.controller.disable();
    }
  }
}
