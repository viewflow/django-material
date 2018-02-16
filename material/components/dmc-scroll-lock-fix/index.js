/* eslint-env browser */

import {Controller} from 'stimulus';


export default class extends Controller {
  initialize() {
    this._reconcileBodyFrame = 0;
    this._clientWidth = document.body.clientWidth;
    this._gap = 0;
  }

  connect() {
    window.addEventListener('resize', this.onResize);
    this._observer = new MutationObserver(this.onBodyChanged);
    this._observer.observe(document.body, {attributes: true, attributeFilter: ['class']});
  }

  disconnect() {
    window.removeEventListener('resize', this.onResize);
    cancelAnimationFrame(this._reconcileBodyFrame);
    this._observer.disconnect();
  }

  onResize = () => {
    if (!document.body.style.width) {
      this._clientWidth = document.body.clientWidth;
    } else {
      cancelAnimationFrame(this._reconcileBodyFrame);
      this._reconcileBodyFrame = requestAnimationFrame(() => {
        document.body.style.width = (window.innerWidth - this._gap) + 'px';
      });
    }
  }

  onBodyChanged = (mutationsList) => {
    let overflow = window.getComputedStyle(document.body).overflow;

    if (overflow == 'hidden') {
      this._gap = window.innerWidth - this._clientWidth;
      document.body.style.width = this._clientWidth + 'px';
    } else {
      document.body.style.removeProperty('width');
      this._clientWidth = document.body.clientWidth;
    }
  }
}
