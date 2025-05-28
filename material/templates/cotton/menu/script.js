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
  let documentScrollHandler = null;
  
  // Position menu relative to anchor
  function positionMenu() {
    const anchorRect = anchor.getBoundingClientRect();
    const menuRect = menu.getBoundingClientRect();
    const viewport = {
      width: window.innerWidth,
      height: window.innerHeight
    };
    
    let top, left;
    let actualPlacement = placement;
    
    // Check if there's enough space below for bottom placement
    const spaceBelow = viewport.height - anchorRect.bottom;
    const spaceAbove = anchorRect.top;
    
    // Auto-flip to top if no space below (for bottom placements)
    if ((placement.startsWith('bottom') || placement === 'bottom-start') && 
        spaceBelow < menuRect.height && spaceAbove > menuRect.height) {
      actualPlacement = placement.replace('bottom', 'top');
    }
    
    // Check if anchor is on the right side of the page
    const anchorCenter = anchorRect.left + anchorRect.width / 2;
    const onRightSide = anchorCenter > viewport.width / 2;
    
    // Auto-adjust horizontal position if on right side
    if (onRightSide && anchorRect.right > menuRect.width) {
      actualPlacement = actualPlacement.replace('start', 'end');
    }
    
    // Calculate position based on actual placement
    switch (actualPlacement) {
      case 'top-start':
        top = -menuRect.height;
        left = 0;
        break;
      case 'top-end':
        top = -menuRect.height;
        left = anchorRect.width - menuRect.width;
        break;
      case 'bottom-end':
        top = anchorRect.height;
        left = anchorRect.width - menuRect.width;
        break;
      case 'bottom-start':
      default:
        top = anchorRect.height;
        left = 0;
        break;
    }
    
    // Ensure menu doesn't go off-screen
    if (left < 0) left = 0;
    if (left + menuRect.width > viewport.width) {
      left = Math.max(0, anchorRect.width - menuRect.width);
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
