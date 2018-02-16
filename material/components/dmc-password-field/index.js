import {Controller} from 'stimulus';
import {textField} from 'material-components-web';


export default class extends Controller {
  initialize() {
    this._inputEl = this.element.querySelector('.dmc-text-field__input');
    this._toggleEl = this.element.querySelector('.dmc-password-field__toggle');
  }

  connect() {
    this._mdcTextField = new textField.MDCTextField(this.element);
    this._toggleEl.addEventListener('click', this.onToggle);
  }

  disconnect() {
    this._mdcTextField.destroy();
    this._toggleEl.removeEventListener('click', this.onToggle);
  }

  onToggle = (event) => {
    event.preventDefault();
    if (this._inputEl.type === 'password') {
      this._inputEl.type = 'text';
      this._toggleEl.text = 'visibility_off';
      this._inputEl.selectionStart = this._inputEl.selectionEnd = this._inputEl.value.length;
      this._inputEl.focus();
    } else {
      this._inputEl.type = 'password';
      this._toggleEl.text = 'visibility';
    }
  }
}
