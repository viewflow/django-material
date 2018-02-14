import {Controller} from 'stimulus';
import {textField} from 'material-components-web';


export default class extends Controller {
  connect() {
    this.textField_ = new textField.MDCTextField(this.element);
  }

  disconnect() {
    if (this.textField_) {
      this.textField_.destroy();
    }
  }
}
