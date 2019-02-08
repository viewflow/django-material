/* eslint-env browser */
class TurbolinksElement extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    document.addEventListener('turbolinks:click', this._onClick);
  }

  disconnectedCallback() {
    document.removeEventListener('turbolinks:click', this._onClick);
  }

  _onClick = (event) => {
    // https://github.com/turbolinks/turbolinks/issues/75#issuecomment-445325162
    let anchorElement = event.target;
    let isSamePageAnchor = (
      anchorElement.hash &&
      anchorElement.origin === window.location.origin &&
      anchorElement.pathname === window.location.pathname
    );

    if (isSamePageAnchor) {
      window.Turbolinks.controller.pushHistoryWithLocationAndRestorationIdentifier(
        event.data.url,
        window.Turbolinks.uuid()
      );
      event.preventDefault();
    }
  }

  _onLoad = (event) => {
    if (window.location.hash) {
      let element = document.getElementById(window.location.hash.substring(1));
      let pos = element.getBoundingClientRect();
      window.scrollTo(0, pos.y);
    }
  }
}

window.addEventListener('load', () => {
  window.customElements.define('dmc-turbolinks', TurbolinksElement);
});
