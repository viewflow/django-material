# Demo Project Development Guidelines

## Project Overview
This demo project showcases Django Material components through interactive examples and documentation. It serves as both a testing ground for components and comprehensive documentation for developers.

## Directory Structure

### Templates Organization
```
demo/templates/demo/
├── index.html                 # Main landing page with component grid
├── html/                      # Component documentation pages
│   ├── base_page.html         # Base template for all component docs
│   ├── buttons.html           # Button component showcase
│   ├── menus.html             # Menu component showcase
│   ├── navigation.html        # Navigation component showcase
│   ├── lists.html             # List component showcase
│   ├── cards.html             # Card component showcase
│   ├── tables.html            # Table component showcase
│   ├── textfields.html        # Text field component showcase
│   ├── textareas.html         # Text area component showcase
│   ├── checkboxes.html        # Checkbox component showcase
│   ├── breadcrumbs.html       # Breadcrumb component showcase
│   ├── colors.html            # Color system documentation
│   └── templates.html         # Base template documentation
└── api/                       # API documentation pages
    ├── forms.html             # Forms API documentation
    ├── views.html             # Views API documentation
    ├── urls.html              # URL configuration documentation
    ├── utils.html             # Utility functions documentation
    ├── middleware.html        # Middleware documentation
    ├── templatetags.html      # Template tags documentation
    └── layout.html            # Layout system documentation
```

### Form Examples
```
demo/forms/
├── showcases/                 # Complete form examples
│   ├── bank_form.py           # Banking form showcase
│   ├── checkout_form.py       # E-commerce checkout form
│   ├── contact_form.py        # Contact form example
│   ├── hospital_form.py       # Medical form example
│   ├── login_form.py          # Authentication forms
│   ├── registration_form.py   # User registration
│   ├── profile_form.py        # User profile editing
│   ├── order_form.py          # Order placement form
│   ├── user_form.py           # User management form
│   ├── wizard_form.py         # Multi-step form wizard
│   └── signup_form.py         # User signup form
└── widgets/                   # Individual widget examples
    ├── checkbox.py            # Checkbox widget demos
    └── textinput.py           # Text input widget demos
```

## Development Guidelines

### Adding New Component Documentation

1. **Create Component Page**: Add new HTML file in `demo/templates/demo/html/`
2. **Follow Naming Convention**: Use lowercase with hyphens (e.g., `text-fields.html`)
3. **Use Base Template**: Extend `demo/html/base_page.html`
4. **Add URL Route**: Register in `demo/urls.py` under the `cotton` Application
5. **Update Navigation**: Add card to `demo/templates/demo/index.html`

### Documentation Page Structure

Each component documentation page should follow this structure:

```html
{% extends 'demo/html/base_page.html' %}
{% load i18n %}

{% block page_breadcrumb %}Component Name{% endblock %}
{% block page_title %}Component Name Components{% endblock %}

{% block page_content %}

  <section id="component-overview" class="mb-12">
    <h2 class="text-2xl mb-4">Component Overview</h2>
    <p class="mb-6">Brief description of the component and its purpose.</p>
    
    <!-- Interactive examples -->
    <div class="border p-6 rounded-lg mb-8 bg-surface-container-low">
      <!-- Component demos here -->
    </div>
  </section>

  <section id="usage" class="mb-12">
    <h2 class="text-2xl mb-4">Usage</h2>
    <div class="bg-surface-container-low p-6 rounded-lg mb-6">
      <pre class="text-on-surface-variant"><code>
        <!-- Code examples here -->
      </code></pre>
    </div>
  </section>

  <section id="attributes" class="mb-12">
    <h2 class="text-2xl mb-4">Attributes</h2>
    <div class="overflow-x-auto mb-6">
      <c-table.container>
        <!-- Attribute documentation table -->
      </c-table.container>
    </div>
  </section>

{% endblock %}
```

### Component Example Standards

1. **Interactive Demos**: Show working examples with visual feedback
2. **Code Examples**: Provide copy-paste ready code snippets
3. **Attribute Tables**: Document all available attributes with types and defaults
4. **Accessibility Notes**: Include keyboard navigation and screen reader info
5. **Variant Coverage**: Show all available component variants and states

### URL Configuration Rules

- Use `menu_path()` helper for all routes
- Include appropriate `icon` for navigation
- Use descriptive `title` for breadcrumbs
- Group related components logically
- Maintain alphabetical order within groups

Example:
```python
menu_path(
    "menus/",
    TemplateView.as_view(template_name="demo/html/menus.html"),
    name="menus",
    icon="more_vert",
    title="Menus",
),
```

### Form Showcase Guidelines

1. **Real-world Examples**: Create forms that solve actual business problems
2. **Complete Implementations**: Include validation, error handling, success states
3. **Responsive Design**: Ensure forms work well on all screen sizes
4. **Accessibility**: Include proper labels, ARIA attributes, keyboard navigation
5. **Material Design**: Follow Material Design 3 form guidelines

### Testing New Components

1. **Visual Testing**: Check appearance across different browsers and screen sizes
2. **Interaction Testing**: Verify all interactive states (hover, focus, active, disabled)
3. **Keyboard Navigation**: Test full keyboard accessibility
4. **Screen Reader**: Verify proper ARIA attributes and semantic HTML
5. **Mobile Testing**: Ensure touch interactions work correctly

### Content Guidelines

1. **Descriptive Text**: Write clear, helpful descriptions for each component
2. **Code Comments**: Include comments in code examples to explain key concepts
3. **Progressive Examples**: Start with basic usage, then show advanced features
4. **Error Cases**: Document common mistakes and how to avoid them
5. **Best Practices**: Include recommendations for optimal usage

### Asset Management

1. **Images**: Store demo images in `material/static/material/img/`
2. **Icons**: Use Material Symbols for consistency
3. **Colors**: Reference Material Design 3 color tokens
4. **Typography**: Use consistent heading hierarchy and text styles

### Performance Considerations

1. **Lazy Loading**: Use Unpoly's lazy loading for heavy content
2. **Code Splitting**: Keep JavaScript modular and component-specific
3. **CSS Optimization**: Use Tailwind's utility classes efficiently
4. **Image Optimization**: Compress and size images appropriately

## Quality Standards

### Code Quality
- Follow existing naming conventions
- Maintain consistent indentation and formatting
- Use semantic HTML elements
- Include proper ARIA attributes for accessibility

### Documentation Quality
- Write clear, concise explanations
- Include practical examples
- Document edge cases and limitations
- Keep examples up-to-date with component changes

### Visual Quality
- Follow Material Design 3 guidelines
- Ensure consistent spacing and alignment
- Use appropriate color contrast ratios
- Test across different screen sizes

## Maintenance Notes

- Update documentation when components change
- Review and update examples regularly
- Test all interactive demos after component updates
- Keep dependency versions synchronized with main project
- Monitor for accessibility regressions