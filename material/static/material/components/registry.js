(function() {
  'use strict';
  let dmc = {};
  dmc.registry = Object.create(null);

  let pageLoaded = false;
  const CONSOLE_WARN = console.warn.bind(console);

  function initComponents(root = document, warn = CONSOLE_WARN, allowUnknown=false) {
    const nodes = root.querySelectorAll('[data-mdc-auto-init]');
    for (let i = 0, node; (node = nodes[i]); i++) {
      const ctorName = node.dataset.mdcAutoInit;
      if (!ctorName) {
        throw new Error('(mdc-auto-init) Constructor name must be given.');
      }
      const Ctor = dmc.registry[ctorName];
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

  function onLoad() {
    initComponents(document.querySelector('body'), CONSOLE_WARN, true);
    pageLoaded = true;
  }

  function onBeforeRender() {
    pageLoaded = false;
    const nodes = document.querySelectorAll('body [data-mdc-auto-init]');
    for (let i=0; i<nodes.length; i++) {
      const node = nodes[i];
      const ctorName = node.dataset.mdcAutoInit;
      const component = node[ctorName];
      component.destroy();
    }
  }

  function onRequestEnd(event) {
    if (event.data.xhr.status>=400) {
      Turbolinks.controller.disable();
    }
  }

  dmc.register = (ctorName, Ctor) => {
    if (typeof Ctor !== 'function') {
      throw new Error(`(mdc-auto-init) Invalid Ctor value ${Ctor}. Expected function`);
    }
    if (dmc.registry[ctorName]) {
      warn(
        `(mdc-auto-init) Overriding registration for ${componentName} with ${Ctor}. ` +
        `Was: ${registry[componentName]}`);
    }
    dmc.registry[ctorName] = Ctor;

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

  dmc.autoInit = () => {
    window.addEventListener('turbolinks:load', onLoad);
    window.addEventListener('turbolinks:before-render', onBeforeRender);
    window.addEventListener('turbolinks:request-end', onRequestEnd);
    initComponents();
  };

  dmc.destroy = () => {
    window.removeEventListener('turbolinks:load', onLoad);
    window.removeEventListener('turbolinks:before-render', onBeforeRender);
    window.removeEventListener('turbolinks:request-end', onRequestEnd);
  };


  dmc.register('MDCCheckbox', mdc.checkbox.MDCCheckbox);
  dmc.register('MDCDialog', mdc.dialog.MDCDialog);
  dmc.register('MDCPersistentDrawer', mdc.drawer.MDCPersistentDrawer);
  dmc.register('MDCTemporaryDrawer', mdc.drawer.MDCTemporaryDrawer);
  dmc.register('MDCFormField', mdc.formField.MDCFormField);
  dmc.register('MDCRipple', mdc.ripple.MDCRipple);
  dmc.register('MDCGridList', mdc.gridList.MDCGridList);
  dmc.register('MDCIconToggle', mdc.iconToggle.MDCIconToggle);
  dmc.register('MDCLinearProgress', mdc.linearProgress.MDCLinearProgress);
  dmc.register('MDCRadio', mdc.radio.MDCRadio);
  dmc.register('MDCSnackbar', mdc.snackbar.MDCSnackbar);
  dmc.register('MDCTab', mdc.tabs.MDCTab);
  dmc.register('MDCTabBar', mdc.tabs.MDCTabBar);
  dmc.register('MDCTextField', mdc.textField.MDCTextField);
  dmc.register('MDCSimpleMenu', mdc.menu.MDCSimpleMenu);
  dmc.register('MDCSelect', mdc.select.MDCSelect);
  dmc.register('MDCSlider', mdc.slider.MDCSlider);
  dmc.register('MDCToolbar', mdc.toolbar.MDCToolbar);

  // Module definition
  if (typeof define !== 'undefined' && define.amd) {
    define(() => dmc);
  } else if (typeof exports !== 'undefined') {
    exports.dmc = dmc;
  } else if (typeof navigator !== 'undefined') {
    function browserLoad() {
      dmc.autoInit();
      window.removeEventListener('load', browserLoad);
    }
    window.addEventListener('load', browserLoad);
    window.dmc = dmc;
  } else if (typeof module !== 'undefined') {
    module.exports = dmc;
  }
})();
