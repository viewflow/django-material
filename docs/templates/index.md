# Templates

Django Material provides a set of customizable templates that implement Material Design guidelines. This documentation explains each template's purpose, available blocks, and customization options.

## Overview

The template system is structured as:

- **Base Templates**: Core structural templates that provide the foundation
- **Layout Templates**: Different layout options (standard, T-shape, etc.)
- **Component Templates**: Reusable UI components using django-cotton
- **Include Templates**: Partial templates for common sections

## Template Usage

To use Django Material templates, extend them in your application templates:

```html
{% extends 'material/base.html' %}

{% block content %}
  <!-- Your content here -->
{% endblock %}
```

## Available Template Documentation

- [Base Template](base.md) - Core template structure and blocks
- Layout Templates (coming soon)
- Component Templates (coming soon)
- Include Templates (coming soon)

## Template Customization

Django Material is designed to be customized by:

1. **Extending base templates** - Override blocks for specific sections
2. **Using different layouts** - Choose layout styles appropriate for your app
3. **Customizing components** - Adapt Material components to your needs

See individual template documentation for specific customization options.