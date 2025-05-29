// Select component behavior with independent positioning
up.compiler('[up-select-trigger]', function (trigger) {
  const container = trigger.closest('.group');
  const menu = container.querySelector('[up-select-menu]');
  const arrow = container.querySelector('[up-select-arrow]');
  
  if (!menu) return;
  
  // Store references to event listeners for cleanup
  let documentClickHandler = null;
  let documentKeyHandler = null;
  let windowResizeHandler = null;
  
  // Typeahead functionality
  let typeaheadString = '';
  let typeaheadTimeout = null;
  
  // Find option that starts with the given string
  function findOptionByPrefix(prefix) {
    const options = menu.querySelectorAll('[up-select-option]');
    const normalizedPrefix = prefix.toLowerCase();
    
    for (const option of options) {
      const text = (option.textContent || '').trim().toLowerCase();
      if (text.startsWith(normalizedPrefix)) {
        return option;
      }
    }
    return null;
  }
  
  // Handle typeahead search
  function handleTypeahead(char) {
    // Clear previous timeout
    if (typeaheadTimeout) {
      clearTimeout(typeaheadTimeout);
    }
    
    // Add character to search string
    typeaheadString += char.toLowerCase();
    
    // Find matching option
    const matchingOption = findOptionByPrefix(typeaheadString);
    if (matchingOption) {
      matchingOption.focus();
      matchingOption.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    // Clear search string after delay
    typeaheadTimeout = setTimeout(() => {
      typeaheadString = '';
    }, 1000);
  }
  
  // Position menu relative to trigger
  function positionMenu() {
    const triggerRect = trigger.getBoundingClientRect();
    const menuRect = menu.getBoundingClientRect();
    const viewport = {
      width: window.innerWidth,
      height: window.innerHeight
    };
    
    let top, left;
    const placement = menu.dataset.placement || 'bottom-start';
    let actualPlacement = placement;
    
    // Check if there's enough space below for bottom placement
    const spaceBelow = viewport.height - triggerRect.bottom;
    const spaceAbove = triggerRect.top;
    
    // Auto-flip to top if no space below
    if (placement.startsWith('bottom') && 
        spaceBelow < menuRect.height && spaceAbove > menuRect.height) {
      actualPlacement = placement.replace('bottom', 'top');
    }
    
    // Calculate position based on placement
    switch (actualPlacement) {
      case 'top-start':
        top = -menuRect.height;
        left = 0;
        break;
      case 'bottom-start':
      default:
        top = triggerRect.height;
        left = 0;
        break;
    }
    
    // Ensure menu doesn't go off-screen
    if (left < 0) left = 0;
    if (left + menuRect.width > viewport.width) {
      left = Math.max(0, triggerRect.width - menuRect.width);
    }
    
    menu.style.left = `${left}px`;
    menu.style.top = `${top}px`;
    menu.style.minWidth = `${triggerRect.width}px`;
  }
  
  // Show menu
  function showMenu() {
    menu.classList.remove('hidden');
    
    // Update aria attributes and select state
    trigger.setAttribute('aria-expanded', 'true');
    trigger.setAttribute('data-select-open', 'true');
    if (arrow) {
      arrow.style.transform = 'rotate(180deg)';
    }
    
    // Add global event listeners when menu opens
    documentClickHandler = function(e) {
      if (!menu.contains(e.target) && !trigger.contains(e.target)) {
        hideMenu();
      }
    };
    
    documentKeyHandler = function(e) {
      if (e.key === 'Escape' && !menu.classList.contains('hidden')) {
        hideMenu();
        trigger.focus();
      } else if (!menu.classList.contains('hidden') && e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        // Handle typeahead for single character keys
        e.preventDefault();
        handleTypeahead(e.key);
      }
    };
    
    windowResizeHandler = function() {
      if (!menu.classList.contains('hidden')) {
        positionMenu();
      }
    };
    
    document.addEventListener('click', documentClickHandler);
    document.addEventListener('keydown', documentKeyHandler);
    window.addEventListener('resize', windowResizeHandler);
    
    // Use requestAnimationFrame to ensure DOM has updated before positioning
    requestAnimationFrame(() => {
      positionMenu();
      
      // Focus the currently selected item, or first item if none selected
      const selectedItem = menu.querySelector('[up-select-option][aria-selected="true"]');
      const firstItem = menu.querySelector('[up-select-option]');
      const itemToFocus = selectedItem || firstItem;
      
      if (itemToFocus) {
        itemToFocus.focus();
      }
    });
  }
  
  // Hide menu
  function hideMenu() {
    menu.classList.add('hidden');
    
    // Update aria attributes and select state
    trigger.setAttribute('aria-expanded', 'false');
    trigger.removeAttribute('data-select-open');
    if (arrow) {
      arrow.style.transform = 'rotate(0deg)';
    }
    
    // Remove global event listeners when menu closes
    if (documentClickHandler) {
      document.removeEventListener('click', documentClickHandler);
      documentClickHandler = null;
    }
    
    if (documentKeyHandler) {
      document.removeEventListener('keydown', documentKeyHandler);
      documentKeyHandler = null;
    }
    
    if (windowResizeHandler) {
      window.removeEventListener('resize', windowResizeHandler);
      windowResizeHandler = null;
    }
  }
  
  // Toggle menu
  function toggleMenu() {
    if (menu.classList.contains('hidden')) {
      showMenu();
    } else {
      hideMenu();
    }
  }
  
  // Store functions for external access
  menu.showMenu = showMenu;
  menu.hideMenu = hideMenu;
  menu.toggleMenu = toggleMenu;
  trigger.handleTypeahead = handleTypeahead;
  
  // Click on trigger toggles menu
  trigger.addEventListener('click', function(e) {
    e.preventDefault();
    toggleMenu();
  });
  
  // Handle keyboard navigation for trigger
  trigger.addEventListener('keydown', function(e) {
    switch (e.key) {
      case 'Enter':
      case ' ':
      case 'ArrowDown':
      case 'ArrowUp':
        e.preventDefault();
        if (menu.classList.contains('hidden')) {
          showMenu();
        }
        break;
      case 'Escape':
        if (!menu.classList.contains('hidden')) {
          e.preventDefault();
          hideMenu();
          trigger.focus();
        }
        break;
    }
  });
  
  // Prevent text selection on the readonly input
  trigger.addEventListener('selectstart', function(e) {
    e.preventDefault();
  });
});

// Select option behavior
up.compiler('[up-select-option]', function (option) {
  const menu = option.closest('[up-select-menu]');
  const container = menu?.closest('.group');
  const trigger = container?.querySelector('[up-select-trigger]');
  
  if (!trigger || !menu) return;
  
  // Handle option selection
  option.addEventListener('click', function(e) {
    e.preventDefault();
    
    // Get the value and text from the option
    const value = option.dataset.value || option.textContent.trim();
    const displayText = option.textContent.trim();
    
    // Update the trigger input
    trigger.value = displayText;
    trigger.setAttribute('value', displayText);
    
    // Update hidden input if it exists (for form submission)
    const hiddenInput = container.querySelector('input[type="hidden"]');
    if (hiddenInput) {
      hiddenInput.value = value;
    }
    
    // Update selected state
    const allOptions = menu.querySelectorAll('[up-select-option]');
    allOptions.forEach(opt => {
      opt.classList.remove('bg-on-surface/12');
      opt.setAttribute('aria-selected', 'false');
    });
    
    option.classList.add('bg-on-surface/12');
    option.setAttribute('aria-selected', 'true');
    
    // Trigger change event
    const changeEvent = new Event('change', { bubbles: true });
    trigger.dispatchEvent(changeEvent);
    
    // Close menu
    setTimeout(() => {
      if (menu.hideMenu) {
        menu.hideMenu();
      }
      trigger.focus();
    }, 100);
  });
  
  // Handle keyboard navigation within options
  option.addEventListener('keydown', function(e) {
    const items = Array.from(menu.querySelectorAll('[up-select-option]'));
    const currentIndex = items.indexOf(option);
    
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        const nextIndex = (currentIndex + 1) % items.length;
        items[nextIndex].focus();
        break;
      case 'ArrowUp':
        e.preventDefault();
        const prevIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
        items[prevIndex].focus();
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        option.click();
        break;
      case 'Tab':
        // Allow tab to close menu and move focus
        if (menu.hideMenu) {
          menu.hideMenu();
        }
        break;
      default:
        // Handle typeahead for single character keys
        if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
          e.preventDefault();
          if (menu.closest('.group').querySelector('[up-select-trigger]')) {
            // Get the select component and call its typeahead function
            const selectTrigger = menu.closest('.group').querySelector('[up-select-trigger]');
            if (selectTrigger.handleTypeahead) {
              selectTrigger.handleTypeahead(e.key);
            }
          }
        }
        break;
    }
  });
  
  // Set initial selected state based on trigger value
  const triggerValue = trigger.value;
  const optionValue = option.dataset.value || option.textContent.trim();
  if (triggerValue === optionValue || triggerValue === option.textContent.trim()) {
    option.classList.add('bg-on-surface/12');
    option.setAttribute('aria-selected', 'true');
  } else {
    option.setAttribute('aria-selected', 'false');
  }
});