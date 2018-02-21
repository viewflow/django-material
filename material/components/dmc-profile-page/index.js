/* eslint-env browser */

import {Controller} from 'stimulus';
import smartcrop from 'smartcrop';
import Turbolinks from 'turbolinks';


export default class extends Controller {
  initialize() {
    this._uploadButtonEl = this.element.querySelector('.dmc-profile-avatar__change');
    this._formEl = this.element.querySelector('form');
  }

  connect() {
    this._uploadButtonEl.addEventListener('change', this.onChangeAvatarClick);
  }

  disconnect() {
    this._uploadButtonEl.removeEventListener('change', this.onChangeAvatarClick);
  }

  onChangeAvatarClick = (event) => {
    let files = event.target.files;
    if (files.length === 0 || files[0].type.indexOf('image') === -1) {
      this.showError('No images selected');
    }

    let reader = new FileReader();
    reader.onload = (readerEvent) => {
      let image = new Image();
      image.onload = () => {
        this._crop(image).then((cropCanvas) => {
          this._upload(cropCanvas);
        }).catch((error) => {
          this._showError(error.message || 'Image cropping error');
        });
      };
      image.src = readerEvent.target.result;
    };
    reader.readAsDataURL(files[0]);
  };

  _crop(image, onSuccess) {
    let options = {
      minScale: 1,
      width: 256,
      height: 256,
    };
    return smartcrop.crop(image, options).then((result) => {
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

  _upload(canvas) {
    this._uploadButtonEl.classList.toggle('dmc-profile-avatar__change--disabled');

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
      let formData = new FormData(this._formEl);
      formData.append('avatar', blob, 'avatar.jpg');
      xhr.send(formData);
    });
  }

  _showError(message, timeout=2000) {
    let snackbarEvent = new CustomEvent('DMCSnackbar:show', {
      'detail': {message: message, timeout: timeout},
    });
    window.dispatchEvent(snackbarEvent);
  }
}

