/* eslint-env browser */
import DMCCalendar from './calendar';
import DMCDateUtils from './date-utils';


export default class DMCInlineCalendar extends DMCCalendar {
  initialize() {
    super.initialize();
    this._targetEl = document.getElementById(this.element.dataset.dateTarget);

    let initialDate = DMCDateUtils.parseDateTime(
      this._targetEl.dataset.dateFormat,
      this._targetEl.value
    );
    if (isNaN(initialDate)) {
      initialDate = new Date();
    } else {
      this._selectedDate = initialDate;
    }
    this._currentYear = initialDate.getFullYear();
    this._currentMonth = initialDate.getMonth();
  }

  connect() {
    super.connect();
    this._renderMonth(this._currentYear, this._currentMonth, this._currentMonthEl);
  }

  _changeDay(day) {
    if (!isNaN(this.selectedDate) && this.selectedDate.getDate() === day) {
      day = undefined;
    }
    super._changeDay(day);
  }

  /** Set new selected date on a month change */
  _updateCurrentMonth() {
    if (!isNaN(this.selectedDate)) {
      let day = this.selectedDate.getDate();
      let daysInMonth = new Date(this._currentYear, this._currentMonth+1, 0).getDate();
      if (daysInMonth < day) {
        day = daysInMonth;
      }
      this._selectedDate = new Date(this._currentYear, this._currentMonth, day);
      this._updateCurrentDate();
    } else {
      this._renderMonth(this._currentYear, this._currentMonth, this._currentMonthEl);
    }
  }

  /** Update target hidden input */
  _updateCurrentDate() {
    if (!isNaN(this.selectedDate)) {
      this._targetEl.value = DMCDateUtils.formatDate(
        this._targetEl.dataset.dateFormat,
        this.selectedDate
      );
    } else {
      this._targetEl.value = '';
    }
    super._updateCurrentDate();
  }
}
