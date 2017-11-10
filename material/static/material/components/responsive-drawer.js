import {autoInit, base, drawer} from 'material-components-web';

// TODO cookie
// TODO open

export class DMCResponsiveDrawer extends base.MDCComponent {
  static attachTo(root) {
    return new DMCResponsiveDrawer(root, new base.MDCFoundation());
  }

  constructor(...args) {
    super(...args)
    this.reconcileDrawer_ = 0
    this.temporalDrawer_ = null
    this.persistentDrawer_ = null
  }

  initialize() {
    this.drawer_ = this.root_.querySelector('nav')
    this.header_ = this.drawer_.querySelector('header')
    this.headerContent_ = this.header_.querySelector('div')
    this.content_ = this.drawer_.querySelector('nav')

    this.onResize = () => {
      cancelAnimationFrame(this.reconcileDrawer_);
      this.reconcileDrawer_ = requestAnimationFrame(() => this.reconcileDrawer())
    }

    window.addEventListener('resize', this.onResize)
    this.reconcileDrawer()
  }

  destroy() {
    window.removeEventListener(this.onResize)
  }

  reconcileDrawer() {
    const rootClasses = this.root_.classList
    if(window.innerWidth < 992 && !rootClasses.contains('mdc-temporary-drawer')) {
      if(this.persistentDrawer_) {
        this.persistentDrawer_.destroy()
        this.persistentDrawer_ = null
      }
      this.root_.classList.remove('mdc-persistent-drawer', 'mdc-persistent-drawer--open')
      this.drawer_.classList.remove('mdc-persistent-drawer__drawer')
      this.header_.classList.remove('mdc-persistent-drawer__header')
      this.headerContent_.classList.remove('mdc-persistent-drawer__header-content')
      this.content_.classList.remove('mdc-persistent-drawer__content')


      this.root_.classList.add('mdc-temporary-drawer')
      this.drawer_.classList.add('mdc-temporary-drawer__drawer')
      this.header_.classList.add('mdc-temporary-drawer__header')
      this.headerContent_.classList.add('mdc-temporary-drawer__header-content')
      this.content_.classList.add('mdc-temporary-drawer__content')
      this.temporalDrawer_ = new drawer.MDCTemporaryDrawer(this.root_)
    } else if(window.innerWidth >= 992 && !rootClasses.contains('mdc-persistent-drawer')) {
      if(this.temporalDrawer_) {
        this.temporalDrawer_.destroy()
        this.temporalDrawer_ = null
      }
      this.root_.classList.remove('mdc-temporary-drawer')
      this.drawer_.classList.remove('mdc-temporary-drawer__drawer')
      this.header_.classList.remove('mdc-temporary-drawer__header')
      this.headerContent_.classList.remove('mdc-temporary-drawer__header-content')
      this.content_.classList.remove('mdc-temporary-drawer__content')


      this.root_.classList.add('mdc-persistent-drawer', 'mdc-persistent-drawer--open')
      this.drawer_.classList.add('mdc-persistent-drawer__drawer')
      this.header_.classList.add('mdc-persistent-drawer__header')
      this.headerContent_.classList.add('mdc-persistent-drawer__header-content')
      this.content_.classList.add('mdc-persistent-drawer__content')
      this.persistentDrawer_ = new drawer.MDCPersistentDrawer(this.root_)
    }
  }
}

autoInit.register('DMCResponsiveDrawer', DMCResponsiveDrawer);
