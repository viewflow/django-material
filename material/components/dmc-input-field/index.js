import {Controller} from 'stimulus';
import {textField} from 'material-components-web';


export default class extends Controller {
  connect() {
    this._mdcTextField = new textField.MDCTextField(this.element);
  }

  disconnect() {
    this._mdcTextField.destroy();
  }
}
