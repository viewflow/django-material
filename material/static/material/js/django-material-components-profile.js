(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(['exports', 'material-components-web', 'django-material-registry'], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require('material-components-web'), require('django-material-registry'));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.mdc, global.djangoMaterialRegistry);
    global.profile = mod.exports;
  }
})(this, function (exports, _materialComponentsWeb, _djangoMaterialRegistry) {
  'use strict';

  Object.defineProperty(exports, "__esModule", {
    value: true
  });
  exports.DMCProfilePage = undefined;

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

  var DMCProfilePage = exports.DMCProfilePage = function (_base$MDCComponent) {
    _inherits(DMCProfilePage, _base$MDCComponent);

    function DMCProfilePage() {
      _classCallCheck(this, DMCProfilePage);

      return _possibleConstructorReturn(this, (DMCProfilePage.__proto__ || Object.getPrototypeOf(DMCProfilePage)).apply(this, arguments));
    }

    _createClass(DMCProfilePage, [{
      key: 'initialize',
      value: function initialize() {
        // TODO
        alert('1');
      }
    }], [{
      key: 'attachTo',
      value: function attachTo(root) {
        return new DMCProfilePage(root, new _materialComponentsWeb.base.MDCFoundation());
      }
    }]);

    return DMCProfilePage;
  }(_materialComponentsWeb.base.MDCComponent);

  (0, _djangoMaterialRegistry.register)('DMCProfilePage', DMCProfilePage);
});
//# sourceMappingURL=django-material-components-profile.js.map
