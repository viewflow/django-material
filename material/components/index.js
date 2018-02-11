import {Application} from 'stimulus';

import inputFieldController from './input-field';

// import './layout';

export const application = Application.start();
application.register('input-field', inputFieldController);
