import {Controller} from 'stimulus';
import {checkbox} from 'material-components-web';


export default class extends Controller {
  connect() {
    this._mdcCheckbox = new checkbox.MDCCheckbox(this.element);
  }

  disconnect() {
    this._mdcCheckbox.destroy();
  }
}
