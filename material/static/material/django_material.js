import * as mdc from 'material-components-web'
import * as dmc from './components'


(() => {
  console.log(dmc, mdc)

  mdc.autoInit()

  document.querySelector('.demo-menu').addEventListener('click', function() {
    var drawer = document.querySelector('.mdc-persistent-drawer').MDCPersistentDrawer;
    drawer.open = !drawer.open;
  });
})()
