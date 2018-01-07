class DMCProfilePage extends mdc.base.MDCComponent {
  static attachTo(root) {
    return new DMCProfilePage(root, new mdc.base.MDCFoundation());
  }

  initialize() {
    // TODO
    alert('1');
  }
}

dmc.register('DMCProfilePage', DMCProfilePage);
