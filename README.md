⚠️ **IMPORTANT:** This project is under active development. APIs, components, and behavior may change between versions. Use for exploration and prototyping; evaluate carefully before production use.

<div align="center">
  <a href="https://github.com/viewflow/django-material">
    <img src="material/static/material/img/favicon.png" alt="Django Material Logo" width="80" />
  </a>
  <h1 align="center">Django Material</h1>
  <p align="center">Modern Material Design 3 components and full-featured CRUD/admin interfaces for Django</p>
  <p align="center">
    <a href="https://material.viewflow.io"><strong>🌐 Explore Material</strong></a>
  </p>
</div>

## Table of Contents
- [About](#about)
- [Features](#features)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Documentation & Demo](#documentation--demo)
- [Contributing](#contributing)
- [License](#license)

## About
Django Material brings Google's Material Design 3 to Django, offering both low-level UI components and full-featured CRUD/admin interfaces for rapid application development. Built on [TailwindCSS] and [django-cotton], it delivers everything you need — from buttons and cards to list, create, update, and delete views — with minimal setup and zero frontend frameworks.

Our goal is to rethink UI component APIs for AI-assisted development: making them intuitive for developers, predictable for code generation tools, and streamlining the process of crafting interfaces by human or machine.

## Features
- 🎨 Material Design 3 components: buttons, cards, forms, tables, navigation, and more
- 🧩 django-cotton integration: intuitive `<c-button>`, `<c-card>`, and other component tags
- 🛠️ No build step required: pre-built CSS and JS included for immediate use
- 📱 Fully responsive & accessible: mobile-first design with ARIA support and keyboard navigation
- 🔄 SPA-like navigation: powered by [Unpoly.js] for seamless page updates
- 🗃️ Full CRUD & admin: ready-to-use list, create, update, and delete views with Material styling and simple customization
- 🤖 AI-first design: APIs optimized for AI-assisted generation and easy human coding
- 🪄 Easily customizable: override templates, tweak styles, or extend components
- ⚡ Zero frontend frameworks: no React, Vue, or Angular dependencies

## Quickstart
1. Install via pip:
   ```bash
   pip install django-material
   ```
2. Add to `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       # ...
       'material',
       # ...
   ]
   ```
3. Collect static files (production):
   ```bash
   python manage.py collectstatic
   ```
4. In your template:
   ```django
   {% extends "material/base.html" %}
   {% block content %}
     <c-button.filled>Start Building</c-button.filled>
   {% endblock %}
   ```

## Usage
- Modify design tokens in `material/assets/` and rebuild:
  ```bash
  npm run build:css
  npm run build:js
  ```
- Develop with live reloading:
  ```bash
  npm run dev
  ```
- Run tests:
  ```bash
  npm test
  ```
- Lint and format:
  ```bash
  npm run lint
  npm run format
  ```

## Documentation & Demo
Explore comprehensive docs and live demos at [material.viewflow.io](https://material.viewflow.io).

## Contributing
Contributions are welcome! See [ISSUES.md] for bug reports and feature requests.

## License
Licensed under AGPLv3 with Additional Permissions. See [LICENSE] and [LICENSE_EXCEPTION]. Commercial terms in [COMM-LICENSE].

---
Built with ❤️ by the Viewflow Team.

[TailwindCSS]: https://tailwindcss.com/
[django-cotton]: https://github.com/viewflow/django-cotton
[Unpoly.js]: https://unpoly.com/