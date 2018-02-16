/* eslint-env browser */

import {Controller} from 'stimulus';
import {drawer} from 'material-components-web';

export default class extends Controller {
  initialize() {
    this._reconcileDrawerFrame = 0;
    this._mdcTemporalDrawer = null;
    this._mdcPersistentDrawer = null;
    this._toggleMenuEl = this.element.querySelector('.dmc-drawer-header__menu-button');
  }

  connect() {
    window.addEventListener('resize', this.onWindowResize);
    this._toggleMenuEl.addEventListener('click', this.onToggleMenuClick);
    this.reconcileDrawer();
  }

  disconnect() {
    window.removeEventListener('resize', this.onWindowResize);
    if (this._mdcTemporalDrawer) {
      this._mdcTemporalDrawer.destroy();
    }
    if (this._mdcPersistentDrawer) {
      this._mdcPersistentDrawer.destroy();
    }
  }

  onWindowResize = () => {
    cancelAnimationFrame(this._reconcileDrawerFrame);
    this._reconcileDrawerFrame = requestAnimationFrame(() => this.reconcileDrawer());
  }

  onToggleMenuClick = (event) => {
    event.preventDefault();
    this.element.classList.toggle('dmc-drawer--secondary-content-shown');
  }

  get open() {
    if (this._mdcPersistentDrawer) {
      return this._mdcPersistentDrawer.open;
    } else {
      return this._mdcTemporalDrawer .open;
    }
  }

  set open(value) {
    if (this._mdcPersistentDrawer) {
      sessionStorage.setItem('dmc_site_drawer_state', value?'open':'closed');
      return this._mdcPersistentDrawer.open = value;
    } else {
      return this._mdcTemporalDrawer .open = value;
    }
  }

  reconcileDrawer() {
    const rootClasses = this.element.classList;
    if (
      window.innerWidth < 992 &&
        (!rootClasses.contains('mdc-drawer--temporary') ||
         this._mdcTemporalDrawer === null)
    ) {
      if (this._mdcTemporalDrawer) {
        this._mdcTemporalDrawer.destroy();
        this._mdcTemporalDrawer = null;
      }
      this.element.classList.remove('mdc-drawer--persistent', 'mdc-drawer--open');
      this.element.classList.add('mdc-drawer--temporary');
      this._mdcTemporalDrawer = new drawer.MDCTemporaryDrawer(this.element);
    } else if (
      window.innerWidth >= 992 &&
        (!rootClasses.contains('mdc-drawer--persistent') ||
         this._mdcPersistentDrawer === null)
    ) {
      if (this._mdcTemporalDrawer) {
        this._mdcTemporalDrawer.destroy();
        this._mdcTemporalDrawer = null;
      }
      this.element.classList.remove('mdc-drawer--temporary');
      this.element.classList.add('mdc-drawer--persistent');
      this.element.classList.toggle(
        'mdc-drawer--open',
        sessionStorage.getItem('dmc_site_drawer_state') != 'closed'
      );
      this._mdcPersistentDrawer = new drawer.MDCPersistentDrawer(this.element);
    }
  }
}
