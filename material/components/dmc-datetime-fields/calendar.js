import {Controller} from 'stimulus';
import DMCDateUtils from './date-utils';

export default class DMCCalendar extends Controller {
  initialize() {
    this._currentYear = 1970;
    this._currentMonth = 0;
    this._selectedDate = NaN;

    this._disabled = this.element.classList.contains('dmc-calendar--disabled');

    this._surfaceEl = this.element.querySelector('.dmc-calendar__surface');
    this._currentMonthEl = this.element.querySelector('.dmc-calendar__month--current');
    this._prevMonthButton = this.element.querySelector('.dmc-calendar__prev');
    this._nextMonthButton = this.element.querySelector('.dmc-calendar__next');
  }

  connect() {
    if (!this._disabled) {
      this._prevMonthButton.addEventListener('click', this.onPrevMonthClick);
      this._nextMonthButton.addEventListener('click', this.onNextMonthClick);
      this._surfaceEl.addEventListener('click', this.onSurfaceClick);
    }
  }

  disconnect() {
    if (!this._disabled) {
      this._prevMonthButton.removeEventListener('click', this.onPrevMonth);
      this._nextMonthButton.removeEventListener('click', this.onNextMonthClick);
      this._surfaceEl.removeEventListener('click', this.onSurfaceClick);
    }
  }

  onPrevMonthClick = () => {
    this._changeMonth(-1);
  }

  onNextMonthClick = () => {
    this._changeMonth(1);
  }

  onSurfaceClick = (event) => {
    if (this._disabled || event.target.tagName != 'SPAN') {
      return;
    }
    const day = parseInt(event.target.textContent);
    if (!isNaN(day)) {
      this._changeDay(day);
    }
  }

  _renderMonth(year, month, target) {
    let currentDay = NaN;
    if (!isNaN(this.selectedDate) &&
        this.selectedDate.getFullYear() === year &&
        this.selectedDate.getMonth() == month) {
      currentDay = this.selectedDate.getDate();
    }

    // title
    let titleEl = target.querySelector('.dmc-calendar__title');
    titleEl.innerText = `${DMCDateUtils.monthsOfYear[month]} ${year}`;

    // weekdays
    let weekdaysEl = target.querySelector('.dmc-calendar__weekdays');
    weekdaysEl.innerHTML = [0, 1, 2, 3, 4, 5, 6].map((e) => {
      let day = DMCDateUtils.daysOfWeek[(e + DMCDateUtils.firstDayOfWeek) % 7];
      return `<div class="dmc-calendar__weekday">${day}</div>`;
    }).join('');

    // days
    let daysEl = target.querySelector('.dmc_calendar__days');
    let days = [];
    let startPos = new Date(year, month, 1).getDay() - DMCDateUtils.firstDayOfWeek;
    let daysInMonth = DMCDateUtils.daysInMonth(year, month);
    for (let i=0; i<6; i++) {
      days.push('<div class="dmc-calendar__row">');
      for (let j=0; j<7; j++) {
        let cell = i*7+j;
        let label='';
        let class_='';
        if (cell >= startPos && cell < daysInMonth + startPos) {
          label = cell - startPos + 1;
          if (label === currentDay) {
            class_ = ' dmc_calendar__current';
          }
        }

        days.push(`<div class="dmc-calendar__day${class_}"><span>${label}</span></div>`);
      }
      days.push('</div>');
    }
    daysEl.innerHTML = days.join('');
  };

  _changeMonth(shift) {
    this._currentMonth += shift;
    if (this._currentMonth < 0) {
      this._currentYear = this._currentYear - 1;
      this._currentMonth = 11;
    } else if (this._currentMonth>11) {
      this._currentYear = this._currentYear + 1;
      this._currentMonth = 0;
    }

    this._updateCurrentMonth();
  }

  _changeDay(day) {
    this._selectedDate = new Date(this._currentYear, this._currentMonth, day);
    this._updateCurrentDate();
  }

  /** Subclasses could override this */
  _updateCurrentMonth() {
    this._renderMonth(this._currentYear, this._currentMonth, this._currentMonthEl);
  }

  /** Subclasses could override this */
  _updateCurrentDate() {
    this._renderMonth(this._currentYear, this._currentMonth, this._currentMonthEl);
  }

  set selectedDate(value) {
    this._selectedDate = value;
    if (!isNaN(value)) {
      this._currentYear = value.getFullYear();
      this._currentMonth = value.getMonth();
    }
    this._updateCurrentDate();
  }

  get selectedDate() {
    return this._selectedDate;
  }
}
