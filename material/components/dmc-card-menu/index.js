/* eslint-env browser */

import {Controller} from 'stimulus';
import {menu} from 'material-components-web';
import Turbolinks from 'turbolinks';

export default class extends Controller {
  static targets = ['menu'];

  connect() {
    this.menu = new menu.MDCMenu(this.menuTarget);
    this.menuTarget.addEventListener('MDCMenu:selected', this.menuSelectedHandler);
  }

  disconnect() {
    this.menu.destroy();
  }

  toggleMenu() {
    this.menu.open = !this.menu.open;
  }

  menuSelectedHandler = (event) => {
    let itemData = event.detail.item.dataset;
    if (itemData.dmcMenuHref) {
        if (Turbolinks) {
          Turbolinks.visit(itemData.dmcMenuHref);
        } else {
          window.location = itemData.dmcMenuHref;
        }
    }
  }
}
