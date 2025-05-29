# Django Cotton Material Design Components

## Component Development Guidelines

### File Structure & Naming
- Component files in `material/templates/cotton/{component_type}/`
- Component filenames use snake_case: `button.html`, `card_list.html`
- Component variants in subfolders or with descriptive names: `button/filled.html`
- Components are used with kebab-case prefixed by 'c-': `<c-my-component>`
- Component variants use dot notation: `<c-button.filled>`

### Cotton Component System Patterns

#### Basic Component Structure
```html
<c-vars
  class="default-classes"
  type="default-value"
  color="primary" />

<element class="{{ class }}" {{ attrs }}>
  {{ slot }}
</element>
```

#### Named Slots Usage
```html
<c-component>
  <c-slot name="leading">Leading content</c-slot>
  Main content
  <c-slot name="trailing">Trailing content</c-slot>
</c-component>
```

#### Dynamic Values
```html
<!-- Template variables with colon prefix -->
<c-component :disabled="is_disabled">Content</c-component>

<!-- Python data types with colon prefix -->
<c-component :options="[{'label': 'Name', 'value': 'val'}]"></c-component>
```

### Material Design 3 Component Standards

#### Color System
- Use semantic color roles: `primary`, `secondary`, `tertiary`
- Surface colors: `surface`, `surface-container-low/high`, `surface-variant`
- Text colors: `on-surface`, `on-surface-variant`, `on-primary`
- Error states: `error`, `on-error`

#### Interactive States
- Default, hover, focus, active, disabled states for all interactive elements
- Use Tailwind peer selectors for form field states
- Implement proper ARIA attributes for accessibility
- Use consistent animation durations (200-300ms)

#### Typography & Spacing
- Use consistent spacing scale (p-2, p-4, p-6, etc.)
- Consistent border radius (rounded, rounded-md, rounded-lg)
- Material Design typography scale

### JavaScript Component Development

#### Unpoly Compiler Pattern
```javascript
// Component behavior with Unpoly
up.compiler('[component-selector]', function (element) {
  // Store references for cleanup
  let eventHandler = null;
  
  // Component logic here
  function handleEvent() {
    // Event handling
  }
  
  // Add event listeners
  eventHandler = handleEvent;
  element.addEventListener('event', eventHandler);
  
  // Cleanup function (optional)
  return function() {
    if (eventHandler) {
      element.removeEventListener('event', eventHandler);
    }
  };
});
```

#### State Management
- Use data attributes for component state: `data-open`, `data-selected`
- Update ARIA attributes for accessibility: `aria-expanded`, `aria-selected`
- Use CSS peer selectors to respond to state changes
- Store component functions on element for external access

#### Event Handling Best Practices
- Always prevent default for custom behavior
- Use event delegation when possible
- Clean up event listeners to prevent memory leaks
- Handle keyboard navigation (Enter, Space, Arrow keys, Escape)

#### Positioning & Layout
- Use `getBoundingClientRect()` for precise positioning
- Implement smart positioning with viewport edge detection
- Use `requestAnimationFrame` for smooth animations
- Handle window resize events for repositioning

### Form Components

#### Input Field Pattern
```html
<c-vars
  class="relative w-full group"
  type="text"
  color="primary" />

<div class="{{ class }}" {{ attrs }}>
  <div class="relative">
    <input 
      type="{{ type }}"
      id="{{ id }}"
      name="{{ name }}"
      class="peer w-full p-4 bg-transparent rounded-md appearance-none focus:outline-none"
      {{ attrs }} />
    
    <label 
      for="{{ id }}" 
      class="pointer-events-none absolute z-10 px-1 text-base text-on-surface-variant 
      peer-focus:text-{{ color }} peer-not-placeholder-shown:text-{{ color }}">
      {{ slot }}
    </label>
  </div>
</div>
```

#### Floating Label Implementation
- Use `placeholder=" "` for CSS-only floating labels
- Implement peer selectors for focus/filled states
- Use data attributes for complex state management
- Ensure label transitions are smooth (duration-300)

### Accessibility Requirements

#### ARIA Attributes
- Always include appropriate `role` attributes
- Use `aria-labelledby`, `aria-describedby` for relationships
- Implement `aria-expanded` for collapsible elements
- Use `aria-selected` for selectable items

#### Keyboard Navigation
- Tab order should be logical and complete
- Enter/Space for activation
- Arrow keys for navigation within components
- Escape to close/cancel actions
- Focus management (return focus after modal close)

#### Screen Reader Support
- Use semantic HTML elements when possible
- Provide text alternatives for icon-only buttons
- Announce state changes appropriately
- Use `aria-live` regions for dynamic content

### CSS Class Organization

#### Tailwind CSS Best Practices
- Group related utilities together
- Use consistent spacing and sizing scales
- Leverage CSS custom properties for theming
- Use peer selectors for form field states

#### Responsive Design
- Mobile-first approach with responsive utilities
- Use consistent breakpoints (sm, md, lg, xl)
- Ensure touch targets are adequate (min 44px)
- Test on various screen sizes

#### CSS Custom Properties
```css
/* Use for dynamic theming */
--color-primary: theme(colors.primary);
--color-on-primary: theme(colors.on-primary);
```

### Required Files for New Components

#### Component Template
- Main component file: `component.html`
- Variants in subfolders: `component/variant.html`
- Use `<c-vars>` for default values

#### JavaScript (if interactive)
- Script file: `component/script.js`
- Add import to `cotton/index.js`
- Use Unpoly compiler pattern

#### CSS Class Generation
- Add new classes to `_dumb.html` for Tailwind
- Run `npm run build:css` after adding classes
- Use semantic class names

#### Demo Page
- Create demo in `demo/templates/demo/html/`
- Add URL route to `demo/urls.py`
- Add navigation card to main demo index
- Include usage examples and attribute documentation

### Common Patterns & Solutions

#### Menu/Dropdown Components
- Use absolute positioning within relative container
- Implement smart positioning with viewport detection
- Handle click outside to close
- Support keyboard navigation
- Match menu width to trigger element

#### Form Field States
- Use peer selectors for CSS-only state management
- Implement error, disabled, required states
- Support help text and validation messages
- Ensure consistent spacing and alignment

#### Interactive Elements
- Implement all Material Design interaction states
- Use consistent animation timing
- Support both mouse and keyboard interaction
- Provide visual feedback for all actions

### Performance Considerations

#### JavaScript
- Use event delegation to minimize event listeners
- Clean up resources in component destructors
- Avoid unnecessary DOM queries
- Use `requestAnimationFrame` for animations

#### CSS
- Leverage Tailwind's utility classes
- Minimize custom CSS
- Use efficient selectors
- Optimize for paint and layout performance

### Testing & Quality Assurance

#### Component Testing
- Test all interactive states
- Verify keyboard navigation
- Check accessibility with screen readers
- Test on multiple browsers and devices
- Validate HTML markup

#### Cross-browser Compatibility
- Test on Chrome, Firefox, Safari, Edge
- Verify mobile browser behavior
- Check for vendor prefix requirements
- Test keyboard navigation across browsers

### Documentation Standards

#### Component Documentation
- Include usage examples in demo pages
- Document all attributes and their types
- Provide accessibility guidelines
- Include keyboard navigation reference
- Show all component variants and states

#### Code Comments
- Document complex logic and calculations
- Explain Material Design pattern implementations
- Note accessibility considerations
- Document browser-specific workarounds

### Integration Guidelines

#### Django Integration
- Follow Django form field patterns
- Support Django's CSRF and form validation
- Integrate with Django's admin interface
- Support internationalization (i18n)

#### Unpoly Integration
- Use up-target and up-transition appropriately
- Support Unpoly's navigation patterns
- Handle up-modal and up-drawer contexts
- Test with Unpoly's caching behavior

Remember: Components should be reusable, accessible, performant, and follow Material Design 3 principles consistently.