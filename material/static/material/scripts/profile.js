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
        let snackbarEvent = new CustomEvent('DMCSnackbar:show', {
          'detail': {message: 'No images selected', timeout: 2000},
        });
        window.dispatchEvent(snackbarEvent);
      }

      let reader = new FileReader();
      reader.onload = (readerEvent) => {
        let img = new Image();
        img.onload = () => {
          let options = {
            minScale: 1,
          };
          SmartCrop.crop(img, options).then((result) => {
            let cropCanvas = document.createElement('canvas');
            cropCanvas.width = 512;
            cropCanvas.height = 512;
            cropCanvas.getContext('2d').drawImage(
              img,
              result.topCrop.x, result.topCrop.y, result.topCrop.width, result.topCrop.height,
              0, 0, 512, 512
            );
            this.avatar_.src=cropCanvas.toDataURL('image/png');
          }).catch((error) => {
            let snackbarEvent = new CustomEvent('DMCSnackbar:show', {
              'detail': {message: error.message || 'Image cropping error', timeout: 2000},
            });
            window.dispatchEvent(snackbarEvent);
          });
        };
        img.src = readerEvent.target.result;
      };
      reader.readAsDataURL(files[0]);
    };

    this.uploadButton_.addEventListener('change', this.onChange);
  }

  destroy() {
    this.uploadButton_.removeEventListener('change', this.onChange);
  }
}

dmc.register('DMCProfilePage', DMCProfilePage);
