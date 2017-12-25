import {autoInit, menu, base} from 'material-components-web';


export class DMCActionMenu extends base.MDCComponent {
  static attachTo(root) {
    return new DMCActionMenu(root, new base.MDCFoundation());
  }

  initialize() {
    this.menu_ = new menu.MDCSimpleMenu(this.root_.querySelector('.mdc-simple-menu'));
    this.trigger_ = this.root_.querySelector('.dmc-list__menu-trigger');
    this.onClick = (event) => {
      this.menu_.open = !this.menu_.open;
    };
    this.trigger_.addEventListener('click', this.onClick);
  }

  destroy() {
    this.root_.removeEventListener('click', this.onClick);
  }
}

autoInit.register('DMCActionMenu', DMCActionMenu);
