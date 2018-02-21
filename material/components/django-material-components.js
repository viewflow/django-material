import {Application} from 'stimulus';


import * as dateTime from './dmc-datetime-fields';
import DMCActiveNavigation from './dmc-active-navigation';
import DMCCardMenu from './dmc-card-menu';
import DMCCheckbox from './dmc-checkbox-field';
import DMCDrawer from './dmc-drawer';
import DMCForm from './dmc-form';
import DMCFormField from './dmc-form-field';
import DMCInputField from './dmc-input-field';
import DMCPasswordField from './dmc-password-field';
import DMCScrollLockFix from './dmc-scroll-lock-fix';
import DMCSelectField from './dmc-select-field';
import DMCSnackbar from './dmc-snackbar';
import DMCToggleDrawerButton from './dmc-toggle-drawer-button';

export const application = Application.start();
application.register('dmc-active-navigation', DMCActiveNavigation);
application.register('dmc-card-menu', DMCCardMenu);
application.register('dmc-checkbox-field', DMCCheckbox);
application.register('dmc-date-input-field', dateTime.DMCDateInput);
application.register('dmc-drawer', DMCDrawer);
application.register('dmc-form', DMCForm);
application.register('dmc-form-field', DMCFormField);
application.register('dmc-inline-calendar-field', dateTime.DMCInlineCalendar);
application.register('dmc-input-field', DMCInputField);
application.register('dmc-password-field', DMCPasswordField);
application.register('dmc-popup-calendar', dateTime.DMCPopupCalendar);
application.register('dmc-scroll-lock-fix', DMCScrollLockFix);
application.register('dmc-select-field', DMCSelectField);
application.register('dmc-snackbar', DMCSnackbar);
application.register('dmc-toggle-drawer-button', DMCToggleDrawerButton);
