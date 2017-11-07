import {autoInit, base} from 'material-components-web';


export class DMCActiveNavFoundation extends base.MDCFoundation {
  init() {
  }

  destroy() {
  }
}


export class DMCActiveNav extends base.MDCComponent {
  static attachTo(root) {
    return new DMCActiveNav(root);
  }

  getDefaultFoundation() {
    return new DMCActiveNavFoundation({
    })
  }
}

autoInit.register('DMCActiveNav', DMCActiveNav);
