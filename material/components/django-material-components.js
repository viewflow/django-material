import {Application} from 'stimulus';


import DMCInputField from './forms/input-field';
import DMCForm from './forms/form';
import DMCPasswordField from './forms/password-field';
import DMCSelectField from './forms/select-field';
import DMCActiveNavigation from './site/active-navigation';
import DMCCardMenu from './site/card-menu';
import DMCDrawer from './site/drawer';
import DMCSnackbar from './site/snackbar';
import DMCToggleDrawerButton from './site/toggle-drawer-button';
import DMCScrollLockFix from './site/scroll-lock-fix';

export const application = Application.start();
application.register('dmc-input-field', DMCInputField);
application.register('dmc-password-field', DMCPasswordField);
application.register('dmc-select-field', DMCSelectField);
application.register('dmc-form', DMCForm);
application.register('dmc-drawer', DMCDrawer);
application.register('dmc-card-menu', DMCCardMenu);
application.register('dmc-active-navigation', DMCActiveNavigation);
application.register('dmc-snackbar', DMCSnackbar);
application.register('dmc-toggle-drawer-button', DMCToggleDrawerButton);
application.register('dmc-scroll-lock-fix', DMCScrollLockFix);
