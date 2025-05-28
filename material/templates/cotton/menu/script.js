// Menu positioning and behavior with Unpoly
up.compiler('[up-menu]', function (menu) {
  const anchorSelector = menu.dataset.anchor;
  const placement = menu.dataset.placement || 'bottom-start';
  
  if (!anchorSelector) return;
  
  const anchor = document.querySelector(anchorSelector);
  if (!anchor) return;
  
  // Store references to event listeners for cleanup
  let documentClickHandler = null;
  let documentKeyHandler = null;
  let windowResizeHandler = null;
  
  // Position menu relative to anchor
  function positionMenu() {
    const anchorRect = anchor.getBoundingClientRect();
    const menuRect = menu.getBoundingClientRect();
    const viewport = {
      width: window.innerWidth,
      height: window.innerHeight
    };
    
    let top, left;
    
    // Calculate initial position based on placement
    switch (placement) {
      case 'bottom-start':
        top = anchorRect.bottom;
        left = anchorRect.left;
        break;
      case 'bottom-end':
        top = anchorRect.bottom;
        left = anchorRect.right - menuRect.width;
        break;
      case 'top-start':
        top = anchorRect.top - menuRect.height;
        left = anchorRect.left;
        break;
      case 'top-end':
        top = anchorRect.top - menuRect.height;
        left = anchorRect.right - menuRect.width;
        break;
      case 'right-start':
        top = anchorRect.top;
        left = anchorRect.right;
        break;
      case 'left-start':
        top = anchorRect.top;
        left = anchorRect.left - menuRect.width;
        break;
      default:
        top = anchorRect.bottom;
        left = anchorRect.left;
    }
    
    // Adjust for viewport boundaries
    if (left + menuRect.width > viewport.width) {
      left = viewport.width - menuRect.width - 8;
    }
    if (left < 8) {
      left = 8;
    }
    
    if (top + menuRect.height > viewport.height) {
      top = anchorRect.top - menuRect.height;
    }
    if (top < 8) {
      top = 8;
    }
    
    menu.style.left = `${left}px`;
    menu.style.top = `${top}px`;
  }
  
  // Show menu
  function showMenu() {
    menu.classList.remove('hidden');
    
    // Add global event listeners when menu opens
    documentClickHandler = function(e) {
      if (!menu.contains(e.target) && !anchor.contains(e.target)) {
        hideMenu();
      }
    };
    
    documentKeyHandler = function(e) {
      if (e.key === 'Escape' && !menu.classList.contains('hidden')) {
        hideMenu();
        anchor.focus();
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
      
      // Focus first menu item
      const firstItem = menu.querySelector('[up-menu-item]');
      if (firstItem) {
        firstItem.focus();
      }
    });
  }
  
  // Hide menu
  function hideMenu() {
    menu.classList.add('hidden');
    
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
  
  // Click on anchor toggles menu
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    toggleMenu();
  });
});

// Menu item keyboard navigation
up.compiler('[up-menu-item]', function (menuItem) {
  const menu = menuItem.closest('[up-menu]');
  if (!menu) return;
  
  menuItem.addEventListener('keydown', function(e) {
    const items = Array.from(menu.querySelectorAll('[up-menu-item]'));
    const currentIndex = items.indexOf(menuItem);
    
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
        menuItem.click();
        break;
      case 'Tab':
        // Allow tab to close menu and move focus
        menu.hideMenu();
        break;
    }
  });
  
  // Click handler for menu items
  menuItem.addEventListener('click', function() {
    // Close menu after item selection
    setTimeout(() => {
      menu.hideMenu();
    }, 100);
  });
});
