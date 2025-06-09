/* eslint camelcase: 0 */
import { gettext, pgettext, get_format } from '../../django-i18n';

/**
 * Date utilities for Material Design date components.
 * Provides Django-aware date formatting, parsing, and internationalization.
 */
export default class MaterialDateUtils {
  static firstDayOfWeek = parseInt(get_format('FIRST_DAY_OF_WEEK'), 10);

  static monthsOfYear = [
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

  static monthsOfYearAbbr = [
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

  static daysOfWeek = [
    pgettext('one letter Sunday', 'S'),
    pgettext('one letter Monday', 'M'),
    pgettext('one letter Tuesday', 'T'),
    pgettext('one letter Wednesday', 'W'),
    pgettext('one letter Thursday', 'T'),
    pgettext('one letter Friday', 'F'),
    pgettext('one letter Saturday', 'S'),
  ];

  static daysOfWeekAbbr = [
    pgettext('three letter Sunday', 'Sun'),
    pgettext('three letter Monday', 'Mon'),
    pgettext('three letter Tuesday', 'Tue'),
    pgettext('three letter Wednesday', 'Wed'),
    pgettext('three letter Thursday', 'Thu'),
    pgettext('three letter Friday', 'Fri'),
    pgettext('three letter Saturday', 'Sat'),
  ];

  /**
   * Formats a Date object using Django-style format strings.
   * @param {string} format - Django date format string (e.g., '%Y-%m-%d')
   * @param {Date} value - Date object to format
   * @returns {string} Formatted date string
   */
  static formatDate(format, value) {
    if (!(value instanceof Date) || isNaN(value)) {
      throw new Error('Invalid date provided to formatDate');
    }

    let result = '';
    for (let i = 0; i < format.length; i++) {
      if (format[i] === '%' && i + 1 < format.length) {
        switch (format[i + 1]) {
          case 'd':
            result += String(value.getDate()).padStart(2, '0');
            break;
          case 'm':
            result += String(value.getMonth() + 1).padStart(2, '0');
            break;
          case 'b':
            result += MaterialDateUtils.monthsOfYearAbbr[value.getMonth()];
            break;
          case 'Y':
            result += value.getFullYear();
            break;
          case 'I':
            const twelveHour = value.getHours() % 12 || 12;
            result += String(twelveHour).padStart(2, '0');
            break;
          case 'H':
            result += String(value.getHours()).padStart(2, '0');
            break;
          case 'M':
            result += String(value.getMinutes()).padStart(2, '0');
            break;
          case 'S':
            result += String(value.getSeconds()).padStart(2, '0');
            break;
          case 'p':
            result += value.getHours() >= 12 ? 'pm' : 'am';
            break;
          default:
            // Unknown format code, include literally
            result += format[i] + format[i + 1];
        }
        i++; // Skip next character as it's part of format code
      } else {
        result += format[i];
      }
    }
    return result;
  }

  /**
   * Parses a date string using Django-style format strings.
   * @param {string} format - Django date format string
   * @param {string} value - Date string to parse
   * @returns {Date} Parsed Date object
   */
  static parseDateTime(format, value) {
    if (!format || !value) {
      throw new Error('Format and value are required for parsing');
    }

    const splitFormat = format.split(/[.\-/:,\s]+/);
    const dateParts = value.split(/[.\-/:,\s]+/);
    
    if (splitFormat.length !== dateParts.length) {
      throw new Error('Format and value structure mismatch');
    }

    let day = 1;
    let month = 0;
    let year = new Date().getFullYear();
    let hour = 0;
    let minute = 0;
    let second = 0;

    for (let i = 0; i < splitFormat.length; i++) {
      const formatPart = splitFormat[i];
      const datePart = dateParts[i];

      if (!datePart) continue;

      switch (formatPart) {
        case '%d':
          day = parseInt(datePart, 10);
          if (isNaN(day) || day < 1 || day > 31) {
            throw new Error(`Invalid day: ${datePart}`);
          }
          break;
        case '%m':
          month = parseInt(datePart, 10) - 1;
          if (isNaN(month) || month < 0 || month > 11) {
            throw new Error(`Invalid month: ${datePart}`);
          }
          break;
        case '%Y':
          year = parseInt(datePart, 10);
          if (isNaN(year)) {
            throw new Error(`Invalid year: ${datePart}`);
          }
          break;
        case '%b':
          month = MaterialDateUtils.monthsOfYearAbbr.indexOf(datePart);
          if (month === -1) {
            throw new Error(`Invalid month abbreviation: ${datePart}`);
          }
          break;
        case '%H':
          hour = parseInt(datePart, 10);
          if (isNaN(hour) || hour < 0 || hour > 23) {
            throw new Error(`Invalid hour: ${datePart}`);
          }
          break;
        case '%M':
          minute = parseInt(datePart, 10);
          if (isNaN(minute) || minute < 0 || minute > 59) {
            throw new Error(`Invalid minute: ${datePart}`);
          }
          break;
        case '%S':
          second = parseInt(datePart, 10);
          if (isNaN(second) || second < 0 || second > 59) {
            throw new Error(`Invalid second: ${datePart}`);
          }
          break;
      }
    }

    const result = new Date(year, month, day, hour, minute, second);
    
    // Validate the constructed date
    if (isNaN(result.getTime())) {
      throw new Error('Invalid date constructed from parsed values');
    }

    return result;
  }

  /**
   * Returns the number of days in a given month and year.
   * @param {number} year - Full year (e.g., 2024)
   * @param {number} month - Month index (0-11)
   * @returns {number} Number of days in the month
   */
  static daysInMonth(year, month) {
    if (typeof year !== 'number' || typeof month !== 'number') {
      throw new Error('Year and month must be numbers');
    }
    if (month < 0 || month > 11) {
      throw new Error('Month must be between 0 and 11');
    }
    return new Date(year, month + 1, 0).getDate();
  }

  /**
   * Checks if a year is a leap year.
   * @param {number} year - Full year to check
   * @returns {boolean} True if leap year
   */
  static isLeapYear(year) {
    return year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  }

  /**
   * Gets the day of week for the first day of a month.
   * @param {number} year - Full year
   * @param {number} month - Month index (0-11)
   * @returns {number} Day of week (0-6, where 0 is Sunday)
   */
  static getFirstDayOfMonth(year, month) {
    return new Date(year, month, 1).getDay();
  }

  /**
   * Validates if a date is within reasonable bounds.
   * @param {Date} date - Date to validate
   * @returns {boolean} True if date is valid and reasonable
   */
  static isValidDate(date) {
    if (!(date instanceof Date)) return false;
    if (isNaN(date.getTime())) return false;
    
    // Check for reasonable date range (1900-2100)
    const year = date.getFullYear();
    return year >= 1900 && year <= 2100;
  }
}
