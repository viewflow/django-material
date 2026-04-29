# django-material

Material Design UI components for Django templates, no npm required.

This repository is the starting point for the open-source UI layer. At this stage it contains only a minimal installable Django app and a runnable demo project. Components will be added incrementally.

## Install

```bash
pip install django-material
```

For local development from this repository:

```bash
cd material
uv run python demo/manage.py runserver
```

## Quick Start

Add the app:

```python
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "material",
]
```

Use the base template:

```django
{% extends "material/base.html" %}

{% block title %}Demo{% endblock %}

{% block content %}
  <h1>django-material</h1>
{% endblock %}
```

## Demo

The demo is intentionally flat and small. It only verifies that the package can be loaded by Django and a page can be rendered.

```bash
cd material
uv run python demo/manage.py runserver
```

Open http://127.0.0.1:8000/.

## Scope

Current scope:

- Installable Django app
- Base template
- Runnable demo project

Not included:

- npm or webpack
- React/Vue/Svelte components
- Workflow runtime
- Component implementation
