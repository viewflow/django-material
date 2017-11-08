if(window.mdc) {
  if(window.Turbolinks) {
    window.addEventListener('turbolinks:load', function() {
      window.mdc.autoInit()
    })
    window.addEventListener('turbolinks:before-cache', function() {
      var nodes = document.querySelectorAll('[data-mdc-auto-init]');
      for(var i=0; i<nodes.length; i++) {
        var node = nodes[i],
            ctorName = nodes[i].dataset.mdcAutoInit,
            component = node[ctorName]
        component.destroy()
      }
    })
  } else {
    window.addEventListener('load', function() {
      window.mdc.autoInit()
    })
  }
}
