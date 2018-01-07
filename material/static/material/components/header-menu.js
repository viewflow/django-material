class DMCHeaderMenu extends mdc.base.MDCComponent {
  static attachTo(root) {
    return new DMCHeaderMenu(root, new mdc.base.MDCFoundation());
  }

  initialize() {
    this.menuContainer_ = document.getElementById(this.root_.dataset.toggleMenu);
    this.trigger_ = this.root_.querySelector('button.mdc-button');
    this.onClick = (event) => {
      event.stopPropagation();
      this.menuContainer_.classList.toggle('dmc-header-secondary-shown');
      this.trigger_.classList.toggle('dmc-header-secondary-shown');
    };
    this.trigger_.addEventListener('click', this.onClick);
  }

  destroy() {
    this.root_.removeEventListener('click', this.onClick);
  }
}

dmc.register('DMCHeaderMenu', DMCHeaderMenu);
