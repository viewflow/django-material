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
- Django templates should follow Material Design guidelines
- Components use django-cotton naming conventions:
  - Component files in templates/cotton/{component_type}/
  - Use <c-button.filled> syntax for specific component variants
  - Named slots with <c-slot name="title">Content</c-slot>
- Always provide ARIA attributes for accessibility

## Testing
- Run Django tests: `python manage.py test`
- Run single test: `python manage.py test path.to.test_module.TestClass.test_method`

## Project Structure
- Place components in material/templates/cotton/{component_type}/
- Document components in docs/components.md
- Demo code goes in demo/ directory