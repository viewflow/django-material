import {Controller} from 'stimulus';

export default class extends Controller {
  connect() {
    const navItems = [].slice.call(
      this.element.querySelectorAll('.mdc-list-item')
    ).filter(
      (node) => window.location.pathname.startsWith(node.pathname)
    );

    navItems.sort((a, b) => b.pathname.length - a.pathname.length);

    if (navItems.length) {
      navItems[0].classList.add('mdc-list-item--selected');
    }
  }
}
