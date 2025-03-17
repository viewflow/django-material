# Django Material 3

<div align="center">
  <a href="https://github.com/viewflow/django-material">
    <img src="material/static/material/img/favicon.png" alt="Django Material Logo" width="80" height="80">
  </a>

  <h3 align="center">Django Material Design 3</h3>

  <p align="center">
    Modern Material Design components for Django
    <br />
    <a href="https://material.viewflow.io"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://demo.viewflow.io/material/">View Demo</a>
    ·
    <a href="https://github.com/viewflow/django-material/issues">Report Bug</a>
    ·
    <a href="https://github.com/viewflow/django-material/issues">Request Feature</a>
  </p>
</div>

## About The Project

Django Material is a modern, clean implementation of Google's Material Design 3 for Django applications. Built with TailwindCSS and django-cotton, it provides enterprise-ready UI components that are both beautiful and functional.

### Philosophy

- **Ship as an app, not a template** - Keep your project clean and focused
- **Modern stack** - TailwindCSS, django-cotton, and Material Design 3
- **AI-friendly architecture** - Optimized for modern AI-assisted development
- **Easy to modify** - Extend and override any component
- **Class-less by default** - Clean HTML with sensible defaults

## Features

- 🎨 **Material Design 3 components** - Buttons, cards, breadcrumbs, and more
- 🧩 **django-cotton integration** - Component-based templating
- 🛠️ **No build step required** - Use immediately in your Django project
- 📱 **Fully responsive** - Works on all device sizes
- ♿ **Accessibility built-in** - ARIA support and keyboard navigation
- 🔄 **SPA-like experience** - With Unpoly.js (better than HTMX)
- 🏢 **Enterprise-ready** - Navigation, deep nesting, and complex layouts
- 📑 **Advanced form layouts** - Tables, pagination, and filtering
- 🎯 **Zero dependencies** - No JavaScript frameworks required

## Getting Started

```bash
pip install django-material
```

Add to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'material',
    # ... your apps
]
```

Use in your templates:

```html
{% extends 'material/base.html' %}

{% block content %}
  <c-button.filled>Material Button</c-button.filled>
{% endblock %}
```

## Documentation

Comprehensive documentation is available at [material.viewflow.io](https://material.viewflow.io)

## License

Django Material is an Open Source project licensed under the terms of the AGPL license - [The GNU Affero General Public License v3.0](http://www.gnu.org/licenses/agpl-3.0.html) with the Additional Permissions described in [LICENSE_EXCEPTION](./LICENSE_EXCEPTION)

The AGPL license with Additional Permissions is a free software license that allows commercial use and distribution of the software. It is similar to the GNU GCC Runtime Library license, and it includes additional permissions that make it more friendly for commercial development.

You can read more about AGPL and its compatibility with commercial use at the [AGPL FAQ](http://www.affero.org/oagf.html)

If you use Linux already, this package license likely won't bring anything new to your stack.

Django Material PRO has a commercial-friendly license allowing private forks and modifications of Django Material. You can find the commercial license terms in [COMM-LICENSE](./COMM-LICENSE).

## Acknowledgments

* Developed with [Google Material Design 3](https://m3.material.io/)
* Built on [django-cotton](https://github.com/viewflow/django-cotton)
* Vibe-coded with [Claude](https://anthropic.com/claude) by an experienced Django developer