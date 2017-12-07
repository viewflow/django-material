import {autoInit, base, select} from 'material-components-web';


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

export class DMCSelect extends base.MDCComponent {
  static attachTo(root) {
    return new DMCSelect(root, new base.MDCFoundation());
  }

  initialize() {
    this.customSelect_ = new MDCSelect(this.root_.querySelector('.mdc-select[role="listbox"]'));
    this.nativeSelect_ = this.root_.querySelector('select.mdc-select');
    this.changeHandler = ({type}) => {
      let changedSelect;
      let selectToUpdate;

      if (type === 'MDCSelect:change') {
        changedSelect = this.customSelect_;
        selectToUpdate = this.nativeSelect_;
      } else {
        changedSelect = this.nativeSelect_;
        selectToUpdate = this.customSelect_;
      }
      selectToUpdate.selectedIndex = changedSelect.selectedIndex;
    };
    this.customSelect_.listen('MDCSelect:change', this.changeHandler);
    this.nativeSelect_.addEventListener('change', this.changeHandler);
  }

  destroy() {
    if (this.customSelect_) {
      this.customSelect_.destroy();
    }
    if (this.nativeSelect_) {
      this.nativeSelect_.removeEventListener('change', this.changeHandler);
    }
  }
}

autoInit.register('DMCSelect', DMCSelect);
