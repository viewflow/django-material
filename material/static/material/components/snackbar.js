import {base, snackbar} from 'material-components-web';
import {register} from 'django-material-registry';


class DMCSnackbar extends base.MDCComponent {
  static attachTo(root) {
    return new DMCSnackbar(root, new base.MDCFoundation());
  }

  initialize() {
    this.snackbar_ = snackbar.MDCSnackbar.attachTo(this.root_);

    let initialText = this.root_.querySelector('.mdc-snackbar__text');

    if (initialText) {
      let actionText;
      let actionHandler;

      const message = Array.prototype.filter.call(initialText.childNodes, (element) => {
        return element.nodeType === Node.TEXT_NODE;
      }).map((element) => {
        return element.textContent.trim();
      }).join(' ');

      const link = initialText.querySelector('a');
      if (link && window.location.href !== link.href) {
        actionText = link.textContent;
        actionHandler = () => {
          if (window.Turbolinks) {
            window.Turbolinks.visit(link.href);
          } else {
            window.location = link.href;
          }
        };
      }

      if (message) {
        setTimeout( () => {
          this.snackbar_.show({
            message: message,
            actionText: actionText,
            actionHandler: actionHandler,
            multiline: true,
            timeout: 4500,
          });
        }, 300);
      }
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

register('DMCSnackbar', DMCSnackbar);
