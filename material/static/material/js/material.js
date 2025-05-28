(() => {
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
})();
