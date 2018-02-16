/* eslint-env browser */

import {Controller} from 'stimulus';
import {dialog, textField} from 'material-components-web';
import DMCDateUtils from './date-utils';


export default class DMCDateInput extends Controller {
  initialize() {
    this._textFieldEl = this.element.querySelector('.mdc-text-field');
    this._calendarEl = this.element.querySelector('.dmc-calendar');
    this._dialogEl = this.element.querySelector('.mdc-dialog');
    this._buttonEl = this.element.querySelector('.dmc-datepicker__button');
    this._targetEl = document.getElementById(this._calendarEl.dataset.dateTarget);
  }

  connect() {
    this._mdcTextField = textField.MDCTextField.attachTo(this._textFieldEl);
    this._mdcDialog = dialog.MDCDialog.attachTo(this._dialogEl);

    this._buttonEl.addEventListener('click', this.onPickerButtonClick);
    this._mdcDialog.listen('MDCDialog:accept', this.onDialogAccept);
  }

  destroy() {
    this._buttonEl.removeEventListener('click', this.onPickerButtonClick);
    this._mdcTextField.destroy();
    this._mdcDialog.destroy();
  }

  getPopupController() {
    return this.application.getControllerForElementAndIdentifier(this._calendarEl, 'dmc-popup-calendar');
  }

  onPickerButtonClick = (event) => {
    event.preventDefault();

    let selectedDate = DMCDateUtils.parseDateTime(
      this._targetEl.dataset.dateFormat,
      this._targetEl.value
    );
    if (isNaN(selectedDate)) {
      selectedDate = new Date();
    }
    this.getPopupController().selectedDate = selectedDate;

    this._mdcDialog.lastFocusedTarget = event.target;
    this._mdcDialog.show();
  }

  onDialogAccept = () => {
    const selectedDate = this.getPopupController().selectedDate;
    if (!isNaN(selectedDate)) {
      this._mdcTextField.value = DMCDateUtils.formatDate(
        this._targetEl.dataset.dateFormat,
        selectedDate
      );
    }
  }
}
