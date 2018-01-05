import {base} from 'material-components-web';
import {register} from 'django-material-registry';


export class DMCProfilePage extends base.MDCComponent {
  static attachTo(root) {
    return new DMCProfilePage(root, new base.MDCFoundation());
  }

  initialize() {
    // TODO
    alert('1');
  }
}

register('DMCProfilePage', DMCProfilePage);
