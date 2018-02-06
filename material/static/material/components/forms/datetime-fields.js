class DMCDateUtils {
  static formatDate(format, value) {
    let result = '';
    for (let i=0; i< format.length; i++) {
      if (format[i] === '%') {
        switch (format[i+1]) {
          case 'd':
            result += ('0' + value.getDate()).slice(-2);
            break;
          case 'm':
            result += ('0' + (value.getMonth()+1)).slice(-2);
            break;
          case 'Y':
            result += value.getFullYear();
            break;
        }
        i++;
      } else {
        result += format[i];
      }
    }
    return result;
  };

  static parseDateTime(format, value) {
    let splitFormat = format.split(/[.\-/]/);
    let date = value.split(/[.\-/]/);
    let day;
    let month;
    let year;
    for (let i=0; i < splitFormat.length; i++) {
      switch (splitFormat[i]) {
          case '%d':
              day = date[i];
              break;
          case '%m':
              month = date[i] - 1;
              break;
          case '%Y':
              year = date[i];
              break;
      }
    }
    return new Date(Date.UTC(year, month, day));
  }

  static daysInMonth(year, month) {
    return new Date(year, month+1, 0).getDate();
  }
}

DMCDateUtils.firstDayOfWeek = parseInt(get_format('FIRST_DAY_OF_WEEK'));

DMCDateUtils.monthsOfYear = [
  gettext('January'),
  gettext('February'),
  gettext('March'),
  gettext('April'),
  gettext('May'),
  gettext('June'),
  gettext('July'),
  gettext('August'),
  gettext('September'),
  gettext('October'),
  gettext('November'),
  gettext('December'),
];

DMCDateUtils.monthsOfYearAbbr = [
  pgettext('three letter January', 'Jan'),
  pgettext('three letter February', 'Feb'),
  pgettext('three letter March', 'Mar'),
  pgettext('three letter April', 'Apr'),
  pgettext('three letter May', 'May'),
  pgettext('three letter June', 'Jun'),
  pgettext('three letter July', 'Jul'),
  pgettext('three letter August', 'Aug'),
  pgettext('three letter September', 'Sep'),
  pgettext('three letter October', 'Oct'),
  pgettext('three letter November', 'Nov'),
  pgettext('three letter December', 'Dec'),
];

DMCDateUtils.daysOfWeek = [
  pgettext('one letter Sunday', 'S'),
  pgettext('one letter Monday', 'M'),
  pgettext('one letter Tuesday', 'T'),
  pgettext('one letter Wednesday', 'W'),
  pgettext('one letter Thursday', 'T'),
  pgettext('one letter Friday', 'F'),
  pgettext('one letter Saturday', 'S'),
];

DMCDateUtils.daysOfWeekAbbr = [
  pgettext('three letter Sunday', 'Sun'),
  pgettext('three letter Monday', 'Mon'),
  pgettext('three letter Tuesday', 'Tue'),
  pgettext('three letter Wednesday', 'Wed'),
  pgettext('three letter Thursday', 'Thu'),
  pgettext('three letter Friday', 'Fri'),
  pgettext('three letter Saturday', 'Sat'),
];

/** Base class for calendar widgets */
class DMCCalendar {
  constructor(root) {
    this.root_ = root;
    this.surfaceEl_ = root.querySelector('.dmc-calendar__surface');
    this.currentMonthEl_ = root.querySelector('.dmc-calendar__month--current');
    this.prevMonthButtonEl_ = root.querySelector('.dmc-calendar__prev');
    this.nextMonthButtonEl_ = root.querySelector('.dmc-calendar__next');

    this.disabled_ = root.classList.contains('dmc-calendar--disabled');

    this.currentYear_ = 1970;
    this.currentMonth_ = 0;
    this.currentDay_ = NaN;

    // navigation
    if (!this.disabled_) {
      this.prevMonthClickHandler_ = () => this.handlePrevMonthClick_();
      this.prevMonthButtonEl_.addEventListener('click', this.prevMonthClickHandler_);

      this.nextMonthClickHandler_ = () => this.handleNextMonthClick_();
      this.nextMonthButtonEl_.addEventListener('click', this.nextMonthClickHandler_);

      this.dayClickHandler_ = (event) => this.handleDayClick_(event);
      this.surfaceEl_.addEventListener('click', this.dayClickHandler_);
    }
  }

  destroy() {
    if (!this.disabled_) {
      this.prevMonthButtonEl_.removeEventListener('click', this.prevMonthClickHandler_);
      this.nextMonthButtonEl_.removeEventListener('click', this.nextMonthClickHandler_);
      this.surfaceEl_.removeEventListener('click', this.dayClickHandler_);
    }
  }

  handleNextMonthClick_() {
    this.changeMonth_(1);
  }

  handlePrevMonthClick_() {
    this.changeMonth_(-1);
  }

  handleDayClick_(event) {
    if (event.target.tagName != 'SPAN') {
      return;
    }
    const day = parseInt(event.target.textContent);
    if (!isNaN(day)) {
      this.changeDay_(day);
    }
  }

  renderMonth_(year, month, day, target) {
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
          if (label === day) {
            class_ = ' dmc_calendar__current';
          }
        }

        days.push(`<div class="dmc-calendar__day${class_}"><span>${label}</span></div>`);
      }
      days.push('</div>');
    }
    daysEl.innerHTML = days.join('');
  };

  changeMonth_(shift) {
    this.currentMonth_ += shift;
    if (this.currentMonth_ < 0) {
      this.currentYear_ = this.currentYear_ - 1;
      this.currentMonth_ = 11;
    } else if (this.currentMonth_>11) {
      this.currentYear_ = this.currentYear_ + 1;
      this.currentMonth_ = 0;
    }

    if (!isNaN(this.currentDay_)) {
      let day = this.currentDay_;
      let daysInMonth = new Date(this.currentYear_, this.currentMonth_+1, 0).getDate();
      if (daysInMonth < this.currentDay_) {
        day = daysInMonth;
      }
      this.currentDay_ = day;
    }

    this.renderMonth_(this.currentYear_, this.currentMonth_, this.currentDay_, this.currentMonthEl_);
    this.updateCurrentDate_();
  }

  changeDay_(day) {
    this.currentDay_ = day;
    this.updateCurrentDate_();
    this.renderMonth_(this.currentYear_, this.currentMonth_, this.currentDay_, this.currentMonthEl_);
  }

  updateCurrentDate_() {
  }

  getSelectedDate() {
    return new Date(this.currentYear_, this.currentMonth_, this.currentDay_);
  }
}

/** Inline calendar widget. */
class DMCInlineCalendar extends DMCCalendar {
  static attachTo(root) {
    return new DMCInlineCalendar(root);
  }

  constructor(root) {
    super(root);
    this.targetEl_ = document.getElementById(root.dataset.dateTarget);

    // init date
    let initialDate = DMCDateUtils.parseDateTime(this.targetEl_.dataset.dateFormat, this.targetEl_.value);
    if (!isNaN(initialDate)) {
      this.currentYear_ = initialDate.getFullYear();
      this.currentMonth_ = initialDate.getMonth();
      this.currentDay_ = initialDate.getDate();
    }

    this.renderMonth_(this.currentYear_, this.currentMonth_, this.currentDay_, this.currentMonthEl_);
  }

  changeDay_(day) {
    if (this.currentDay === day) {
      day = undefined; // unset current date, if selected day clicked.
    }
    super.changeDay_(day);
  }

  // update target
  updateCurrentDate_() {
    if (!isNaN(this.getSelectedDate())) {
      this.targetEl_.value = DMCDateUtils.formatDate(
        this.targetEl_.dataset.dateFormat,
        this.getSelectedDate()
      );
    } else {
      this.targetEl_.value = '';
    }
    super.updateCurrentDate_();
  }
}

class DMCPopupCalendar extends DMCCalendar {
  constructor(root) {
    super(root);
    this.headerEl_ = root.querySelector('.dmc-calendar-header');
    this.headerYearEl_ = this.headerEl_.querySelector('.dmc-calendar-header__year');
    this.headerWeekdayEl_ = this.headerEl_.querySelector('.dmc-calendar-header__weekday');
    this.headerDayEl_ = this.headerEl_.querySelector('.dmc-calendar-header__day');
  }

  renderHeader() {
    this.headerYearEl_.innerText = this.currentYear_;
    if (!isNan(day)) {
      this.headerWeekdayEl_.innerText = DMCDateUtils.daysOfWeekAbbr[this.getSelectedDate().getDay()] + ',';
      this.headerDayEl_.innerText = DMCCalendar.monthsOfYearAbbr[this.currentMonth_] + ' ' + this.currentDay_;
    } else {
      this.headerWeekdayEl_.innerText = '';
      this.headerDayEl_.innerText = '';
    }
  }
}

class DMCDateInput {
  static attachTo(root) {
    return new DMCDateInput(root);
  }

  constructor(root) {
    this.root_ = root;
    this.textEl_ = root.querySelector('.mdc-text-field');
    this.calendarEl_ = root.querySelector('.dmc-calendar');
    this.dialogEl_ = root.querySelector('.mdc-dialog');
    this.buttonEl_ = root.querySelector('.dmc-datepicker__button');

    this.popupOpenHandler = (event) => this.handlePopupOpen(event);

    this.text_ = mdc.textField.MDCTextField.attachTo(this.textEl_);
    this.dialog_ = mdc.dialog.MDCDialog.attachTo(this.dialogEl_);
    this.calendar_ = new DMCPopupCalendar(this.calendarEl_);

    this.buttonEl_.addEventListener('click', this.popupOpenHandler);
  }

  destroy() {
    this.buttonEl_.removeEventListener('click', this.popupOpenHandler);
    this.text_.destroy();
    this.dialog_.destroy();
    this.calendar_.destroy();
  }

  handlePopupOpen(event) {
    event.preventDefault();
    this.dialog_.lastFocusedTarget = event.target;
    this.dialog_.show();
  }
}

dmc.register('DMCInlineCalendar', DMCInlineCalendar);
dmc.register('DMCDateInput', DMCDateInput);
