(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(['exports', 'material-components-web'], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require('material-components-web'));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.mdc);
    global.activeNavigation = mod.exports;
  }
})(this, function (exports, _materialComponentsWeb) {
  'use strict';

  Object.defineProperty(exports, "__esModule", {
    value: true
  });
  exports.DMCActiveNav = undefined;

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  var _createClass = function () {
    function defineProperties(target, props) {
      for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
      }
    }

    return function (Constructor, protoProps, staticProps) {
      if (protoProps) defineProperties(Constructor.prototype, protoProps);
      if (staticProps) defineProperties(Constructor, staticProps);
      return Constructor;
    };
  }();

  function _possibleConstructorReturn(self, call) {
    if (!self) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return call && (typeof call === "object" || typeof call === "function") ? call : self;
  }

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        enumerable: false,
        writable: true,
        configurable: true
      }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
  }

  var DMCActiveNav = exports.DMCActiveNav = function (_base$MDCComponent) {
    _inherits(DMCActiveNav, _base$MDCComponent);

    function DMCActiveNav() {
      _classCallCheck(this, DMCActiveNav);

      return _possibleConstructorReturn(this, (DMCActiveNav.__proto__ || Object.getPrototypeOf(DMCActiveNav)).apply(this, arguments));
    }

    _createClass(DMCActiveNav, [{
      key: 'initialize',
      value: function initialize() {
        var navItems = [].slice.call(this.root_.querySelectorAll('.mdc-list-item')).filter(function (node) {
          return window.location.pathname.startsWith(node.pathname);
        });
        navItems.sort(function (a, b) {
          return b.pathname.length - a.pathname.length;
        });
        if (navItems.length) {
          navItems[0].classList.add('mdc-permanent-drawer--selected');
        }
      }
    }], [{
      key: 'attachTo',
      value: function attachTo(root) {
        return new DMCActiveNav(root, new _materialComponentsWeb.base.MDCFoundation());
      }
    }]);

    return DMCActiveNav;
  }(_materialComponentsWeb.base.MDCComponent);

  _materialComponentsWeb.autoInit.register('DMCActiveNav', DMCActiveNav);
});
(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(['exports', 'material-components-web', 'turbolinks'], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require('material-components-web'), require('turbolinks'));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.mdc, global.Turbolinks);
    global.djangoTurbolinks = mod.exports;
  }
})(this, function (exports, _materialComponentsWeb, _turbolinks) {
  'use strict';

  Object.defineProperty(exports, "__esModule", {
    value: true
  });
  exports.DMCTurbolinks = undefined;

  var _turbolinks2 = _interopRequireDefault(_turbolinks);

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule ? obj : {
      default: obj
    };
  }

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  var _createClass = function () {
    function defineProperties(target, props) {
      for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
      }
    }

    return function (Constructor, protoProps, staticProps) {
      if (protoProps) defineProperties(Constructor.prototype, protoProps);
      if (staticProps) defineProperties(Constructor, staticProps);
      return Constructor;
    };
  }();

  function _possibleConstructorReturn(self, call) {
    if (!self) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return call && (typeof call === "object" || typeof call === "function") ? call : self;
  }

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        enumerable: false,
        writable: true,
        configurable: true
      }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
  }

  var DMCTurbolinks = exports.DMCTurbolinks = function (_base$MDCComponent) {
    _inherits(DMCTurbolinks, _base$MDCComponent);

    function DMCTurbolinks() {
      _classCallCheck(this, DMCTurbolinks);

      return _possibleConstructorReturn(this, (DMCTurbolinks.__proto__ || Object.getPrototypeOf(DMCTurbolinks)).apply(this, arguments));
    }

    _createClass(DMCTurbolinks, [{
      key: 'initialize',
      value: function initialize() {
        this.onLoad = function () {
          window.mdc.autoInit(document.querySelector('body'));
        };

        this.onBeforeCache = function () {
          var nodes = document.querySelectorAll('body [data-mdc-auto-init]');
          for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i],
                ctorName = nodes[i].dataset.mdcAutoInit,
                component = node[ctorName];
            component.destroy();
          }
        };

        this.onRequestEnd = function (event) {
          if (event.data.xhr.status == 500) {
            _turbolinks2.default.controller.disable();
          }
        };

        window.addEventListener('turbolinks:load', this.onLoad);
        window.addEventListener('turbolinks:before-cache', this.onBeforeCache);
        window.addEventListener('turbolinks:request-end', this.onRequestEnd);
      }
    }, {
      key: 'destroy',
      value: function destroy() {
        window.removeEventListener('turbolinks:load', this.onLoad);
        window.removeEventListener('turbolinks:before-cache', this.onBeforeCache);
        window.removeEventListener('turbolinks:request-end', this.onRequestEnd);
      }
    }], [{
      key: 'attachTo',
      value: function attachTo(root) {
        return new DMCTurbolinks(root, new _materialComponentsWeb.base.MDCFoundation());
      }
    }]);

    return DMCTurbolinks;
  }(_materialComponentsWeb.base.MDCComponent);

  _materialComponentsWeb.autoInit.register('DMCTurbolinks', DMCTurbolinks);
});
(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(['exports', 'material-components-web'], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require('material-components-web'));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.mdc);
    global.passwordField = mod.exports;
  }
})(this, function (exports, _materialComponentsWeb) {
  'use strict';

  Object.defineProperty(exports, "__esModule", {
    value: true
  });
  exports.DMCPasswordField = undefined;

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  var _createClass = function () {
    function defineProperties(target, props) {
      for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
      }
    }

    return function (Constructor, protoProps, staticProps) {
      if (protoProps) defineProperties(Constructor.prototype, protoProps);
      if (staticProps) defineProperties(Constructor, staticProps);
      return Constructor;
    };
  }();

  function _possibleConstructorReturn(self, call) {
    if (!self) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return call && (typeof call === "object" || typeof call === "function") ? call : self;
  }

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        enumerable: false,
        writable: true,
        configurable: true
      }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
  }

  var DMCPasswordField = exports.DMCPasswordField = function (_base$MDCComponent) {
    _inherits(DMCPasswordField, _base$MDCComponent);

    function DMCPasswordField() {
      _classCallCheck(this, DMCPasswordField);

      return _possibleConstructorReturn(this, (DMCPasswordField.__proto__ || Object.getPrototypeOf(DMCPasswordField)).apply(this, arguments));
    }

    _createClass(DMCPasswordField, [{
      key: 'initialize',
      value: function initialize() {
        var _this2 = this;

        this.textField_ = new _materialComponentsWeb.textField.MDCTextField(this.root_);
        this.input_ = this.root_.querySelector('.dmc-text-field__input');
        this.toggle_ = this.root_.querySelector('.dmc-password-field__toggle');

        this.onToggle = function (event) {
          event.preventDefault();
          if (_this2.input_.type === "password") {
            _this2.input_.type = "text";
            _this2.toggle_.text = "visibility_off";
          } else {
            _this2.input_.type = "password";
            _this2.toggle_.text = "visibility";
          }
          if (event.type !== "keypress") {
            _this2.input_.selectionStart = _this2.input_.selectionEnd = _this2.input_.value.length;
            _this2.input_.focus();
          }
        };
        this.toggle_.addEventListener('click', this.onToggle);
        this.toggle_.addEventListener('keypress', this.onToggle);
      }
    }, {
      key: 'destroy',
      value: function destroy() {
        if (this.textField_) {
          this.textField_.destroy();
        }
        this.toggle_.removeEventListener('click', this.onToggle);
        this.toggle_.removeEventListener('keypress', this.onToggle);
      }
    }], [{
      key: 'attachTo',
      value: function attachTo(root) {
        return new DMCPasswordField(root, new _materialComponentsWeb.base.MDCFoundation());
      }
    }]);

    return DMCPasswordField;
  }(_materialComponentsWeb.base.MDCComponent);

  _materialComponentsWeb.autoInit.register('DMCPasswordField', DMCPasswordField);
});
(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(['exports', 'material-components-web'], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require('material-components-web'));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.mdc);
    global.responsiveDrawer = mod.exports;
  }
})(this, function (exports, _materialComponentsWeb) {
  'use strict';

  Object.defineProperty(exports, "__esModule", {
    value: true
  });
  exports.DMCResponsiveDrawer = undefined;

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  function _possibleConstructorReturn(self, call) {
    if (!self) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return call && (typeof call === "object" || typeof call === "function") ? call : self;
  }

  var _createClass = function () {
    function defineProperties(target, props) {
      for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
      }
    }

    return function (Constructor, protoProps, staticProps) {
      if (protoProps) defineProperties(Constructor.prototype, protoProps);
      if (staticProps) defineProperties(Constructor, staticProps);
      return Constructor;
    };
  }();

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        enumerable: false,
        writable: true,
        configurable: true
      }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
  }

  var DMCResponsiveDrawer = exports.DMCResponsiveDrawer = function (_base$MDCComponent) {
    _inherits(DMCResponsiveDrawer, _base$MDCComponent);

    _createClass(DMCResponsiveDrawer, null, [{
      key: 'attachTo',
      value: function attachTo(root) {
        return new DMCResponsiveDrawer(root, new _materialComponentsWeb.base.MDCFoundation());
      }
    }]);

    function DMCResponsiveDrawer() {
      var _ref;

      _classCallCheck(this, DMCResponsiveDrawer);

      for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
        args[_key] = arguments[_key];
      }

      return _possibleConstructorReturn(this, (_ref = DMCResponsiveDrawer.__proto__ || Object.getPrototypeOf(DMCResponsiveDrawer)).call.apply(_ref, [this].concat(args)));
    }

    _createClass(DMCResponsiveDrawer, [{
      key: 'initialize',
      value: function initialize() {
        var _this2 = this;

        this.reconcileDrawer_ = 0;
        this.temporalDrawer_ = null;
        this.persistentDrawer_ = null;

        this.drawer_ = this.root_.querySelector('nav');
        this.header_ = this.drawer_.querySelector('header');
        this.headerContent_ = this.header_.querySelector('div');
        this.content_ = this.drawer_.querySelector('nav');

        this.onResize = function () {
          cancelAnimationFrame(_this2.reconcileDrawer_);
          _this2.reconcileDrawer_ = requestAnimationFrame(function () {
            return _this2.reconcileDrawer();
          });
        };

        window.addEventListener('resize', this.onResize);
        this.reconcileDrawer();
      }
    }, {
      key: 'destroy',
      value: function destroy() {
        window.removeEventListener('resize', this.onResize);
        if (this.temporalDrawer_) {
          this.temporalDrawer_.destroy();
        }
        if (this.persistentDrawer_) {
          this.persistentDrawer_.destroy();
        }
      }
    }, {
      key: 'reconcileDrawer',
      value: function reconcileDrawer() {
        var rootClasses = this.root_.classList;
        if (window.innerWidth < 992 && (!rootClasses.contains('mdc-temporary-drawer') || this.temporalDrawer_ === null)) {
          if (this.persistentDrawer_) {
            this.persistentDrawer_.destroy();
            this.persistentDrawer_ = null;
          }
          this.root_.classList.remove('mdc-persistent-drawer', 'mdc-persistent-drawer--open');
          this.drawer_.classList.remove('mdc-persistent-drawer__drawer');
          this.header_.classList.remove('mdc-persistent-drawer__header');
          this.headerContent_.classList.remove('mdc-persistent-drawer__header-content');
          this.content_.classList.remove('mdc-persistent-drawer__content');

          this.root_.classList.add('mdc-temporary-drawer');
          this.drawer_.classList.add('mdc-temporary-drawer__drawer');
          this.header_.classList.add('mdc-temporary-drawer__header');
          this.headerContent_.classList.add('mdc-temporary-drawer__header-content');
          this.content_.classList.add('mdc-temporary-drawer__content');
          this.temporalDrawer_ = new _materialComponentsWeb.drawer.MDCTemporaryDrawer(this.root_);
          this.drawer_.removeEventListener('click', this.temporalDrawer_.foundation_.drawerClickHandler_);
        } else if (window.innerWidth >= 992 && (!rootClasses.contains('mdc-persistent-drawer') || this.persistentDrawer_ === null)) {
          if (this.temporalDrawer_) {
            this.temporalDrawer_.destroy();
            this.temporalDrawer_ = null;
          }
          this.root_.classList.remove('mdc-temporary-drawer');
          this.drawer_.classList.remove('mdc-temporary-drawer__drawer');
          this.header_.classList.remove('mdc-temporary-drawer__header');
          this.headerContent_.classList.remove('mdc-temporary-drawer__header-content');
          this.content_.classList.remove('mdc-temporary-drawer__content');

          this.root_.classList.add('mdc-persistent-drawer');
          if (sessionStorage.getItem('dmc_site_drawer_state') != "closed") {
            this.root_.classList.add('mdc-persistent-drawer--open');
          } else {
            this.root_.classList.remove('mdc-persistent-drawer--open');
          }
          this.drawer_.classList.add('mdc-persistent-drawer__drawer');
          this.header_.classList.add('mdc-persistent-drawer__header');
          this.headerContent_.classList.add('mdc-persistent-drawer__header-content');
          this.content_.classList.add('mdc-persistent-drawer__content');
          this.persistentDrawer_ = new _materialComponentsWeb.drawer.MDCPersistentDrawer(this.root_);
          this.drawer_.removeEventListener('click', this.persistentDrawer_.foundation_.drawerClickHandler_);
        }
      }
    }, {
      key: 'open',
      get: function get() {
        if (this.persistentDrawer_) {
          return this.persistentDrawer_.open;
        } else {
          return this.temporalDrawer_.open;
        }
      },
      set: function set(value) {
        if (this.persistentDrawer_) {
          sessionStorage.setItem('dmc_site_drawer_state', value ? "open" : "closed");
          return this.persistentDrawer_.open = value;
        } else {
          return this.temporalDrawer_.open = value;
        }
      }
    }]);

    return DMCResponsiveDrawer;
  }(_materialComponentsWeb.base.MDCComponent);

  _materialComponentsWeb.autoInit.register('DMCResponsiveDrawer', DMCResponsiveDrawer);
});
(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(['exports', 'material-components-web'], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require('material-components-web'));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.mdc);
    global.toggleDrawer = mod.exports;
  }
})(this, function (exports, _materialComponentsWeb) {
  'use strict';

  Object.defineProperty(exports, "__esModule", {
    value: true
  });
  exports.DMCToggleDrawer = undefined;

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  var _createClass = function () {
    function defineProperties(target, props) {
      for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
      }
    }

    return function (Constructor, protoProps, staticProps) {
      if (protoProps) defineProperties(Constructor.prototype, protoProps);
      if (staticProps) defineProperties(Constructor, staticProps);
      return Constructor;
    };
  }();

  function _possibleConstructorReturn(self, call) {
    if (!self) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return call && (typeof call === "object" || typeof call === "function") ? call : self;
  }

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        enumerable: false,
        writable: true,
        configurable: true
      }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
  }

  var DMCToggleDrawer = exports.DMCToggleDrawer = function (_base$MDCComponent) {
    _inherits(DMCToggleDrawer, _base$MDCComponent);

    function DMCToggleDrawer() {
      _classCallCheck(this, DMCToggleDrawer);

      return _possibleConstructorReturn(this, (DMCToggleDrawer.__proto__ || Object.getPrototypeOf(DMCToggleDrawer)).apply(this, arguments));
    }

    _createClass(DMCToggleDrawer, [{
      key: 'initialize',
      value: function initialize() {
        var _this2 = this;

        this.drawer_ = document.getElementById(this.root_.dataset.toggleDrawerId);
        this.onClick = function (event) {
          event.preventDefault();
          var new_state = !_this2.drawer_.DMCResponsiveDrawer.open;
          _this2.drawer_.DMCResponsiveDrawer.open = new_state;
        };
        this.root_.addEventListener('click', this.onClick);
      }
    }, {
      key: 'destroy',
      value: function destroy() {
        this.root_.removeEventListener('click', this.onClick);
      }
    }], [{
      key: 'attachTo',
      value: function attachTo(root) {
        return new DMCToggleDrawer(root, new _materialComponentsWeb.base.MDCFoundation());
      }
    }]);

    return DMCToggleDrawer;
  }(_materialComponentsWeb.base.MDCComponent);

  _materialComponentsWeb.autoInit.register('DMCToggleDrawer', DMCToggleDrawer);
});
//# sourceMappingURL=django-material-components.js.map
