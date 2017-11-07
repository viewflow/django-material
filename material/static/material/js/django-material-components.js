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
  exports.DMCActiveNav = exports.DMCActiveNavFoundation = undefined;

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

  var DMCActiveNavFoundation = exports.DMCActiveNavFoundation = function (_base$MDCFoundation) {
    _inherits(DMCActiveNavFoundation, _base$MDCFoundation);

    function DMCActiveNavFoundation() {
      _classCallCheck(this, DMCActiveNavFoundation);

      return _possibleConstructorReturn(this, (DMCActiveNavFoundation.__proto__ || Object.getPrototypeOf(DMCActiveNavFoundation)).apply(this, arguments));
    }

    _createClass(DMCActiveNavFoundation, [{
      key: 'init',
      value: function init() {
        alert(1);
      }
    }, {
      key: 'destroy',
      value: function destroy() {
        alert(2);
      }
    }]);

    return DMCActiveNavFoundation;
  }(_materialComponentsWeb.base.MDCFoundation);

  var DMCActiveNav = exports.DMCActiveNav = function (_base$MDCComponent) {
    _inherits(DMCActiveNav, _base$MDCComponent);

    function DMCActiveNav() {
      _classCallCheck(this, DMCActiveNav);

      return _possibleConstructorReturn(this, (DMCActiveNav.__proto__ || Object.getPrototypeOf(DMCActiveNav)).apply(this, arguments));
    }

    _createClass(DMCActiveNav, [{
      key: 'getDefaultFoundation',
      value: function getDefaultFoundation() {
        return new DMCActiveNavFoundation({});
      }
    }], [{
      key: 'attachTo',
      value: function attachTo(root) {
        return new DMCActiveNav(root);
      }
    }]);

    return DMCActiveNav;
  }(_materialComponentsWeb.base.MDCComponent);

  _materialComponentsWeb.autoInit.register('DMCActiveNav', DMCActiveNav);
});
//# sourceMappingURL=django-material-components.js.map
