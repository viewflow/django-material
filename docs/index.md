# Django Material

A modern Material Design framework for Django.

## Overview

Django Material is a Django library that implements Google's Material Design for web applications. It provides a collection of reusable UI components, templates, and tools to help you build beautiful, accessible, and responsive Django applications.

## Installation

```bash
pip install django-material
```

Add `material` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'material',
    # ...
]
```

## Basic Usage

To use the Material components in your Django templates, extend from the base Material template:

```html
{% extends 'material/base.html' %}

{% block body %}
  <!-- Your page content here -->
{% endblock %}
```

## Key Features

- Modern Material Design components
- Responsive layouts
- Accessibility built-in
- Customizable theming
- Integration with Django forms
- Support for RTL languages

## Components

Django Material includes a variety of UI components:

- Buttons
- Cards
- Forms
- Navigation
- Dialogs
- And more...

See the [Components](./components.md) documentation for a complete list and usage examples.

## Customization

Django Material can be customized to match your brand or application theme. See the [Customization](./customization.md) guide for more information.

## Accessibility

All Django Material components are designed with accessibility in mind, following the WAI-ARIA guidelines. See the [Accessibility](./accessibility.md) guide for more information.

## Browser Support

Django Material supports all modern browsers, including:

- Chrome
- Firefox
- Safari
- Edge