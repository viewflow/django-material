import {Application} from 'stimulus';

import inputFieldController from './input-field';

import './dmc-breadcrumbs';
import './dmc-card';
import './dmc-form-page';
import './dmc-list';
import './dmc-lockscreen';
import './dmc-page';
import './dmc-submit-button';

export const application = Application.start();
application.register('input-field', inputFieldController);
