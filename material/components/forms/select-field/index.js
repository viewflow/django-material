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
  connect() {
    this.customSelect = new MDCSelect(this.element.querySelector('.mdc-select[role="listbox"]'));
    this.nativeSelect = this.element.querySelector('.dmc-select-field__native');
    this.customSelect.listen('MDCSelect:change', this.changeHandler);
    this.nativeSelect.addEventListener('change', this.changeHandler);
  }

  disconnect() {
    this.customSelect.destroy();
    this.nativeSelect.removeEventListener('change', this.changeHandler);
  }

  changeHandler = ({type}) => {
    let changedSelect;
    let selectToUpdate;

    if (type === 'MDCSelect:change') {
      changedSelect = this.customSelect;
      selectToUpdate = this.nativeSelect;
    } else {
      changedSelect = this.nativeSelect;
      selectToUpdate = this.customSelect;
    }
    selectToUpdate.selectedIndex = changedSelect.selectedIndex;
  };
}
