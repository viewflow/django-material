/* eslint-env browser */

import {Controller} from 'stimulus';


export default class extends Controller {
  initialize() {
    this.reconcileBody_ = 0;
    this.clientWidth_ = document.body.clientWidth;
    this.gap_ = 0;
  }

  connect() {
    window.addEventListener('resize', this.onResize);
    this.observer_ = new MutationObserver(this.onBodyChanged);
    this.observer_.observe(document.body, {attributes: true, attributeFilter: ['class']});
  }

  disconnect() {
    window.removeEventListener('resize', this.onResize);
    cancelAnimationFrame(this.reconcileBody_);
    this.observer_.disconnect();
  }

  onResize = () => {
    if (!document.body.style.width) {
      this.clientWidth_ = document.body.clientWidth;
    } else {
      cancelAnimationFrame(this.reconcileBody_);
      this.reconcileBody_ = requestAnimationFrame(() => {
        document.body.style.width = (window.innerWidth - this.gap_) + 'px';
      });
    }
  }

  onBodyChanged = (mutationsList) => {
    let overflow = window.getComputedStyle(document.body).overflow;

    if (overflow == 'hidden') {
      this.gap_ = window.innerWidth - this.clientWidth_;
      document.body.style.width = this.clientWidth_ + 'px';
    } else {
      document.body.style.removeProperty('width');
      this.clientWidth_ = document.body.clientWidth;
    }
  }
}
