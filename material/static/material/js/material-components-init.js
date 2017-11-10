if(window.mdc) {
  window.addEventListener('load', function(event) {
    window.mdc.autoInit()
    event.target.removeEventListener(
      event.type, arguments.callee);
  })
}
