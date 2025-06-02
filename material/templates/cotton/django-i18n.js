/* eslint-env browser */
/* eslint camelcase: 0 */

/**
 * Django i18n JavaScript fallback functions.
 * Provides internationalization support when Django's jsi18n is not available.
 */

// Try to use Django's i18n functions if available, otherwise use fallbacks
let pluralidx = window.pluralidx;
let gettext = window.gettext;
let ngettext = window.ngettext;
let gettext_noop = window.gettext_noop;
let pgettext = window.pgettext;
let npgettext = window.npgettext;
let get_format = window.get_format;
let interpolate = window.interpolate;

// Initialize fallback functions if Django's i18n is not loaded
if (!window.django || !window.django.jsi18n_initialized) {
  // Simple plural index for English (0 for singular, 1 for plural)
  pluralidx = (count) => (count === 1) ? 0 : 1;
  
  // Simple gettext that returns the message as-is
  gettext = (msg) => msg;
  
  // Ngettext that chooses singular/plural based on count
  ngettext = (singular, plural, count) => (count === 1) ? singular : plural;
  
  // No-op gettext that returns the message unchanged
  gettext_noop = (msg) => msg;
  
  // Context-aware gettext that ignores context and returns message
  pgettext = (context, msg) => msg;
  
  // Context-aware ngettext that ignores context
  npgettext = (context, singular, plural, count) => (count === 1) ? singular : plural;

  // Default format strings for various date/time formats
  const formats = {
    'DATETIME_FORMAT': 'N j, Y, P',
    'DATETIME_INPUT_FORMATS': ['%Y-%m-%d %H:%M:%S'],
    'DATE_FORMAT': 'N j, Y',
    'DATE_INPUT_FORMATS': ['%Y-%m-%d'],
    'DECIMAL_SEPARATOR': '.',
    'FIRST_DAY_OF_WEEK': 0,
    'MONTH_DAY_FORMAT': 'F j',
    'NUMBER_GROUPING': 3,
    'SHORT_DATETIME_FORMAT': 'm/d/Y P',
    'SHORT_DATE_FORMAT': 'm/d/Y',
    'THOUSAND_SEPARATOR': ',',
    'TIME_FORMAT': 'P',
    'TIME_INPUT_FORMATS': ['%H:%M:%S'],
    'YEAR_MONTH_FORMAT': 'F Y',
  };

  // Get format string by type, with fallback to formatType itself
  get_format = (formatType) => {
    const value = formats[formatType];
    return (typeof value === 'undefined') ? formatType : value;
  };

  // String interpolation function supporting both named and positional parameters
  interpolate = (fmt, obj, named) => {
    if (named) {
      // Named parameter interpolation: %(name)s
      return fmt.replace(/%\(\w+\)s/g, (match) => {
        const key = match.slice(2, -2);
        return String(obj[key] || match);
      });
    } else {
      // Positional parameter interpolation: %s
      const objCopy = [...obj]; // Don't mutate the original array
      return fmt.replace(/%s/g, () => String(objCopy.shift() || ''));
    }
  };
}

export {
  gettext, pluralidx, ngettext, gettext_noop,
  pgettext, npgettext, get_format, interpolate,
};
