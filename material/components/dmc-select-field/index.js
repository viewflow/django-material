import {Controller} from 'stimulus';
import {select} from 'material-components-web';

class MDCSelect extends select.MDCSelect {
  getDefaultFoundation() {
    let foundation = super.getDefaultFoundation();
    let superSetMenuStyle = foundation.setMenuStylesForOpenAtIndex_;

    foundation.resize = function() {
      /* no action here */
    };

    foundation.setMenuStylesForOpenAtIndex_ = function(index) {
      superSetMenuStyle.call(foundation, index);

      const rect = foundation.adapter_.computeBoundingRect();
      foundation.adapter_.setMenuElStyle('width', `${rect.width}px`);
    };

    return foundation;
  }
}


export default class extends Controller {
  initialize() {
    this._customSelectEl = this.element.querySelector('.mdc-select[role="listbox"]');
    this._nativeSelectEl = this.element.querySelector('.dmc-select-field__native');
  }

  connect() {
    this._mdcSelect = new MDCSelect(this._customSelectEl);
    this._mdcSelect.listen('MDCSelect:change', this.onSelectChange);
    this._nativeSelectEl.addEventListener('change', this.onSelectChange);
  }

  disconnect() {
    this._mdcSelect.destroy();
    this._nativeSelectEl.removeEventListener('change', this.onSelectChange);
  }

  onSelectChange = ({type}) => {
    let changedSelect;
    let selectToUpdate;

    if (type === 'MDCSelect:change') {
      changedSelect = this._mdcSelect;
      selectToUpdate = this._nativeSelectEl;
    } else {
      changedSelect = this._nativeSelectEl;
      selectToUpdate = this._mdcSelect;
    }
    selectToUpdate.selectedIndex = changedSelect.selectedIndex;
  };
}
