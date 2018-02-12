import {Application} from 'stimulus';

import './forms/checkbox-field';
import './forms/datetime-fields';
import './forms/form';
import './forms/password-field';
import './forms/select-field';
import inputFieldController from './forms/input-field';

import './site/breadcrumbs';
import './site/card';
import './site/form-page';
import './site/list';
import './site/lockscreen';
import './site/page';
import './site/profile-page';

export const application = Application.start();
application.register('input-field', inputFieldController);
