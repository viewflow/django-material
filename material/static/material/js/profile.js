'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var DMCProfilePage = function () {
  _createClass(DMCProfilePage, null, [{
    key: 'attachTo',
    value: function attachTo(root) {
      return new DMCProfilePage(root);
    }
  }]);

  function DMCProfilePage(root) {
    var _this = this;

    _classCallCheck(this, DMCProfilePage);

    this.root_ = root;
    this.uploadButton_ = this.root_.querySelector('.dmc-profile-avatar__change');
    this.avatar_ = this.root_.querySelector('.dmc-profile-avatar__media img');
    this.onChange = function (event) {
      var files = event.target.files;
      if (files.length === 0 || files[0].type.indexOf('image') === -1) {
        _this.showError('No images selected');
      }

      var reader = new FileReader();
      reader.onload = function (readerEvent) {
        var image = new Image();
        image.onload = function () {
          _this.crop(image).then(function (cropCanvas) {
            _this.avatar_.src = cropCanvas.toDataURL('image/png');
            _this.upload(cropCanvas);
          }).catch(function (error) {
            _this.showError(error.message || 'Image cropping error');
          });
        };
        image.src = readerEvent.target.result;
      };
      reader.readAsDataURL(files[0]);
    };

    this.uploadButton_.addEventListener('change', this.onChange);
  }

  _createClass(DMCProfilePage, [{
    key: 'crop',
    value: function crop(image, onSuccess) {
      var options = {
        minScale: 1,
        width: 256,
        height: 256
      };
      return SmartCrop.crop(image, options).then(function (result) {
        var cropCanvas = document.createElement('canvas');
        cropCanvas.width = 256;
        cropCanvas.height = 256;
        cropCanvas.getContext('2d').drawImage(image, result.topCrop.x, result.topCrop.y, result.topCrop.width, result.topCrop.height, 0, 0, 256, 256);
        return cropCanvas;
      });
    }
  }, {
    key: 'upload',
    value: function upload(canvas) {
      var _this2 = this;

      this.uploadButton_.classList.toggle('dmc-profile-avatar__change--disabled');

      var xhr = new XMLHttpRequest();
      xhr.open('POST', window.location.search, true);
      xhr.setRequestHeader('Turbolinks-Referrer', window.location);

      xhr.onload = function (event) {
        var location = xhr.getResponseHeader('turbolinks-location');
        var snapshot = window.Turbolinks.Snapshot.wrap(xhr.response);

        if (!location) {
          location = window.location.href;
        }

        window.Turbolinks.controller.adapter.hideProgressBar();
        window.Turbolinks.controller.cache.put(location, snapshot);
        window.Turbolinks.visit(location, { action: 'restore' });
        window.Turbolinks.clearCache();

        if (xhr.status > 299) {
          Turbolinks.controller.disable();
        }
      };

      xhr.onerror = function (event) {
        window.Turbolinks.controller.adapter.hideProgressBar();
        _this2.uploadButton_.classList.toggle('dmc-profile-avatar__change--disabled');
        _this2.showError('Request error');
      };

      window.Turbolinks.controller.adapter.showProgressBarAfterDelay();

      canvas.toBlob(function (blob) {
        var formData = new FormData(_this2.root_.querySelector('form'));
        formData.append('avatar', blob, 'avatar.jpg');
        xhr.send(formData);
      });
    }
  }, {
    key: 'showError',
    value: function showError(message) {
      var timeout = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2000;

      var snackbarEvent = new CustomEvent('DMCSnackbar:show', {
        'detail': { message: message, timeout: timeout }
      });
      window.dispatchEvent(snackbarEvent);
    }
  }, {
    key: 'destroy',
    value: function destroy() {
      this.uploadButton_.removeEventListener('change', this.onChange);
    }
  }]);

  return DMCProfilePage;
}();

dmc.register('DMCProfilePage', DMCProfilePage);
//# sourceMappingURL=profile.js.map
