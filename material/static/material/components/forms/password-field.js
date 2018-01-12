class DMCPasswordField extends mdc.base.MDCComponent {
  static attachTo(root) {
    return new DMCPasswordField(root, new mdc.base.MDCFoundation());
  }

  initialize() {
    this.textField_ = new mdc.textField.MDCTextField(this.root_);
    this.input_ = this.root_.querySelector('.dmc-text-field__input');
    this.toggle_ = this.root_.querySelector('.dmc-password-field__toggle');

    this.onToggle = (event) => {
      event.preventDefault();
      if (this.input_.type === 'password') {
        this.input_.type = 'text';
        this.toggle_.text = 'visibility_off';
      } else {
        this.input_.type = 'password';
        this.toggle_.text = 'visibility';
      }

      this.input_.selectionStart = this.input_.selectionEnd = this.input_.value.length;
      this.input_.focus();
    };
    this.toggle_.addEventListener('click', this.onToggle);
  }

  destroy() {
    if (this.textField_) {
      this.textField_.destroy();
    }
    this.toggle_.removeEventListener('click', this.onToggle);
  }
}

dmc.register('DMCPasswordField', DMCPasswordField);
