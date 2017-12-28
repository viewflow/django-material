import {autoInit, base, snackbar} from 'material-components-web';


export class DMCSnackbar extends base.MDCComponent {
  static attachTo(root) {
    return new DMCSnackbar(root, new base.MDCFoundation());
  }

  initialize() {
    this.snackbar_ = snackbar.MDCSnackbar.attachTo(this.root_);

    let initialText = this.root_.querySelector('.mdc-snackbar__text');

    if (initialText && initialText.textContent) {
      this.snackbar_.show({message: initialText.textContent});
    }

    this.showSnackbar_ = (event) => {
      this.snackbar_.show(event.detail);
    };

    window.addEventListener('DMCSnackbar:show', this.showSnackbar_, false);
  }

  destroy() {
    this.snackbar_.destroy();
    window.removeEventListener('DMCSnackbar:show', this.showSnackbar_);
  }
}

autoInit.register('DMCSnackbar', DMCSnackbar);
