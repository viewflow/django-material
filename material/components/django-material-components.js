import {Application} from 'stimulus';


import InputField from './forms/input-field';
import ActiveNavigation from './site/active-navigation';
import DMCCardMenu from './site/card-menu';
import DMCDrawer from './site/drawer';
import DMCToggleDrawerButton from './site/toggle-drawer-button';

export const application = Application.start();
application.register('input-field', InputField);
application.register('dmc-drawer', DMCDrawer);
application.register('dmc-card-menu', DMCCardMenu);
application.register('dmc-active-navigation', ActiveNavigation);
application.register('dmc-toggle-drawer-button', DMCToggleDrawerButton);
