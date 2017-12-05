  import {autoInit, base, select} from 'material-components-web';


class MDCSelect extends select.MDCSelect {
  getDefaultFoundation() {
    let foundation = super.getDefaultFoundation(),
        super_setMenuStyle = foundation.setMenuStylesForOpenAtIndex_

    foundation.resize = function() {
      /* no action here */
    }

    foundation.setMenuStylesForOpenAtIndex_ = function (index) {
      super_setMenuStyle.call(foundation, index)

      const rect = foundation.adapter_.computeBoundingRect()
      foundation.adapter_.setMenuElStyle('width', `${rect.width}px`);
    }

    return foundation
  }
}

export class DMCSelect extends base.MDCComponent {
  static attachTo(root) {
    return new DMCSelect(root, new base.MDCFoundation());
  }

  initialize() {
    this.selectField_ = new MDCSelect(this.root_)
  }

  destroy() {
    if(this.selectField_) {
      this.selectField_.destroy()
    }
  }
}

autoInit.register('DMCSelect', DMCSelect);
