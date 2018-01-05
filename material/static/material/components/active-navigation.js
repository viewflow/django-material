import {base} from 'material-components-web';
import {register} from 'django-material-registry';


class DMCActiveNav extends base.MDCComponent {
  static attachTo(root) {
    return new DMCActiveNav(root, new base.MDCFoundation());
  }

  initialize() {
    const navItems = [].slice.call(
      this.root_.querySelectorAll('.mdc-list-item')
    ).filter(
      (node) => window.location.pathname.startsWith(node.pathname)
    );

    navItems.sort((a, b) => b.pathname.length - a.pathname.length);

    if (navItems.length) {
      navItems[0].classList.add('mdc-permanent-drawer--selected');
    }
  }
}

register('DMCActiveNav', DMCActiveNav);
