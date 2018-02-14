import {Controller} from 'stimulus';

export default class extends Controller {
  connect() {
    this.drawer = document.getElementById(this.element.dataset.toggleDrawerId);
  }

  toggleDrawer(event) {
    event.preventDefault();
    const drawerController = this.getDrawerController();
    if (drawerController) {
      drawerController.open = !drawerController.open;
    }
  }

  getDrawerController() {
    return this.application.getControllerForElementAndIdentifier(this.drawer, 'dmc-drawer');
  }
}
