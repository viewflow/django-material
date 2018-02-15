import {Controller} from 'stimulus';
import {textField} from 'material-components-web';


export default class extends Controller {
  static targets = ['input', 'toggle'];

  connect() {
    this.textField = new textField.MDCTextField(this.element);
  }

  disconnect() {
    this.textField.destroy();
  }

  toggle(event) {
    event.preventDefault();
    if (this.inputTarget.type === 'password') {
      this.inputTarget.type = 'text';
      this.toggleTarget.text = 'visibility_off';
    } else {
      this.inputTarget.type = 'password';
      this.toggleTarget.text = 'visibility';
    }

    this.inputTarget.selectionStart = this.inputTarget.selectionEnd = this.inputTarget.value.length;
    this.inputTarget.focus();
  }
}
