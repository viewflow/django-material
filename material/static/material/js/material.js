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
})();
//# sourceMappingURL=material.js.map
