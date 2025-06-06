(() => {
  // material/templates/cotton/django-i18n.js
  var pluralidx = window.pluralidx;
  var gettext = window.gettext;
  var ngettext = window.ngettext;
  var gettext_noop = window.gettext_noop;
  var pgettext = window.pgettext;
  var npgettext = window.npgettext;
  var get_format = window.get_format;
  var interpolate = window.interpolate;
  if (!window.django || !window.django.jsi18n_initialized) {
    pluralidx = (count) => count === 1 ? 0 : 1;
    gettext = (msg) => msg;
    ngettext = (singular, plural, count) => count === 1 ? singular : plural;
    gettext_noop = (msg) => msg;
    pgettext = (context, msg) => msg;
    npgettext = (context, singular, plural, count) => count === 1 ? singular : plural;
    const formats = {
      "DATETIME_FORMAT": "N j, Y, P",
      "DATETIME_INPUT_FORMATS": ["%Y-%m-%d %H:%M:%S"],
      "DATE_FORMAT": "N j, Y",
      "DATE_INPUT_FORMATS": ["%Y-%m-%d"],
      "DECIMAL_SEPARATOR": ".",
      "FIRST_DAY_OF_WEEK": 0,
      "MONTH_DAY_FORMAT": "F j",
      "NUMBER_GROUPING": 3,
      "SHORT_DATETIME_FORMAT": "m/d/Y P",
      "SHORT_DATE_FORMAT": "m/d/Y",
      "THOUSAND_SEPARATOR": ",",
      "TIME_FORMAT": "P",
      "TIME_INPUT_FORMATS": ["%H:%M:%S"],
      "YEAR_MONTH_FORMAT": "F Y"
    };
    get_format = (formatType) => {
      const value = formats[formatType];
      return typeof value === "undefined" ? formatType : value;
    };
    interpolate = (fmt, obj, named) => {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, (match) => {
          const key = match.slice(2, -2);
          return String(obj[key] || match);
        });
      } else {
        const objCopy = [...obj];
        return fmt.replace(/%s/g, () => String(objCopy.shift() || ""));
      }
    };
  }

  // material/templates/cotton/nav/script.js
  up.compiler("[up-nav-toggle]", function(element) {
    element.addEventListener("click", function() {
      document.body.toggleAttribute("data-nav-open");
    });
  });
  up.compiler("[up-nav-toggle-off]", function(element) {
    element.addEventListener("click", function() {
      document.body.removeAttribute("data-nav-open");
    });
  });

  // material/templates/cotton/forms/textarea/script.js
  up.compiler("[up-auto-grow]", function(element) {
    requestAnimationFrame(function() {
      adjustHeight(element);
    });
    element.addEventListener("input", function() {
      adjustHeight(element);
    });
    function adjustHeight(el) {
      el.style.height = "auto";
      el.style.height = el.scrollHeight + 2 + "px";
    }
  });

  // material/templates/cotton/button/script.js
  up.compiler("[up-ripple]", function(elementWithRipple) {
    elementWithRipple.addEventListener("pointerdown", (mouseEvent) => {
      elementWithRipple.style.setProperty("--ripple-x", `${mouseEvent.offsetX}px`);
      elementWithRipple.style.setProperty("--ripple-y", `${mouseEvent.offsetY}px`);
    });
  });

  // material/templates/cotton/menu/script.js
  up.compiler("[up-menu]", function(menu) {
    const anchorSelector = menu.dataset.anchor;
    const placement = menu.dataset.placement || "bottom-start";
    if (!anchorSelector) return;
    const anchor = document.querySelector(anchorSelector);
    if (!anchor) return;
    let documentClickHandler = null;
    let documentKeyHandler = null;
    let windowResizeHandler = null;
    let documentScrollHandler = null;
    function positionMenu() {
      const anchorRect = anchor.getBoundingClientRect();
      const menuRect = menu.getBoundingClientRect();
      const viewport = {
        width: window.innerWidth,
        height: window.innerHeight
      };
      let top, left;
      let actualPlacement = placement;
      const spaceBelow = viewport.height - anchorRect.bottom;
      const spaceAbove = anchorRect.top;
      if ((placement.startsWith("bottom") || placement === "bottom-start") && spaceBelow < menuRect.height && spaceAbove > menuRect.height) {
        actualPlacement = placement.replace("bottom", "top");
      }
      const anchorCenter = anchorRect.left + anchorRect.width / 2;
      const onRightSide = anchorCenter > viewport.width / 2;
      if (onRightSide && anchorRect.right > menuRect.width) {
        actualPlacement = actualPlacement.replace("start", "end");
      }
      switch (actualPlacement) {
        case "top-start":
          top = -menuRect.height;
          left = 0;
          break;
        case "top-end":
          top = -menuRect.height;
          left = anchorRect.width - menuRect.width;
          break;
        case "bottom-end":
          top = anchorRect.height;
          left = anchorRect.width - menuRect.width;
          break;
        case "bottom-start":
        default:
          top = anchorRect.height;
          left = 0;
          break;
      }
      if (left < 0) left = 0;
      if (left + menuRect.width > viewport.width) {
        left = Math.max(0, anchorRect.width - menuRect.width);
      }
      menu.style.left = `${left}px`;
      menu.style.top = `${top}px`;
    }
    function showMenu() {
      menu.classList.remove("hidden");
      documentClickHandler = function(e) {
        if (!menu.contains(e.target) && !anchor.contains(e.target)) {
          hideMenu();
        }
      };
      documentKeyHandler = function(e) {
        if (e.key === "Escape" && !menu.classList.contains("hidden")) {
          hideMenu();
          anchor.focus();
        }
      };
      windowResizeHandler = function() {
        if (!menu.classList.contains("hidden")) {
          positionMenu();
        }
      };
      document.addEventListener("click", documentClickHandler);
      document.addEventListener("keydown", documentKeyHandler);
      window.addEventListener("resize", windowResizeHandler);
      requestAnimationFrame(() => {
        positionMenu();
        const firstItem = menu.querySelector("[up-menu-item]");
        if (firstItem) {
          firstItem.focus();
        }
      });
    }
    function hideMenu() {
      menu.classList.add("hidden");
      if (documentClickHandler) {
        document.removeEventListener("click", documentClickHandler);
        documentClickHandler = null;
      }
      if (documentKeyHandler) {
        document.removeEventListener("keydown", documentKeyHandler);
        documentKeyHandler = null;
      }
      if (windowResizeHandler) {
        window.removeEventListener("resize", windowResizeHandler);
        windowResizeHandler = null;
      }
    }
    function toggleMenu() {
      if (menu.classList.contains("hidden")) {
        showMenu();
      } else {
        hideMenu();
      }
    }
    menu.showMenu = showMenu;
    menu.hideMenu = hideMenu;
    menu.toggleMenu = toggleMenu;
    anchor.addEventListener("click", function(e) {
      e.preventDefault();
      toggleMenu();
    });
  });
  up.compiler("[up-menu-item]", function(menuItem) {
    const menu = menuItem.closest("[up-menu]");
    if (!menu) return;
    menuItem.addEventListener("keydown", function(e) {
      const items = Array.from(menu.querySelectorAll("[up-menu-item]"));
      const currentIndex = items.indexOf(menuItem);
      switch (e.key) {
        case "ArrowDown":
          e.preventDefault();
          const nextIndex = (currentIndex + 1) % items.length;
          items[nextIndex].focus();
          break;
        case "ArrowUp":
          e.preventDefault();
          const prevIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
          items[prevIndex].focus();
          break;
        case "Enter":
        case " ":
          e.preventDefault();
          menuItem.click();
          break;
        case "Tab":
          menu.hideMenu();
          break;
      }
    });
    menuItem.addEventListener("click", function() {
      setTimeout(() => {
        menu.hideMenu();
      }, 100);
    });
  });

  // material/templates/cotton/forms/select/script.js
  up.compiler("[up-select-trigger]", function(trigger) {
    const container = trigger.closest(".group");
    const menu = container.querySelector("[up-select-menu]");
    const arrow = container.querySelector("[up-select-arrow]");
    if (!menu) return;
    let documentClickHandler = null;
    let documentKeyHandler = null;
    let windowResizeHandler = null;
    let typeaheadString = "";
    let typeaheadTimeout = null;
    function findOptionByPrefix(prefix) {
      const options = menu.querySelectorAll("[up-select-option]");
      const normalizedPrefix = prefix.toLowerCase();
      for (const option of options) {
        const text = (option.textContent || "").trim().toLowerCase();
        if (text.startsWith(normalizedPrefix)) {
          return option;
        }
      }
      return null;
    }
    function handleTypeahead(char) {
      if (typeaheadTimeout) {
        clearTimeout(typeaheadTimeout);
      }
      typeaheadString += char.toLowerCase();
      const matchingOption = findOptionByPrefix(typeaheadString);
      if (matchingOption) {
        matchingOption.focus();
        matchingOption.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      typeaheadTimeout = setTimeout(() => {
        typeaheadString = "";
      }, 1e3);
    }
    function positionMenu() {
      const triggerRect = trigger.getBoundingClientRect();
      const menuRect = menu.getBoundingClientRect();
      const viewport = {
        width: window.innerWidth,
        height: window.innerHeight
      };
      let top, left;
      const placement = menu.dataset.placement || "bottom-start";
      let actualPlacement = placement;
      const spaceBelow = viewport.height - triggerRect.bottom;
      const spaceAbove = triggerRect.top;
      if (placement.startsWith("bottom") && spaceBelow < menuRect.height && spaceAbove > menuRect.height) {
        actualPlacement = placement.replace("bottom", "top");
      }
      switch (actualPlacement) {
        case "top-start":
          top = -menuRect.height;
          left = 0;
          break;
        case "bottom-start":
        default:
          top = triggerRect.height;
          left = 0;
          break;
      }
      if (left < 0) left = 0;
      if (left + menuRect.width > viewport.width) {
        left = Math.max(0, triggerRect.width - menuRect.width);
      }
      menu.style.left = `${left}px`;
      menu.style.top = `${top}px`;
      menu.style.minWidth = `${triggerRect.width}px`;
    }
    function showMenu() {
      menu.classList.remove("hidden");
      trigger.setAttribute("aria-expanded", "true");
      trigger.setAttribute("data-select-open", "true");
      if (arrow) {
        arrow.style.transform = "rotate(180deg)";
      }
      documentClickHandler = function(e) {
        if (!menu.contains(e.target) && !trigger.contains(e.target)) {
          hideMenu();
        }
      };
      documentKeyHandler = function(e) {
        if (e.key === "Escape" && !menu.classList.contains("hidden")) {
          hideMenu();
          trigger.focus();
        } else if (!menu.classList.contains("hidden") && e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
          e.preventDefault();
          handleTypeahead(e.key);
        }
      };
      windowResizeHandler = function() {
        if (!menu.classList.contains("hidden")) {
          positionMenu();
        }
      };
      document.addEventListener("click", documentClickHandler);
      document.addEventListener("keydown", documentKeyHandler);
      window.addEventListener("resize", windowResizeHandler);
      requestAnimationFrame(() => {
        positionMenu();
        const selectedItem = menu.querySelector('[up-select-option][aria-selected="true"]');
        const firstItem = menu.querySelector("[up-select-option]");
        const itemToFocus = selectedItem || firstItem;
        if (itemToFocus) {
          itemToFocus.focus();
        }
      });
    }
    function hideMenu() {
      menu.classList.add("hidden");
      trigger.setAttribute("aria-expanded", "false");
      trigger.removeAttribute("data-select-open");
      if (arrow) {
        arrow.style.transform = "rotate(0deg)";
      }
      if (documentClickHandler) {
        document.removeEventListener("click", documentClickHandler);
        documentClickHandler = null;
      }
      if (documentKeyHandler) {
        document.removeEventListener("keydown", documentKeyHandler);
        documentKeyHandler = null;
      }
      if (windowResizeHandler) {
        window.removeEventListener("resize", windowResizeHandler);
        windowResizeHandler = null;
      }
    }
    function toggleMenu() {
      if (menu.classList.contains("hidden")) {
        showMenu();
      } else {
        hideMenu();
      }
    }
    menu.showMenu = showMenu;
    menu.hideMenu = hideMenu;
    menu.toggleMenu = toggleMenu;
    trigger.handleTypeahead = handleTypeahead;
    trigger.addEventListener("click", function(e) {
      e.preventDefault();
      toggleMenu();
    });
    trigger.addEventListener("keydown", function(e) {
      switch (e.key) {
        case "Enter":
        case " ":
        case "ArrowDown":
        case "ArrowUp":
          e.preventDefault();
          if (menu.classList.contains("hidden")) {
            showMenu();
          }
          break;
        case "Escape":
          if (!menu.classList.contains("hidden")) {
            e.preventDefault();
            hideMenu();
            trigger.focus();
          }
          break;
      }
    });
    trigger.addEventListener("selectstart", function(e) {
      e.preventDefault();
    });
  });
  up.compiler("[up-select-option]", function(option) {
    const menu = option.closest("[up-select-menu]");
    const container = menu?.closest(".group");
    const trigger = container?.querySelector("[up-select-trigger]");
    if (!trigger || !menu) return;
    option.addEventListener("click", function(e) {
      e.preventDefault();
      const value = option.dataset.value;
      const displayText = option.textContent.trim();
      const finalDisplayText = value === "" || value === "null" || value === "undefined" ? "" : displayText;
      trigger.value = finalDisplayText;
      trigger.setAttribute("value", finalDisplayText);
      const hiddenInput = container.querySelector("input[up-select-value]");
      if (hiddenInput) {
        hiddenInput.value = value === "" || value === "null" || value === "undefined" ? "" : value;
      }
      const allOptions = menu.querySelectorAll("[up-select-option]");
      allOptions.forEach((opt) => {
        opt.classList.remove("bg-on-surface/12");
        opt.setAttribute("aria-selected", "false");
      });
      option.classList.add("bg-on-surface/12");
      option.setAttribute("aria-selected", "true");
      const changeEvent = new Event("change", { bubbles: true });
      trigger.dispatchEvent(changeEvent);
      setTimeout(() => {
        if (menu.hideMenu) {
          menu.hideMenu();
        }
        trigger.focus();
      }, 100);
    });
    option.addEventListener("keydown", function(e) {
      const items = Array.from(menu.querySelectorAll("[up-select-option]"));
      const currentIndex = items.indexOf(option);
      switch (e.key) {
        case "ArrowDown":
          e.preventDefault();
          const nextIndex = (currentIndex + 1) % items.length;
          items[nextIndex].focus();
          break;
        case "ArrowUp":
          e.preventDefault();
          const prevIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
          items[prevIndex].focus();
          break;
        case "Enter":
        case " ":
          e.preventDefault();
          option.click();
          break;
        case "Tab":
          if (menu.hideMenu) {
            menu.hideMenu();
          }
          break;
        default:
          if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
            e.preventDefault();
            if (menu.closest(".group").querySelector("[up-select-trigger]")) {
              const selectTrigger = menu.closest(".group").querySelector("[up-select-trigger]");
              if (selectTrigger.handleTypeahead) {
                selectTrigger.handleTypeahead(e.key);
              }
            }
          }
          break;
      }
    });
    const triggerValue = trigger.value;
    const optionValue = option.dataset.value;
    if (triggerValue === optionValue || triggerValue === option.textContent.trim()) {
      option.classList.add("bg-on-surface/12");
      option.setAttribute("aria-selected", "true");
    } else {
      option.setAttribute("aria-selected", "false");
    }
  });

  // material/templates/cotton/date/date-utils.js
  var MaterialDateUtils = class _MaterialDateUtils {
    static firstDayOfWeek = parseInt(get_format("FIRST_DAY_OF_WEEK"), 10);
    static monthsOfYear = [
      gettext("January"),
      gettext("February"),
      gettext("March"),
      gettext("April"),
      gettext("May"),
      gettext("June"),
      gettext("July"),
      gettext("August"),
      gettext("September"),
      gettext("October"),
      gettext("November"),
      gettext("December")
    ];
    static monthsOfYearAbbr = [
      pgettext("three letter January", "Jan"),
      pgettext("three letter February", "Feb"),
      pgettext("three letter March", "Mar"),
      pgettext("three letter April", "Apr"),
      pgettext("three letter May", "May"),
      pgettext("three letter June", "Jun"),
      pgettext("three letter July", "Jul"),
      pgettext("three letter August", "Aug"),
      pgettext("three letter September", "Sep"),
      pgettext("three letter October", "Oct"),
      pgettext("three letter November", "Nov"),
      pgettext("three letter December", "Dec")
    ];
    static daysOfWeek = [
      pgettext("one letter Sunday", "S"),
      pgettext("one letter Monday", "M"),
      pgettext("one letter Tuesday", "T"),
      pgettext("one letter Wednesday", "W"),
      pgettext("one letter Thursday", "T"),
      pgettext("one letter Friday", "F"),
      pgettext("one letter Saturday", "S")
    ];
    static daysOfWeekAbbr = [
      pgettext("three letter Sunday", "Sun"),
      pgettext("three letter Monday", "Mon"),
      pgettext("three letter Tuesday", "Tue"),
      pgettext("three letter Wednesday", "Wed"),
      pgettext("three letter Thursday", "Thu"),
      pgettext("three letter Friday", "Fri"),
      pgettext("three letter Saturday", "Sat")
    ];
    /**
     * Formats a Date object using Django-style format strings.
     * @param {string} format - Django date format string (e.g., '%Y-%m-%d')
     * @param {Date} value - Date object to format
     * @returns {string} Formatted date string
     */
    static formatDate(format, value) {
      if (!(value instanceof Date) || isNaN(value)) {
        throw new Error("Invalid date provided to formatDate");
      }
      let result = "";
      for (let i = 0; i < format.length; i++) {
        if (format[i] === "%" && i + 1 < format.length) {
          switch (format[i + 1]) {
            case "d":
              result += String(value.getDate()).padStart(2, "0");
              break;
            case "m":
              result += String(value.getMonth() + 1).padStart(2, "0");
              break;
            case "b":
              result += _MaterialDateUtils.monthsOfYearAbbr[value.getMonth()];
              break;
            case "Y":
              result += value.getFullYear();
              break;
            case "I":
              const twelveHour = value.getHours() % 12 || 12;
              result += String(twelveHour).padStart(2, "0");
              break;
            case "H":
              result += String(value.getHours()).padStart(2, "0");
              break;
            case "M":
              result += String(value.getMinutes()).padStart(2, "0");
              break;
            case "S":
              result += String(value.getSeconds()).padStart(2, "0");
              break;
            case "p":
              result += value.getHours() >= 12 ? "pm" : "am";
              break;
            default:
              result += format[i] + format[i + 1];
          }
          i++;
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
        throw new Error("Format and value are required for parsing");
      }
      const splitFormat = format.split(/[.\-/:,\s]+/);
      const dateParts = value.split(/[.\-/:,\s]+/);
      if (splitFormat.length !== dateParts.length) {
        throw new Error("Format and value structure mismatch");
      }
      let day = 1;
      let month = 0;
      let year = (/* @__PURE__ */ new Date()).getFullYear();
      let hour = 0;
      let minute = 0;
      let second = 0;
      for (let i = 0; i < splitFormat.length; i++) {
        const formatPart = splitFormat[i];
        const datePart = dateParts[i];
        if (!datePart) continue;
        switch (formatPart) {
          case "%d":
            day = parseInt(datePart, 10);
            if (isNaN(day) || day < 1 || day > 31) {
              throw new Error(`Invalid day: ${datePart}`);
            }
            break;
          case "%m":
            month = parseInt(datePart, 10) - 1;
            if (isNaN(month) || month < 0 || month > 11) {
              throw new Error(`Invalid month: ${datePart}`);
            }
            break;
          case "%Y":
            year = parseInt(datePart, 10);
            if (isNaN(year)) {
              throw new Error(`Invalid year: ${datePart}`);
            }
            break;
          case "%b":
            month = _MaterialDateUtils.monthsOfYearAbbr.indexOf(datePart);
            if (month === -1) {
              throw new Error(`Invalid month abbreviation: ${datePart}`);
            }
            break;
          case "%H":
            hour = parseInt(datePart, 10);
            if (isNaN(hour) || hour < 0 || hour > 23) {
              throw new Error(`Invalid hour: ${datePart}`);
            }
            break;
          case "%M":
            minute = parseInt(datePart, 10);
            if (isNaN(minute) || minute < 0 || minute > 59) {
              throw new Error(`Invalid minute: ${datePart}`);
            }
            break;
          case "%S":
            second = parseInt(datePart, 10);
            if (isNaN(second) || second < 0 || second > 59) {
              throw new Error(`Invalid second: ${datePart}`);
            }
            break;
        }
      }
      const result = new Date(year, month, day, hour, minute, second);
      if (isNaN(result.getTime())) {
        throw new Error("Invalid date constructed from parsed values");
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
      if (typeof year !== "number" || typeof month !== "number") {
        throw new Error("Year and month must be numbers");
      }
      if (month < 0 || month > 11) {
        throw new Error("Month must be between 0 and 11");
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
      const year = date.getFullYear();
      return year >= 1900 && year <= 2100;
    }
  };

  // material/templates/cotton/date/script.js
  up.compiler("[data-calendar]", function(element) {
    const color = element.dataset.color || "primary";
    const format = element.dataset.format || "%Y-%m-%d";
    const header = element.dataset.header === "true";
    const actions = element.dataset.actions === "true";
    const disabled = element.dataset.disabled === "true";
    let currentYear = (/* @__PURE__ */ new Date()).getFullYear();
    let currentMonth = (/* @__PURE__ */ new Date()).getMonth();
    let selectedDate = null;
    let isYearPickerOpen = false;
    if (element.dataset.value) {
      try {
        selectedDate = MaterialDateUtils.parseDateTime(format, element.dataset.value);
        currentYear = selectedDate.getFullYear();
        currentMonth = selectedDate.getMonth();
      } catch (e) {
        console.warn("Invalid initial date value:", element.dataset.value);
      }
    }
    const monthYearEl = element.querySelector("[data-month-year]");
    const yearPicker = element.querySelector("[data-year-picker]");
    const weekdaysContainer = element.querySelector("[data-weekdays]");
    const daysContainer = element.querySelector("[data-calendar-days]");
    const prevButton = element.querySelector("[data-prev-month]");
    const nextButton = element.querySelector("[data-next-month]");
    const cancelButton = element.querySelector("[data-calendar-cancel]");
    const acceptButton = element.querySelector("[data-calendar-accept]");
    const selectedWeekdayEl = element.querySelector("[data-selected-weekday]");
    const selectedDateEl = element.querySelector("[data-selected-date]");
    const weekdayElements = element.querySelectorAll("[data-weekday]");
    weekdayElements.forEach((el, index) => {
      const dayIndex = (index + MaterialDateUtils.firstDayOfWeek) % 7;
      el.textContent = MaterialDateUtils.daysOfWeek[dayIndex];
    });
    function updateHeader() {
      if (!header || !selectedDate) return;
      if (selectedWeekdayEl) {
        selectedWeekdayEl.textContent = MaterialDateUtils.daysOfWeekAbbr[selectedDate.getDay()] + ",";
      }
      if (selectedDateEl) {
        selectedDateEl.textContent = MaterialDateUtils.monthsOfYearAbbr[selectedDate.getMonth()] + " " + selectedDate.getDate();
      }
    }
    function renderCalendar() {
      if (!monthYearEl || !daysContainer) return;
      monthYearEl.textContent = `${MaterialDateUtils.monthsOfYear[currentMonth]} ${currentYear}`;
      daysContainer.innerHTML = "";
      const firstDay = MaterialDateUtils.getFirstDayOfMonth(currentYear, currentMonth);
      const daysInMonth = MaterialDateUtils.daysInMonth(currentYear, currentMonth);
      const startPos = (firstDay - MaterialDateUtils.firstDayOfWeek + 7) % 7;
      for (let week = 0; week < 6; week++) {
        for (let day = 0; day < 7; day++) {
          const cell = week * 7 + day;
          const dayNumber = cell >= startPos && cell < daysInMonth + startPos ? cell - startPos + 1 : "";
          const dayEl = document.createElement("div");
          dayEl.className = "flex justify-center items-center h-9";
          if (dayNumber) {
            const span = document.createElement("span");
            const isSelected = selectedDate && selectedDate.getFullYear() === currentYear && selectedDate.getMonth() === currentMonth && selectedDate.getDate() === dayNumber;
            if (isSelected) {
              span.className = `inline-block rounded-full w-9 h-9 leading-9 text-xs bg-${color} text-on-${color} cursor-pointer transition-colors`;
              if (!disabled) {
                span.className += ` hover:bg-${color}`;
              }
            } else {
              span.className = `inline-block rounded-full w-9 h-9 leading-9 text-xs text-on-surface cursor-pointer transition-colors`;
              if (!disabled) {
                span.className += ` hover:bg-surface-variant`;
              }
            }
            span.textContent = dayNumber;
            span.dataset.day = dayNumber;
            dayEl.appendChild(span);
          }
          daysContainer.appendChild(dayEl);
        }
      }
      updateHeader();
    }
    function showYearPicker() {
      if (!yearPicker || disabled) return;
      isYearPickerOpen = true;
      if (weekdaysContainer) weekdaysContainer.classList.add("hidden");
      daysContainer.classList.add("hidden");
      yearPicker.classList.remove("hidden");
      yearPicker.innerHTML = "";
      const startYear = currentYear - 11;
      const endYear = currentYear + 12;
      for (let year = startYear; year <= endYear; year++) {
        const yearButton = document.createElement("button");
        yearButton.type = "button";
        yearButton.className = "h-9 px-2 py-1 text-sm rounded transition-colors focus:outline-none focus:ring-2 focus:ring-primary/20";
        yearButton.textContent = year;
        if (year === currentYear) {
          yearButton.className += ` bg-${color} text-on-${color}`;
        } else {
          yearButton.className += " text-on-surface hover:bg-surface-variant";
        }
        yearButton.addEventListener("click", () => selectYear(year));
        yearPicker.appendChild(yearButton);
      }
      const currentYearIndex = currentYear - startYear;
      const currentYearButton = yearPicker.querySelector(`button:nth-child(${currentYearIndex + 1})`);
      if (currentYearButton) {
        currentYearButton.focus();
      }
    }
    function hideYearPicker() {
      if (!yearPicker) return;
      isYearPickerOpen = false;
      if (weekdaysContainer) weekdaysContainer.classList.remove("hidden");
      daysContainer.classList.remove("hidden");
      yearPicker.classList.add("hidden");
    }
    function selectYear(year) {
      currentYear = year;
      renderCalendar();
      hideYearPicker();
      monthYearEl?.focus();
    }
    function toggleYearPicker() {
      if (isYearPickerOpen) {
        hideYearPicker();
      } else {
        showYearPicker();
      }
    }
    function changeMonth(delta) {
      if (disabled) return;
      currentMonth += delta;
      if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
      } else if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
      }
      renderCalendar();
      if (selectedDate) {
        const newDay = Math.min(selectedDate.getDate(), MaterialDateUtils.daysInMonth(currentYear, currentMonth));
        selectDate(newDay);
      }
    }
    function selectDate(day) {
      if (disabled) return;
      const newDate = new Date(currentYear, currentMonth, day);
      selectedDate = newDate;
      const formattedDate = MaterialDateUtils.formatDate(format, newDate);
      element.dataset.value = formattedDate;
      const changeEvent = new CustomEvent("calendar:change", {
        detail: { date: newDate, formatted: formattedDate },
        bubbles: true
      });
      element.dispatchEvent(changeEvent);
      renderCalendar();
    }
    function onDayClick(event) {
      if (disabled || event.target.tagName !== "SPAN") return;
      const day = parseInt(event.target.dataset.day);
      if (!isNaN(day)) {
        selectDate(day);
      }
    }
    function onMonthYearClick() {
      if (!disabled) {
        toggleYearPicker();
      }
    }
    function onPrevMonth() {
      changeMonth(-1);
    }
    function onNextMonth() {
      changeMonth(1);
    }
    function onCancel() {
      const cancelEvent = new CustomEvent("calendar:cancel", { bubbles: true });
      element.dispatchEvent(cancelEvent);
    }
    function onAccept() {
      const acceptEvent = new CustomEvent("calendar:accept", {
        detail: { date: selectedDate, formatted: selectedDate ? MaterialDateUtils.formatDate(format, selectedDate) : null },
        bubbles: true
      });
      element.dispatchEvent(acceptEvent);
    }
    function onPrevButtonKeyDown(event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        onPrevMonth();
      }
    }
    function onNextButtonKeyDown(event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        onNextMonth();
      }
    }
    function onMonthYearKeyDown(event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        toggleYearPicker();
      } else if (event.key === "Escape" && isYearPickerOpen) {
        event.preventDefault();
        hideYearPicker();
      }
    }
    if (daysContainer) {
      daysContainer.addEventListener("click", onDayClick);
    }
    if (monthYearEl) {
      monthYearEl.addEventListener("click", onMonthYearClick);
      monthYearEl.addEventListener("keydown", onMonthYearKeyDown);
    }
    if (prevButton) {
      prevButton.addEventListener("click", onPrevMonth);
      prevButton.addEventListener("keydown", onPrevButtonKeyDown);
    }
    if (nextButton) {
      nextButton.addEventListener("click", onNextMonth);
      nextButton.addEventListener("keydown", onNextButtonKeyDown);
    }
    if (cancelButton) {
      cancelButton.addEventListener("click", onCancel);
    }
    if (acceptButton) {
      acceptButton.addEventListener("click", onAccept);
    }
    function onKeyDown(event) {
      if (disabled) return;
      if (event.target === cancelButton || event.target === acceptButton || isYearPickerOpen) {
        return;
      }
      switch (event.key) {
        case "ArrowLeft":
          event.preventDefault();
          if (selectedDate) {
            const newDay = selectedDate.getDate() - 1;
            if (newDay >= 1) {
              selectDate(newDay);
            } else {
              changeMonth(-1);
              const prevMonthDays = MaterialDateUtils.daysInMonth(currentYear, currentMonth);
              selectDate(prevMonthDays);
            }
          }
          break;
        case "ArrowRight":
          event.preventDefault();
          if (selectedDate) {
            const maxDays = MaterialDateUtils.daysInMonth(currentYear, currentMonth);
            const newDay = selectedDate.getDate() + 1;
            if (newDay <= maxDays) {
              selectDate(newDay);
            } else {
              changeMonth(1);
              selectDate(1);
            }
          }
          break;
        case "ArrowUp":
          event.preventDefault();
          if (selectedDate) {
            const newDay = selectedDate.getDate() - 7;
            if (newDay >= 1) {
              selectDate(newDay);
            } else {
              changeMonth(-1);
              const prevMonthDays = MaterialDateUtils.daysInMonth(currentYear, currentMonth);
              selectDate(Math.max(1, prevMonthDays + newDay));
            }
          }
          break;
        case "ArrowDown":
          event.preventDefault();
          if (selectedDate) {
            const maxDays = MaterialDateUtils.daysInMonth(currentYear, currentMonth);
            const newDay = selectedDate.getDate() + 7;
            if (newDay <= maxDays) {
              selectDate(newDay);
            } else {
              changeMonth(1);
              selectDate(Math.min(MaterialDateUtils.daysInMonth(currentYear, currentMonth), newDay - maxDays));
            }
          }
          break;
        case "Enter":
        case " ":
          event.preventDefault();
          if (selectedDate && acceptButton) {
            onAccept();
          }
          break;
        case "Escape":
          event.preventDefault();
          if (isYearPickerOpen) {
            hideYearPicker();
          } else if (cancelButton) {
            onCancel();
          }
          break;
      }
    }
    element.addEventListener("keydown", onKeyDown);
    element.setAttribute("tabindex", "0");
    element.materialCalendar = {
      getValue: () => selectedDate ? MaterialDateUtils.formatDate(format, selectedDate) : null,
      setValue: (value) => {
        if (!value) {
          selectedDate = null;
        } else {
          try {
            selectedDate = MaterialDateUtils.parseDateTime(format, value);
            currentYear = selectedDate.getFullYear();
            currentMonth = selectedDate.getMonth();
          } catch (e) {
            console.warn("Invalid date value:", value);
            return;
          }
        }
        element.dataset.value = value || "";
        renderCalendar();
      },
      getDate: () => selectedDate,
      setDate: (date) => {
        if (date instanceof Date && MaterialDateUtils.isValidDate(date)) {
          selectedDate = date;
          currentYear = date.getFullYear();
          currentMonth = date.getMonth();
          element.dataset.value = MaterialDateUtils.formatDate(format, date);
          renderCalendar();
        }
      }
    };
    renderCalendar();
    return function() {
      if (daysContainer) {
        daysContainer.removeEventListener("click", onDayClick);
      }
      if (monthYearEl) {
        monthYearEl.removeEventListener("click", onMonthYearClick);
        monthYearEl.removeEventListener("keydown", onMonthYearKeyDown);
      }
      if (prevButton) {
        prevButton.removeEventListener("click", onPrevMonth);
        prevButton.removeEventListener("keydown", onPrevButtonKeyDown);
      }
      if (nextButton) {
        nextButton.removeEventListener("click", onNextMonth);
        nextButton.removeEventListener("keydown", onNextButtonKeyDown);
      }
      if (cancelButton) {
        cancelButton.removeEventListener("click", onCancel);
      }
      if (acceptButton) {
        acceptButton.removeEventListener("click", onAccept);
      }
      element.removeEventListener("keydown", onKeyDown);
    };
  });
  up.compiler("[data-inline-calendar]", function(element) {
    const hiddenInput = element.parentElement.querySelector("[data-inline-calendar-input]");
    if (!hiddenInput) return;
    function onCalendarChange(event) {
      hiddenInput.value = event.detail.formatted || "";
      const inputEvent = new Event("input", { bubbles: true });
      hiddenInput.dispatchEvent(inputEvent);
      const changeEvent = new Event("change", { bubbles: true });
      hiddenInput.dispatchEvent(changeEvent);
    }
    element.addEventListener("calendar:change", onCalendarChange);
    return function() {
      element.removeEventListener("calendar:change", onCalendarChange);
    };
  });
})();
//# sourceMappingURL=material.js.map
