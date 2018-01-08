class DMCProfilePage {
  static attachTo(root) {
    return new DMCProfilePage(root);
  }

  constructor(root) {
    this.root_ = root;
    this.uploadButton_ = this.root_.querySelector('.dmc-profile-avatar__change');
    this.avatar_ = this.root_.querySelector('.dmc-profile-avatar__media img');
    this.onChange = (event) => {
      let files = event.target.files;
      if (files.length === 0 || files[0].type.indexOf('image') === -1) {
        this.showError('No images selected');
      }

      let reader = new FileReader();
      reader.onload = (readerEvent) => {
        let image = new Image();
        image.onload = () => {
          this.crop(image).then((cropCanvas) => {
            this.avatar_.src=cropCanvas.toDataURL('image/png');
            this.upload(cropCanvas);
          }).catch((error) => {
            this.showError(error.message || 'Image cropping error');
          });
        };
        image.src = readerEvent.target.result;
      };
      reader.readAsDataURL(files[0]);
    };

    this.uploadButton_.addEventListener('change', this.onChange);
  }

  crop(image, onSuccess) {
    let options = {
      minScale: 1,
      width: 256,
      height: 256,
    };
    return SmartCrop.crop(image, options).then((result) => {
      let cropCanvas = document.createElement('canvas');
      cropCanvas.width = 256;
      cropCanvas.height = 256;
      cropCanvas.getContext('2d').drawImage(
        image,
        result.topCrop.x, result.topCrop.y, result.topCrop.width, result.topCrop.height,
        0, 0, 256, 256
      );
      return cropCanvas;
    });
  }

  upload(canvas) {
    this.uploadButton_.classList.toggle('dmc-profile-avatar__change--disabled');

    let xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.search, true);
    xhr.setRequestHeader('Turbolinks-Referrer', window.location);

    xhr.onload = (event) => {
      let location = xhr.getResponseHeader('turbolinks-location');
      let snapshot = window.Turbolinks.Snapshot.wrap(xhr.response);

      if (!location) {
        location = window.location.href;
      }

      window.Turbolinks.controller.adapter.hideProgressBar();
      window.Turbolinks.controller.cache.put(location, snapshot);
      window.Turbolinks.visit(location, {action: 'restore'});
      window.Turbolinks.clearCache();

      if (xhr.status > 299) {
        Turbolinks.controller.disable();
      }
    };

    xhr.onerror = (event) => {
      window.Turbolinks.controller.adapter.hideProgressBar();
      this.uploadButton_.classList.toggle('dmc-profile-avatar__change--disabled');
      this.showError('Request error');
    };

    window.Turbolinks.controller.adapter.showProgressBarAfterDelay();

    canvas.toBlob((blob) => {
      let formData = new FormData(this.root_.querySelector('form'));
      formData.append('avatar', blob, 'avatar.jpg');
      xhr.send(formData);
    });
  }

  showError(message, timeout=2000) {
    let snackbarEvent = new CustomEvent('DMCSnackbar:show', {
      'detail': {message: message, timeout: timeout},
    });
    window.dispatchEvent(snackbarEvent);
  }

  destroy() {
    this.uploadButton_.removeEventListener('change', this.onChange);
  }
}

dmc.register('DMCProfilePage', DMCProfilePage);
