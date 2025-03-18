# Development Guidelines for Django Material

## Project Setup
- Install dependencies: `pip install -e ".[docs]"`
- Run Django dev server: `python manage.py runserver`

## Documentation
- Build docs: `mkdocs build` or `hatch run docs:build`
- Serve docs locally: `mkdocs serve` or `hatch run docs:serve`
- Deploy docs: `hatch run docs:deploy`

## Code Style
- Use TailwindCSS for styling components
- Follow Google style docstrings for Python code
- Follow Material Design 3 guidelines for component styling
- Components use django-cotton naming conventions:
  - Component files in templates/cotton/{component_type}/
  - Use <c-button.filled> syntax for specific component variants
  - Named slots with <c-slot name="title">Content</c-slot>
- Always provide ARIA attributes for accessibility
- Use CSS custom properties for theming with primary/secondary/tertiary color schemes
- Use flexbox for component layouts
- Implement proper hover and focus states for interactive elements
- Standardize on `icon` attribute for all components that display icons
- Components with text content should use slot content directly instead of label attributes
- Required attributes should have sensible defaults whenever possible

## Comment Guidelines
- Module docstrings: 1-2 lines explaining core purpose/function
- Class docstrings: Single line explaining role/responsibility
- Method docstrings: Brief description of function and parameters
- Inline comments: Only for non-obvious code or key functionality
- Use concise language, avoid excessive verbosity
- For form renderers, document template context variables

## Component Structure
- **Button Components**:
  - filled.html - High-emphasis filled background button
  - text.html - Low-emphasis text-only button
  - outlined.html - Medium-emphasis outlined button
  - elevated.html - Button with shadow elevation
  - icon.html - Circular icon-only button
  - fab.html - Floating action button with size variants
  - segment.html - Segmented button for grouped controls

- **Card Components**:
  - elevated.html - Card with shadow elevation
  - filled.html - Card with colored background
  - outlined.html - Card with border outline (supports hover_border)

- **Breadcrumb Components**:
  - container.html - Container for breadcrumb items
  - item.html - Individual breadcrumb link/item

- **Navigation Components**:
  - container.html - Navigation container (supports rail variant)
  - item.html - Navigation item (supports expandable/nested items)
  - group.html - Grouping of navigation items
  - header.html - Navigation header with title and optional subtitle
  - divider.html - Visual separator between navigation sections

## Testing
- Run Django tests: `python manage.py test`
- Run single test: `python manage.py test path.to.test_module.TestClass.test_method`

## Project Structure
- Place components in material/templates/cotton/{component_type}/
- Document components in docs/components.md
- Demo code in demo/ directory:
  - demo/templates/demo/index.html - Main landing page
  - Dedicated pages for each component category (buttons.html, cards.html, etc.)
  - Each demo page should have consistent navigation

## Timeless Component Design Principles
- Use semantic HTML elements for proper accessibility
- Keep component APIs simple and intuitive
- Be consistent with attribute naming across similar components
- Minimize required JavaScript dependencies
- Design for mobile-first, responsive experiences
- Ensure keyboard navigability for all interactive elements
- Provide visual feedback for all interactive states
- Design components to be composable with other components
- Follow progressive enhancement principles
- Ensure components work well with screen readers

## Naming Conventions
- Use consistent parameter names across similar components
- Component variants follow Material Design 3 naming: filled, outlined, elevated, etc.
- For component demos, use semantic IDs that match component types
- Demo templates should have concise, descriptive titles
- Prefer shorter component names (e.g., c-nav instead of c-navigation)
- Use standard attribute names (e.g., icon, title, variant) consistently