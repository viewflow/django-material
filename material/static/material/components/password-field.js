import {autoInit, base, textField} from 'material-components-web';


export class DMCPasswordField extends base.MDCComponent {
  static attachTo(root) {
    return new DMCPasswordField(root, new base.MDCFoundation());
  }

  initialize() {
    this.textField_ = new textField.MDCTextField(this.root_)
    this.input_ = this.root_.querySelector('.dmc-text-field__input')
    this.toggle_ = this.root_.querySelector('.dmc-password-field__toggle')

    this.onToggle = (event) => {
      event.preventDefault()
      if(this.input_.type === "password") {
        this.input_.type = "text";
        this.toggle_.text = "visibility_off"
      } else {
        this.input_.type = "password";
        this.toggle_.text = "visibility"
      }
      if(event.type !== "keypress") {
        this.input_.selectionStart = this.input_.selectionEnd = this.input_.value.length
        this.input_.focus()
      }
    }
    this.toggle_.addEventListener('click', this.onToggle)
    this.toggle_.addEventListener('keypress', this.onToggle)
  }

  destroy() {
    if(this.textField_) {
      this.textField_.destroy()
    }
    this.toggle_.removeEventListener('click', this.onToggle)
    this.toggle_.removeEventListener('keypress', this.onToggle)
  }
}

autoInit.register('DMCPasswordField', DMCPasswordField);
