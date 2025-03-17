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
  - outlined.html - Card with border outline

- **Breadcrumb Components**:
  - container.html - Container for breadcrumb items
  - item.html - Individual breadcrumb link/item

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
  
## Naming Conventions
- Use consistent parameter names across similar components
- Component variants follow Material Design 3 naming: filled, outlined, elevated, etc.
- For component demos, use semantic IDs that match component types
- Demo templates should have concise, descriptive titles