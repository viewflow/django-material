class DMCActionMenu extends mdc.base.MDCComponent {
  static attachTo(root) {
    return new DMCActionMenu(root, new mdc.base.MDCFoundation());
  }

  initialize() {
    this.menuEl_ = this.root_.querySelector('.mdc-menu');
    this.menu_ = new mdc.menu.MDCMenu(this.menuEl_);
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

    this.trigger_ = this.root_.querySelector('button.mdc-button');
    this.onClick = (event) => {
      this.menu_.open = !this.menu_.open;
    };
    this.trigger_.addEventListener('click', this.onClick);
  }

  destroy() {
    this.root_.removeEventListener('click', this.onClick);
  }
}

dmc.register('DMCActionMenu', DMCActionMenu);
