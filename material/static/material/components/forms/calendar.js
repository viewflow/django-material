/* global dmc, gettext, pgettext, get_format*/

class DMCCalendar {
  static attachTo(root) {
    return new DMCCalendar(root);
  }

  constructor(root) {
    this.root_ = root;

    this.targetEl_ = document.getElementById(root.dataset.dateTarget);
    this.surfaceEl_ = root.querySelector('.dmc-calendar__surface');

    // current month
    this.currEl_ = root.querySelector('.dmc-calendar__month--current');
    this.currTitleEl_ = this.currEl_.querySelector('.dmc-calendar__title');
    this.currWeekdaysEl_ = this.currEl_.querySelector('.dmc-calendar__weekdays');
    this.currDaysEl_ = this.currEl_.querySelector('.dmc_calendar__days');

    // initialization
    this.currentDate_ = DMCCalendar.parseDate(this.targetEl_.dataset.dateFormat, this.targetEl_.value);
    if (isNaN(this.currentDate_)) {
      this.currentDate_ = new Date();
      this.updateTarget();
    }
    this.renderCurrentMonth();

    // navigation
    this.prevMonthEl_ = root.querySelector('.dmc-calendar__prev');
    this.onPrevMonthClick = () => {
      this.changeMonth(-1);
    };
    this.prevMonthEl_.addEventListener('click', this.onPrevMonthClick);

    this.nextMonthEl_ = root.querySelector('.dmc-calendar__next');
    this.onNextMonthClick = () => {
      this.changeMonth(1);
    };
    this.nextMonthEl_.addEventListener('click', this.onNextMonthClick);

    this.onDaysClick = (event) => {
      if (event.target.tagName != 'SPAN') {
        return;
      }

      const day = parseInt(event.target.textContent);

      if (isNaN(day)) {
        return;
      };
      this.changeDay(day);
    };
    this.surfaceEl_.addEventListener('click', this.onDaysClick);
  }

  destroy() {
    this.prevMonthEl_.removeEventListener('click', this.onPrevMonthClick);
    this.nextMonthEl_.removeEventListener('click', this.onNextMonthClick);
    this.surfaceEl_.removeEventListener('click', this.onDaysClick);
  }

  renderCurrentMonth() {
    this.renderTitle(this.currentDate_.getFullYear(), this.currentDate_.getMonth(), this.currTitleEl_);
    this.renderWeekDays(this.currWeekdaysEl_);
    this.renderDays(
      this.currentDate_.getFullYear(),
      this.currentDate_.getMonth(),
      this.currentDate_.getDate(),
      this.currDaysEl_);
  }
  renderTitle(year, month, target) {
    target.innerText = `${DMCCalendar.monthsOfYear[month]} ${year}`;
  }

  renderWeekDays(target) {
    let weekdays = [];
    for (let i=0; i<7; i++) {
      let day = DMCCalendar.daysOfWeek[(i+DMCCalendar.firstDayOfWeek) % 7];
      weekdays.push(`<div class="dmc-calendar__weekday">${day}</div>`);
    }
    target.innerHTML = weekdays.join('');
  }

  renderDays(year, month, day, target) {
    let days = [];
    let startPos = new Date(year, month, 1).getDay() - DMCCalendar.firstDayOfWeek;
    let daysInMonth = new Date(year, month+1, 0).getDate();

    for (let i=0; i<5; i++) {
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
    target.innerHTML = days.join('');
  }

  changeMonth(shift) {
    this.currentDate_.setMonth(this.currentDate_.getMonth() + shift);
    this.renderCurrentMonth();
    this.updateTarget();
  }

  changeDay(day) {
    this.currentDate_.setDate(day);
    this.renderDays(
      this.currentDate_.getFullYear(),
      this.currentDate_.getMonth(),
      this.currentDate_.getDate(),
      this.currDaysEl_);
    this.updateTarget();
  }

  updateTarget() {
    if (!this.targetEl_ || !this.targetEl_.dataset.dateFormat) {
      return;
    }
    this.targetEl_.value = DMCCalendar.formatDate(
      this.targetEl_.dataset.dateFormat,
      this.currentDate_
    );
  }
}

DMCCalendar.parseDate = (format, value) => {
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
};

DMCCalendar.formatDate = (format, value) => {
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

DMCCalendar.firstDayOfWeek = parseInt(get_format('FIRST_DAY_OF_WEEK'));

DMCCalendar.monthsOfYear = [
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

DMCCalendar.monthsOfYearAbbr = [
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

DMCCalendar.daysOfWeek = [
  pgettext('one letter Sunday', 'S'),
  pgettext('one letter Monday', 'M'),
  pgettext('one letter Tuesday', 'T'),
  pgettext('one letter Wednesday', 'W'),
  pgettext('one letter Thursday', 'T'),
  pgettext('one letter Friday', 'F'),
  pgettext('one letter Saturday', 'S'),
];

DMCCalendar.daysOfWeekAbbr = [
  pgettext('three letter Sunday', 'Sun'),
  pgettext('three letter Monday', 'Mon'),
  pgettext('three letter Tuesday', 'Tue'),
  pgettext('three letter Wednesday', 'Wed'),
  pgettext('three letter Thursday', 'Thu'),
  pgettext('three letter Friday', 'Fri'),
  pgettext('three letter Saturday', 'Sat'),
];

dmc.register('DMCCalendar', DMCCalendar);
