import {Controller} from 'stimulus';
import {formField} from 'material-components-web';


export default class extends Controller {
  connect() {
    this._mdcFormField = new formField.MDCFormField(this.element);
  }

  disconnect() {
    this._mdcFormField.destroy();
  }
}
