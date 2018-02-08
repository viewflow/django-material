class DMCResponsiveDrawer extends mdc.base.MDCComponent {
  static attachTo(root) {
    return new DMCResponsiveDrawer(root, new mdc.base.MDCFoundation());
  }

  constructor(...args) {
    super(...args);
  }

  initialize() {
    this.reconcileDrawer_ = 0;
    this.temporalDrawer_ = null;
    this.persistentDrawer_ = null;

    this.onResize = () => {
      cancelAnimationFrame(this.reconcileDrawer_);
      this.reconcileDrawer_ = requestAnimationFrame(() => this.reconcileDrawer());
    };

    window.addEventListener('resize', this.onResize);
    this.reconcileDrawer();
  }

  destroy() {
    window.removeEventListener('resize', this.onResize);
    if (this.temporalDrawer_) {
      this.temporalDrawer_.destroy();
    }
    if (this.persistentDrawer_) {
      this.persistentDrawer_.destroy();
    }
  }

  reconcileDrawer() {
    const rootClasses = this.root_.classList;
    if (
      window.innerWidth < 992 &&
        (!rootClasses.contains('mdc-drawer--temporary') ||
         this.temporalDrawer_ === null)
    ) {
      if (this.persistentDrawer_) {
        this.persistentDrawer_.destroy();
        this.persistentDrawer_ = null;
      }
      // this.root_.classList.remove('mdc-persistent-drawer', 'mdc-persistent-drawer--open');
      this.root_.classList.add('mdc-drawer--temporary');
      this.temporalDrawer_ = new mdc.drawer.MDCTemporaryDrawer(this.root_);
      // this.drawer_.removeEventListener('click', this.temporalDrawer_.foundation_.drawerClickHandler_);
    } else if (
      window.innerWidth >= 992 &&
        (!rootClasses.contains('mdc-drawer--persistent') ||
         this.persistentDrawer_ === null)
    ) {
      if (this.temporalDrawer_) {
        this.temporalDrawer_.destroy();
        this.temporalDrawer_ = null;
      }
      this.root_.classList.remove('mdc-drawer--temporary');
      this.root_.classList.add('mdc-drawer--persistent');
      if (sessionStorage.getItem('dmc_site_drawer_state') != 'closed') {
        this.root_.classList.add('mdc-drawer--open');
      } else {
        this.root_.classList.remove('mdc-drawer--open');
      }
      this.persistentDrawer_ = new mdc.drawer.MDCPersistentDrawer(this.root_);
      // this.drawer_.removeEventListener('click', this.persistentDrawer_.foundation_.drawerClickHandler_);
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
      // TODO cookie ??
      sessionStorage.setItem('dmc_site_drawer_state', value?'open':'closed');
      return this.persistentDrawer_.open = value;
    } else {
      return this.temporalDrawer_ .open = value;
    }
  }
}

dmc.register('DMCResponsiveDrawer', DMCResponsiveDrawer);
