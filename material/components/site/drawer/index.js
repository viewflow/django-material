import {Controller} from 'stimulus';
import {drawer} from 'material-components-web';

export default class extends Controller {
  initialize() {
    this.reconcileDrawer_ = 0;
    this.temporalDrawer_ = null;
    this.persistentDrawer_ = null;
  }

  connect() {
    this.resizeHandler = () => this.handleResize();
    window.addEventListener('resize', this.resizeHandler);
    this.reconcileDrawer();
  }

  disconnect() {
    window.removeEventListener('resize', this.resizeHandler);
    if (this.temporalDrawer_) {
      this.temporalDrawer_.destroy();
    }
    if (this.persistentDrawer_) {
      this.persistentDrawer_.destroy();
    }
  }

  get open() {
    if (this.persistentDrawer_) {
      return this.persistentDrawer_.open;
    } else {
      return this.temporalDrawer_ .open;
    }
  }

  set open(value) {
    if (this.persistentDrawer_) {
      sessionStorage.setItem('dmc_site_drawer_state', value?'open':'closed');
      return this.persistentDrawer_.open = value;
    } else {
      return this.temporalDrawer_ .open = value;
    }
  }

  handleResize() {
    cancelAnimationFrame(this.reconcileDrawer_);
    this.reconcileDrawer_ = requestAnimationFrame(() => this.reconcileDrawer());
  }

  toggleUserMenu() {
    this.menuContainer.classList.toggle('dmc-drawer-menu--secondary-shown');
    this.element.classList.toggle('dmc-drawer-menu__secondary--shown');
  }

  reconcileDrawer() {
    const rootClasses = this.element.classList;
    if (
      window.innerWidth < 992 &&
        (!rootClasses.contains('mdc-drawer--temporary') ||
         this.temporalDrawer_ === null)
    ) {
      if (this.persistentDrawer_) {
        this.persistentDrawer_.destroy();
        this.persistentDrawer_ = null;
      }
      this.element.classList.remove('mdc-drawer--persistent', 'mdc-drawer--open');
      this.element.classList.add('mdc-drawer--temporary');
      this.temporalDrawer_ = new drawer.MDCTemporaryDrawer(this.element);
    } else if (
      window.innerWidth >= 992 &&
        (!rootClasses.contains('mdc-drawer--persistent') ||
         this.persistentDrawer_ === null)
    ) {
      if (this.temporalDrawer_) {
        this.temporalDrawer_.destroy();
        this.temporalDrawer_ = null;
      }
      this.element.classList.remove('mdc-drawer--temporary');
      this.element.classList.add('mdc-drawer--persistent');
      if (sessionStorage.getItem('dmc_site_drawer_state') != 'closed') {
        this.element.classList.add('mdc-drawer--open');
      } else {
        this.element.classList.remove('mdc-drawer--open');
      }
      this.persistentDrawer_ = new drawer.MDCPersistentDrawer(this.element);
    }
  }
}
