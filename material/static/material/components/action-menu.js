import {autoInit, menu, base} from 'material-components-web';


export class DMCActionMenu extends base.MDCComponent {
  static attachTo(root) {
    return new DMCActionMenu(root, new base.MDCFoundation());
  }

  initialize() {
    this.menuEl_ = this.root_.querySelector('.mdc-simple-menu');
    this.menu_ = new menu.MDCSimpleMenu(this.menuEl_);
    this.menuEl_.addEventListener('MDCSimpleMenu:selected', function(evt) {
      let itemData = evt.detail.item.dataset;
      if (itemData.dmcMenuHref) {
        if (window.Turbolinks) {
          Turbolinks.visit(itemData.dmcMenuHref);
        } else {
          window.location = itemData.dmcMenuHref;
        }
      }
    });

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
