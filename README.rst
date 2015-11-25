===============
Django Material
===============

Material design for Django Forms and Admin. Template driven.

.. image:: https://img.shields.io/pypi/v/django-material.svg
    :target: https://pypi.python.org/pypi/django-material

.. image:: https://travis-ci.org/viewflow/django-material.svg
    :target: https://travis-ci.org/viewflow/django-material
    
.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/viewflow/django-material
   :target: https://gitter.im/viewflow/django-material?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


Overview
========

- Forms_ - new way to render django forms

  * Strong python/html code separation
  * Easy redefinition of particular fields rendering
  * Complex form layout support

- Frontend_ - Quick starter template for modular ERP-like applications developent

- Admin_ - Material-designed django admin

Demo: http://forms.viewflow.io/

.. image:: .screen.png
   :width: 400px

Installation
============

django-material tested with Python 2.7/3.4, django 1.8, django 1.9::

    pip install django-material


Forms
=====

Add `material` into INSTALLED_APPS settings 

.. code-block:: python

    INSTALLED_APPS = (
         'material',
         ...
    )

Include material javascript and styles into your base template.

.. code-block:: html

    {% include 'material/includes/material_css.html' %}
    {% include 'material/includes/material_js.html' %}

Load the `material_form` template tag library

.. code-block:: html

        {% load material_form %}

And render your form with {% form %} template tag

.. code-block:: html

    <form method="POST">
        {% csrf_token %}
        {% form form=form %}{% endform %}
        <button type="submit" name="_submit" class="btn">Submit</button>
    </form>

Template tags
-------------

`django-material` forms processing is built around simple concept
called *part*. `part` is like django template block, it has a default
value and could be overriden.  But `parts` are created dynamically for
each form field, which allows you to redefine specific form field html
render output.

Here is the example of rendering form with but prefix email field with email icon.

.. code-block:: html

    <form method="POST">
        {% csrf_token %}
        {% form %}
            {% part form.email prefix %}<div class="input-group-addon">@</div>{% endpart %}
        {% endform %}
        <button type="submit" name="_submit" class="btn">Submit</button>
    </form>

There is a lot of other parts declared in default templates. See
template code for details.  If your widget is so special, you can
completly override its rendering 

.. code-block:: html

    {% part form.my_field %}any html code here{% endpart %}


Layout
------

Layout object is the way to specify relative fields placements and sizes.

.. code-block:: python

    from material import *

    layout = Layout(
        Row('shipment_no', 'description')
        Fieldset("Add to inventory",
                 Row(Span3('product_name'), 'tags'),
                 Row('vendor', 'product_type'),
                 Row(Column('sku',
                            'stock_level',
                            span_columns=4),
                     'gender', 'desired_gender'),
                 Row('cost_price', Span2('wholesale_price'), 'retail_price')))

SpanXX elements are not to material grid classes, but used to
determine relative fields width. Each row occupies 12 grid columns.
Elements in Row('elem1', 'elem2') would be rendered in 6 grid coulmns
each, and in Row(Span2('elem1'), 'elem2') `elem1` would be rendered in
8 grid columns, and `elem2` in 4 grid columns.

Layouts rendering itself is specified in template.


ModelForm Views
---------------

Material forms library provides  LayoutMixin for model form views, populates
form fields list directly from layout object

.. code-block:: python

    from django import generic
    from viewform import LayoutMixin

    class SampleView(LayoutMixin, generic.ModelFormView):
        layout = Layout(...)

****

Frontend
========

Frontend template assumes that your application contains a set of top level `modules`
each one could restrict user access level and have own submenu.

To quick start add `material.frontend` into INSTALLED_APPS settings 

.. code-block:: python

    INSTALLED_APPS = (
         'material',
         'material.frontend',
         ...
    )

Add frontend urls into global urlconf module at urls.py

.. code-block:: python

    from material.frontend import urls as frontend_urls

    urlpatterns = [
        ...
        url(r'^admin/', include(admin.site.urls)),
        url(r'', include(frontend_urls)),
    ]

The fronend module perform all required settings modification (add middleware, context_processors and template tags),
automagically till `MATERIAL_FRONTEND_AUTOREGISTER` settings set to False.

To create a new module make a `modules.py` file, inside app directory, with following content

.. code-block:: python

    from material.frontend import Module

    class Sample(Module):
        icon = 'mdi-image-compare'

By default module expose a single view that renders html template from <module_name>/index.html file.

You can override `Module.get_urls()` method to provide module url config that would be automatically included into
global urls.

To provide custom module menu, just create a template `<module_name>/menu.html`.

You can disable modules autodiscovery and explicitly list enabled modules in the `MODULES` setting

.. code-block:: python

    MODULES = (
        'my_app.modules.Sample'
    )

****

Admin
======

Add `material.admin` into INSTALLED_APPS settings 

.. code-block:: python

    INSTALLED_APPS = (
         'material',
         'material.admin',
         ...
    )

*NOTE:* 'material.admin' must be added before 'django.contrib.admin'

Ensure that `django.template.context_processors.request` in your template context processor settings list

.. code-block:: python

    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'django.template.context_processors.request',
                    ...
                ],
            },
        },
    ]

You can provide a custom admin site module in the `MATERIAL_ADMIN_SITE` setting

.. code-block:: python

    MATERIAL_ADMIN_SITE = 'mymodule.admin.admin_site'

Admin support development is on initial stage. Only basic admin features are available.

****

Changelog
=========

0.5.0 2015-11-19 - Alpha
------------------------

* Django 1.9 support
* Forms - Add latest materializecss
* Admin - Support for Readonly widget
* Admin - Custom admin site support
* Admin - Proper lang_code for html
* Admin - Tabular inlines formset support
* Admin - Fk and Many2Many fields support
* Frontend - Integrate django-easy-pjax into the app
* Frontend - Cancel animation as soon as page loaded


0.4.0 2015-05-29 - Alpha
------------------------

* Forms - CheckboxSelectMultiple widgets with multi-column layout support
* Forms - TimeiInput widget support (thnks @Morozzzko)
* Forms - Dynamic formsets support 
* Admin - fix user change password form
* Frontend - support for smooth navigation back to initial page


0.3.0 2015-05-11 - Alpha
------------------------

* Migrated to new version of materializecss framework
* List all applications in admin navigation menu
* Added breadcrumbs in admin
* Custom material css and js cleanup
* New Frontend template
* Various widget rendering fixes (splitdatetime, empty selects)

0.2.1 2015-04-20 - Alpha
------------------------

* Fixed SplitDateTime widget rendering with empty value
* More consistent parts/variables names over widgets templates
* Fixed file field submition and validation
* Compact html output
* Added ellipses on long labels overflow


0.2.0 2015-04-03 - Alpha
------------------------
* Switched to material design
* Initial admin interface support


0.1.0 2014-11-05 - Alpha
------------------------

* First alpha version extracted from `Viewflow <http://viewflow.io>`_ library
* Basic django widgets support
