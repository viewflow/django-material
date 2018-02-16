/* eslint-env browser */

import DMCCalendar from './calendar';
import DMCDateUtils from './date-utils';


export default class DMCPopupCalendar extends DMCCalendar {
  initialize() {
    super.initialize();
    this._targetEl = document.getElementById(this.element.dataset.dateTarget);

    let headerEl = this.element.querySelector('.dmc-calendar-header');
    this._headerYearEl = headerEl.querySelector('.dmc-calendar-header__year');
    this._headerWeekdayEl = headerEl.querySelector('.dmc-calendar-header__weekday');
    this._headerDayEl = headerEl.querySelector('.dmc-calendar-header__day');
  }

  _updateCurrentDate() {
    super._updateCurrentDate();
    this._renderHeader();
  }

  _renderHeader() {
    if (!isNaN(this.selectedDate)) {
      this._headerYearEl.innerText = this.selectedDate.getFullYear();
      this._headerWeekdayEl.innerText = DMCDateUtils.daysOfWeekAbbr[this.selectedDate.getDay()] + ',';
      this._headerDayEl.innerText = DMCDateUtils.monthsOfYearAbbr[this.selectedDate.getMonth()] +
        ' ' + this.selectedDate.getDate();
    } else {
      this._headerYearEl.innerText = '';
      this._headerWeekdayEl.innerText = '';
      this._headerDayEl.innerText = '';
    }
  }
}
