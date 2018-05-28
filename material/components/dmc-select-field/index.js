import {Controller} from 'stimulus';
import {select} from 'material-components-web';


export default class extends Controller {
  connect() {
    this._mdcSelect = new select.MDCSelect(this.element);
  }

  disconnect() {
    this._mdcSelect.destroy();
  }
}
