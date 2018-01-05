import * as mdc from 'material-components-web';
import Turbolinks from 'turbolinks';

const registry = Object.create(null);
const CONSOLE_WARN = console.warn.bind(console);
let pageLoaded = false;

export function autoInit() {
  window.addEventListener('turbolinks:load', onLoad);
  window.addEventListener('turbolinks:before-render', onBeforeRender);
  window.addEventListener('turbolinks:request-end', onRequestEnd);
  initComponents();
};

export function initComponents(root = document, warn = CONSOLE_WARN, allowUnknown=false) {
  const nodes = root.querySelectorAll('[data-mdc-auto-init]');
  for (let i = 0, node; (node = nodes[i]); i++) {
    const ctorName = node.dataset.mdcAutoInit;
    if (!ctorName) {
      throw new Error('(mdc-auto-init) Constructor name must be given.');
    }
    const Ctor = registry[ctorName];
    if (typeof Ctor !== 'function') {
      if (!allowUnknown) {
        throw new Error(
          `(mdc-auto-init) Could not find constructor in registry for ${ctorName}`);
      }
      continue;
    }
    const component = Ctor.attachTo(node);
    Object.defineProperty(node, ctorName, {
      value: component,
      writable: false,
      enumerable: false,
      configurable: true,
    });
  }
}

export function register(ctorName, Ctor) {
    if (typeof Ctor !== 'function') {
      throw new Error(`(mdc-auto-init) Invalid Ctor value ${Ctor}. Expected function`);
    }
    if (registry[ctorName]) {
      warn(
        `(mdc-auto-init) Overriding registration for ${componentName} with ${Ctor}. ` +
        `Was: ${registry[componentName]}`);
    }
    registry[ctorName] = Ctor;

  if (pageLoaded) {
    // an additional script loaded after turbolinks:load,
    // components need to be initialized on the current page
    const nodes = document.querySelectorAll(`body [data-mdc-auto-init=${ctorName}]`);
    for (let i = 0, node; (node = nodes[i]); i++) {
      if (node[ctorName]) {
        console.warn(`(mdc-auto-init) Component already initialized for ${node}. Skipping...`);
        continue;
      }
      const component = Ctor.attachTo(node);
      Object.defineProperty(node, ctorName, {
        value: component,
        writable: false,
        enumerable: false,
        configurable: true,
      });
    }
  }
};

function onLoad() {
  initComponents(document.querySelector('body'), CONSOLE_WARN, true);
  pageLoaded = true;
};

function onBeforeRender() {
  pageLoaded = false;
  const nodes = document.querySelectorAll('body [data-mdc-auto-init]');
  for (let i=0; i<nodes.length; i++) {
    const node = nodes[i];
    const ctorName = node.dataset.mdcAutoInit;
    const component = node[ctorName];
    component.destroy();
  }
};

function onRequestEnd(event) {
  if (event.data.xhr.status>=400) {
    Turbolinks.controller.disable();
  }
};

export function destroy() {
  window.removeEventListener('turbolinks:load', onLoad);
  window.removeEventListener('turbolinks:before-render', onBeforeRender);
  window.removeEventListener('turbolinks:request-end', onRequestEnd);
}


register('MDCCheckbox', mdc.checkbox.MDCCheckbox);
register('MDCDialog', mdc.dialog.MDCDialog);
register('MDCPersistentDrawer', mdc.drawer.MDCPersistentDrawer);
register('MDCTemporaryDrawer', mdc.drawer.MDCTemporaryDrawer);
register('MDCFormField', mdc.formField.MDCFormField);
register('MDCRipple', mdc.ripple.MDCRipple);
register('MDCGridList', mdc.gridList.MDCGridList);
register('MDCIconToggle', mdc.iconToggle.MDCIconToggle);
register('MDCLinearProgress', mdc.linearProgress.MDCLinearProgress);
register('MDCRadio', mdc.radio.MDCRadio);
register('MDCSnackbar', mdc.snackbar.MDCSnackbar);
register('MDCTab', mdc.tabs.MDCTab);
register('MDCTabBar', mdc.tabs.MDCTabBar);
register('MDCTextField', mdc.textField.MDCTextField);
register('MDCSimpleMenu', mdc.menu.MDCSimpleMenu);
register('MDCSelect', mdc.select.MDCSelect);
register('MDCSlider', mdc.slider.MDCSlider);
register('MDCToolbar', mdc.toolbar.MDCToolbar);


function browserLoad() {
  autoInit();
  window.removeEventListener('load', browserLoad);
}
window.addEventListener('load', browserLoad);
