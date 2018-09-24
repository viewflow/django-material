class Snackbar extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const children = this.children;
    for(let i=0; i<this.children.length;i++) {
      M.toast({html: this.children[0].innerHTML, displayLength: 10000, classes: this.children[0].className})
    }
  }

}

window.addEventListener('load', () => {
  window.customElements.define('dmc-snackbar', Snackbar);
});
