/* eslint-env browser */
import MaterialDateUtils from './date-utils.js';

// Calendar component with Unpoly compiler
up.compiler('[data-calendar]', function(element) {
  const color = element.dataset.color || 'primary';
  const format = element.dataset.format || '%Y-%m-%d';
  const header = element.dataset.header === 'true';
  const actions = element.dataset.actions === 'true';
  const disabled = element.dataset.disabled === 'true';
  
  let currentYear = new Date().getFullYear();
  let currentMonth = new Date().getMonth();
  let selectedDate = null;
  let isYearPickerOpen = false;
  
  // Initialize from value if provided
  if (element.dataset.value) {
    try {
      selectedDate = MaterialDateUtils.parseDateTime(format, element.dataset.value);
      currentYear = selectedDate.getFullYear();
      currentMonth = selectedDate.getMonth();
    } catch (e) {
      console.warn('Invalid initial date value:', element.dataset.value);
    }
  }
  
  // DOM elements
  const monthYearEl = element.querySelector('[data-month-year]');
  const yearPicker = element.querySelector('[data-year-picker]');
  const weekdaysContainer = element.querySelector('[data-weekdays]');
  const daysContainer = element.querySelector('[data-calendar-days]');
  const prevButton = element.querySelector('[data-prev-month]');
  const nextButton = element.querySelector('[data-next-month]');
  const cancelButton = element.querySelector('[data-calendar-cancel]');
  const acceptButton = element.querySelector('[data-calendar-accept]');
  const selectedWeekdayEl = element.querySelector('[data-selected-weekday]');
  const selectedDateEl = element.querySelector('[data-selected-date]');
  
  // Initialize weekday headers
  const weekdayElements = element.querySelectorAll('[data-weekday]');
  weekdayElements.forEach((el, index) => {
    const dayIndex = (index + MaterialDateUtils.firstDayOfWeek) % 7;
    el.textContent = MaterialDateUtils.daysOfWeek[dayIndex];
  });
  
  function updateHeader() {
    if (!header || !selectedDate) return;
    
    if (selectedWeekdayEl) {
      selectedWeekdayEl.textContent = MaterialDateUtils.daysOfWeekAbbr[selectedDate.getDay()] + ',';
    }
    if (selectedDateEl) {
      selectedDateEl.textContent = MaterialDateUtils.monthsOfYearAbbr[selectedDate.getMonth()] + ' ' + selectedDate.getDate();
    }
  }
  
  function renderCalendar() {
    if (!monthYearEl || !daysContainer) return;
    
    // Update month/year title
    monthYearEl.textContent = `${MaterialDateUtils.monthsOfYear[currentMonth]} ${currentYear}`;
    
    // Clear days
    daysContainer.innerHTML = '';
    
    // Calculate calendar layout
    const firstDay = MaterialDateUtils.getFirstDayOfMonth(currentYear, currentMonth);
    const daysInMonth = MaterialDateUtils.daysInMonth(currentYear, currentMonth);
    const startPos = (firstDay - MaterialDateUtils.firstDayOfWeek + 7) % 7;
    
    // Create 6 rows of 7 days
    for (let week = 0; week < 6; week++) {
      for (let day = 0; day < 7; day++) {
        const cell = week * 7 + day;
        const dayNumber = cell >= startPos && cell < daysInMonth + startPos ? cell - startPos + 1 : '';
        
        const dayEl = document.createElement('div');
        dayEl.className = 'flex justify-center items-center h-9';
        
        if (dayNumber) {
          const span = document.createElement('span');
          
          // Check if this is the selected date
          const isSelected = selectedDate && 
              selectedDate.getFullYear() === currentYear && 
              selectedDate.getMonth() === currentMonth && 
              selectedDate.getDate() === dayNumber;
          
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

  /**
   * Shows the year picker grid
   */
  function showYearPicker() {
    if (!yearPicker || disabled) return;
    
    isYearPickerOpen = true;
    
    // Hide weekdays and calendar days, show year picker
    if (weekdaysContainer) weekdaysContainer.classList.add('hidden');
    daysContainer.classList.add('hidden');
    yearPicker.classList.remove('hidden');
    
    // Clear existing years
    yearPicker.innerHTML = '';
    
    // Create 6 rows × 4 columns = 24 years (current year ± 11)
    const startYear = currentYear - 11;
    const endYear = currentYear + 12;
    
    for (let year = startYear; year <= endYear; year++) {
      const yearButton = document.createElement('button');
      yearButton.type = 'button';
      yearButton.className = 'h-9 px-2 py-1 text-sm rounded transition-colors focus:outline-none focus:ring-2 focus:ring-primary/20';
      yearButton.textContent = year;
      
      if (year === currentYear) {
        yearButton.className += ` bg-${color} text-on-${color}`;
      } else {
        yearButton.className += ' text-on-surface hover:bg-surface-variant';
      }
      
      yearButton.addEventListener('click', () => selectYear(year));
      yearPicker.appendChild(yearButton);
    }
    
    // Focus current year (should be around the middle)
    const currentYearIndex = currentYear - startYear;
    const currentYearButton = yearPicker.querySelector(`button:nth-child(${currentYearIndex + 1})`);
    if (currentYearButton) {
      currentYearButton.focus();
    }
  }

  /**
   * Hides the year picker grid
   */
  function hideYearPicker() {
    if (!yearPicker) return;
    
    isYearPickerOpen = false;
    
    // Show weekdays and calendar days, hide year picker
    if (weekdaysContainer) weekdaysContainer.classList.remove('hidden');
    daysContainer.classList.remove('hidden');
    yearPicker.classList.add('hidden');
  }

  /**
   * Selects a year and updates the calendar
   */
  function selectYear(year) {
    currentYear = year;
    renderCalendar();
    hideYearPicker();
    monthYearEl?.focus();
  }

  /**
   * Toggles the year picker dropdown
   */
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
    
    // Update selected date if it exists to the same day in new month
    if (selectedDate) {
      const newDay = Math.min(selectedDate.getDate(), MaterialDateUtils.daysInMonth(currentYear, currentMonth));
      selectDate(newDay);
    }
  }
  
  function selectDate(day) {
    if (disabled) return;
    
    const newDate = new Date(currentYear, currentMonth, day);
    selectedDate = newDate;
    
    // Format and store the date
    const formattedDate = MaterialDateUtils.formatDate(format, newDate);
    element.dataset.value = formattedDate;
    
    // Trigger change event
    const changeEvent = new CustomEvent('calendar:change', {
      detail: { date: newDate, formatted: formattedDate },
      bubbles: true
    });
    element.dispatchEvent(changeEvent);
    
    renderCalendar();
  }
  
  // Event listeners
  function onDayClick(event) {
    if (disabled || event.target.tagName !== 'SPAN') return;
    
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
    const cancelEvent = new CustomEvent('calendar:cancel', { bubbles: true });
    element.dispatchEvent(cancelEvent);
  }
  
  function onAccept() {
    const acceptEvent = new CustomEvent('calendar:accept', {
      detail: { date: selectedDate, formatted: selectedDate ? MaterialDateUtils.formatDate(format, selectedDate) : null },
      bubbles: true
    });
    element.dispatchEvent(acceptEvent);
  }
  
  // Navigation button keyboard handlers
  function onPrevButtonKeyDown(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      onPrevMonth();
    }
  }
  
  function onNextButtonKeyDown(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      onNextMonth();
    }
  }

  function onMonthYearKeyDown(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      toggleYearPicker();
    } else if (event.key === 'Escape' && isYearPickerOpen) {
      event.preventDefault();
      hideYearPicker();
    }
  }

  // Attach event listeners
  if (daysContainer) {
    daysContainer.addEventListener('click', onDayClick);
  }
  if (monthYearEl) {
    monthYearEl.addEventListener('click', onMonthYearClick);
    monthYearEl.addEventListener('keydown', onMonthYearKeyDown);
  }
  if (prevButton) {
    prevButton.addEventListener('click', onPrevMonth);
    prevButton.addEventListener('keydown', onPrevButtonKeyDown);
  }
  if (nextButton) {
    nextButton.addEventListener('click', onNextMonth);
    nextButton.addEventListener('keydown', onNextButtonKeyDown);
  }
  if (cancelButton) {
    cancelButton.addEventListener('click', onCancel);
  }
  if (acceptButton) {
    acceptButton.addEventListener('click', onAccept);
  }

  
  // Keyboard navigation
  function onKeyDown(event) {
    if (disabled) return;
    
    // Don't handle keyboard events if focus is on action buttons or year picker is open
    if (event.target === cancelButton || event.target === acceptButton || isYearPickerOpen) {
      return;
    }
    
    switch (event.key) {
      case 'ArrowLeft':
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
      case 'ArrowRight':
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
      case 'ArrowUp':
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
      case 'ArrowDown':
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
      case 'Enter':
      case ' ':
        event.preventDefault();
        if (selectedDate && acceptButton) {
          onAccept();
        }
        break;
      case 'Escape':
        event.preventDefault();
        if (isYearPickerOpen) {
          hideYearPicker();
        } else if (cancelButton) {
          onCancel();
        }
        break;
    }
  }
  
  element.addEventListener('keydown', onKeyDown);
  element.setAttribute('tabindex', '0');
  
  // Public API
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
          console.warn('Invalid date value:', value);
          return;
        }
      }
      element.dataset.value = value || '';
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
  
  // Initial render
  renderCalendar();
  
  // Cleanup function
  return function() {
    if (daysContainer) {
      daysContainer.removeEventListener('click', onDayClick);
    }
    if (monthYearEl) {
      monthYearEl.removeEventListener('click', onMonthYearClick);
      monthYearEl.removeEventListener('keydown', onMonthYearKeyDown);
    }
    if (prevButton) {
      prevButton.removeEventListener('click', onPrevMonth);
      prevButton.removeEventListener('keydown', onPrevButtonKeyDown);
    }
    if (nextButton) {
      nextButton.removeEventListener('click', onNextMonth);
      nextButton.removeEventListener('keydown', onNextButtonKeyDown);
    }
    if (cancelButton) {
      cancelButton.removeEventListener('click', onCancel);
    }
    if (acceptButton) {
      acceptButton.removeEventListener('click', onAccept);
    }
    element.removeEventListener('keydown', onKeyDown);
  };
});

// Inline calendar form component
up.compiler('[data-inline-calendar]', function(element) {
  const hiddenInput = element.parentElement.querySelector('[data-inline-calendar-input]');
  
  if (!hiddenInput) return;
  
  // Listen for calendar changes and update hidden input
  function onCalendarChange(event) {
    hiddenInput.value = event.detail.formatted || '';
    
    // Trigger input change event for form validation
    const inputEvent = new Event('input', { bubbles: true });
    hiddenInput.dispatchEvent(inputEvent);
    
    const changeEvent = new Event('change', { bubbles: true });
    hiddenInput.dispatchEvent(changeEvent);
  }
  
  element.addEventListener('calendar:change', onCalendarChange);
  
  // Cleanup
  return function() {
    element.removeEventListener('calendar:change', onCalendarChange);
  };
});