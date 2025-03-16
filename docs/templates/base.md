# Base Template

`material/base.html` is the core template that provides the foundation for all pages in Django Material. This page documents its structure and customization options.

## Template Structure

The base template creates a minimal HTML structure with proper meta tags, CSS includes, and block definitions for customization:

```html
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE|default:"en-us" }}">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% block favicon %}...{% endblock %}
    <title>{% block title %}{{ site.title|default:"Django Material" }}{% endblock %}</title>
    {% block css %}...{% endblock %}
    {% block js %}...{% endblock %}
    {% block extrahead %}{% endblock %}
  </head>
  <body>
    {% block body %}{% endblock %}
  </body>
</html>
```

## Available Blocks

### Core Structure Blocks

| Block Name | Purpose | Default Content |
|------------|---------|----------------|
| `title` | Sets the page title | `{{ site.title\|default:"Django Material" }}` |
| `favicon` | Customizes the favicon | Material Design favicon |
| `body` | Main body content wrapper | Empty |
| `extrahead` | Additional head elements | Empty |

### CSS Blocks

| Block Name | Purpose | Default Content |
|------------|---------|----------------|
| `css` | All CSS includes | Base CSS links including fonts and layouts |
| `layout_css` | Layout-specific CSS | Standard layout CSS (`layout.css`) |

#### Layout CSS

The base template uses a separate block for layout CSS, allowing you to choose different layouts:

```html
{% block layout_css %}
<link rel="stylesheet" href="{% static 'material/css/layout.css' %}">
{% endblock %}
```

Available layouts:
- Standard layout: `layout.css` (default)
- T-shape layout: `layout_tshape.css`

### JavaScript Blocks

| Block Name | Purpose | Default Content |
|------------|---------|----------------|
| `js` | JavaScript resources | Base JS includes and django-js-catalog |

## Usage Examples

### Basic Page Template

```html
{% extends 'material/base.html' %}

{% block title %}My Page Title{% endblock %}

{% block body %}
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold">My Page Content</h1>
    <p>This is a sample page using Django Material.</p>
</div>
{% endblock %}
```

### Using T-Shape Layout

```html
{% extends 'material/base.html' %}

{% block layout_css %}
<link rel="stylesheet" href="{% static 'material/css/layout_tshape.css' %}">
{% endblock %}
```

### Adding Custom CSS

```html
{% extends 'material/base.html' %}

{% block css %}
{{ block.super }}
<link rel="stylesheet" href="{% static 'myapp/css/custom.css' %}">
{% endblock %}
```

## Best Practices

1. Always extend the base template instead of copying it
2. Use `{{ block.super }}` when adding to a block instead of replacing it completely
3. Place your main content in the `body` block
4. Add custom CSS/JS by extending the respective blocks with `{{ block.super }}`
5. Use the `extrahead` block for page-specific meta tags or resources