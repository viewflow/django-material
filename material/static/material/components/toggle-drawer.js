import {autoInit, base} from 'material-components-web';


export class DMCToggleDrawer extends base.MDCComponent {
  static attachTo(root) {
    return new DMCToggleDrawer(root, new base.MDCFoundation());
  }

  initialize() {
    this.drawer_ = document.getElementById(this.root_.dataset.toggleDrawerId)
    this.onClick = (event) => {
      event.preventDefault()
      this.drawer_.DMCResponsiveDrawer.open = !this.drawer_.DMCResponsiveDrawer.open
    }
    this.root_.addEventListener('click', this.onClick)
  }

  destroy() {
    this.root_.removeEventListener('click', this.onClick)
  }
}

autoInit.register('DMCToggleDrawer', DMCToggleDrawer);
