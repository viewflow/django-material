import {Controller} from 'stimulus';
import {select} from 'material-components-web';


export default class extends Controller {
  initialize() {
    this._selectEl = this.element.querySelector('.dmc-select-field');
  }

  connect() {
    this._mdcSelect = new select.MDCSelect(this._selectEl);
  }

  disconnect() {
    this._mdcSelect.destroy();
  }
}
