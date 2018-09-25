class Snackbar extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    window.addEventListener('dmc-snackbar:show', this.onShowSnackbarEvent, false);

    const children = this.children;
    for(let i=0; i<this.children.length;i++) {
      setTimeout(() => {
        M.toast({html: this.children[0].innerHTML, displayLength: 10000, classes: this.children[0].className});
      });
    }
  }

  disconnectedCallback() {
    window.removeEventListener('dmc-snackbar:show', this.onShowSnackbarEvent);
    M.Toast.dismissAll();
  }

  onShowSnackbarEvent = (event) => {
    M.toast({html: event.detail.message, displayLength: 10000});
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-snackbar', Snackbar);
});
