import {Application} from 'stimulus';


import InputField from './forms/input-field';
import DMCForm from './forms/form';
import DMCActiveNavigation from './site/active-navigation';
import DMCCardMenu from './site/card-menu';
import DMCDrawer from './site/drawer';
import DMCSnackbar from './site/snackbar';
import DMCToggleDrawerButton from './site/toggle-drawer-button';

export const application = Application.start();
application.register('input-field', InputField);
application.register('dmc-form', DMCForm);
application.register('dmc-drawer', DMCDrawer);
application.register('dmc-card-menu', DMCCardMenu);
application.register('dmc-active-navigation', DMCActiveNavigation);
application.register('dmc-snackbar', DMCSnackbar);
application.register('dmc-toggle-drawer-button', DMCToggleDrawerButton);
