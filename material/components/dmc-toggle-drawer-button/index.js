/* eslint-env browser */

import {Controller} from 'stimulus';

export default class extends Controller {
  connect() {
    this._drawerEl = document.getElementById(this.element.dataset.toggleDrawerId);
    this.element.addEventListener('click', this.onToggleDrawerClick);
  }

  onToggleDrawerClick = (event) => {
    event.preventDefault();
    const drawerController = this.getDrawerController();
    if (drawerController) {
      drawerController.open = !drawerController.open;
    }
  }

  getDrawerController() {
    return this.application.getControllerForElementAndIdentifier(this._drawerEl, 'dmc-drawer');
  }
}
