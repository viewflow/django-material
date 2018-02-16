/* eslint-env browser */

import {Controller} from 'stimulus';
import {menu} from 'material-components-web';
import Turbolinks from 'turbolinks';

export default class extends Controller {
  initialize() {
    this._menuEl = this.element.querySelector('.mdc-menu');
    this._triggerEl = this.element.querySelector('.dmc-list__menu-trigger');
  }

  connect() {
    this._mdcMenu = new menu.MDCMenu(this._menuEl);
    this._menuEl.addEventListener('MDCMenu:selected', this.onMenuSelect);
    this._triggerEl.addEventListener('click', this.onToggleMenu);
  }

  disconnect() {
    this._mdcMenu.destroy();
    this._triggerEl.removeEventListener('click', this.onToggleMenu);
  }

  onToggleMenu = () => {
    this._mdcMenu.open = !this._mdcMenu.open;
  }

  onMenuSelect = (event) => {
    let itemData = event.detail.item.dataset;
    if (itemData.dmcCardMenuHref) {
        if (Turbolinks) {
          Turbolinks.visit(itemData.dmcCardMenuHref);
        } else {
          window.location = itemData.dmcCardMenuHref;
        }
    }
  }
}
