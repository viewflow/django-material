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

- Forms_ - New way to render django forms

  * Strong python/html code separation
  * Easy redefinition of particular fields rendering
  * Complex form layout support

- Frontend_ - Quick starter template for modular applications development

- Admin_ - Material-designed django admin

Demo: http://forms.viewflow.io/

.. image:: .screen.png
   :width: 400px

Installation
============

django-material tested with Python 2.7/3.4/3.5, django 1.8, django 1.9::

    pip install django-material


Forms
=====

Add `material` into INSTALLED_APPS settings

.. code-block:: python

    INSTALLED_APPS = (
         'material',
         ...
    )

Include material javascript and styles along with jQuery into your base template.

.. code-block:: html

    {% include 'material/includes/material_css.html' %}
    <script src="{% static 'material/js/jquery-2.2.0.js' %}"></script>
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

You can append value to of some tags attribute or completly override the attribute content.

.. code-block:: html

   {% form %}
       {% attr form.email 'group' class append %}yellow{% endattr %}
       {% attr form.email 'label' class append %}big{% endattr %}
       {% attr form.email 'widget' data-validate %}email{% endattr %} <!-- by default value would be overriden -->
       {% attr form.email 'widget' placeholder override %}{% endattr %}
   {% endform %}

There is a lot of other parts and attribute groups declared in default
templates. See template code for details.  If your widget is so
special, you can completly override its rendering

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
        url(r'', include(frontend_urls)),
    ]

The fronend module perform all required settings modification (add middleware, context_processors and template tags),
automagically till `MATERIAL_FRONTEND_AUTOREGISTER` settings set to False.

To create a new module add `ModuleMixin` to your `AppConfig` definision in `apps.py`

.. code-block:: python

    from material.frontend.apps import ModuleMixin

    class Sales(ModuleMixin, AppConfig):
        name = 'sales'
        icon = '<i class="mdi-communication-quick-contacts-dialer"></i>'

The application have to have <app_module>/urls.py file, with
a single no-parametrized url with name='index', ex

.. code-block:: python

    urlpatterns = [
            url('^$', generic.TemplateView.as_view(template_name="sales/index.html"), name="index"),
    ]

All AppConfigs urls will be included into material.frontend.urls automatically under /<app_label>/ prefix
The AppConfig.label, used for the urls namespace.

The menu.html sample

.. code-block:: html

        <ul>
            <li><a href="{% url 'sales:index' %}">Dashboard</a></li>
            <li><a href="{% url 'sales:customers' %}">Customers</a></li>
            {% if perms.sales.can_add_lead %}<li><a href="{% url 'sales:leads' %}">Leads</a></li>{% endif %}
        </ul>

After you create a new module, you need to run `./manage.py migrate`.

You can manage module installed state on the django admin page - `/admin/frontend/module/`

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

****

Changelog
=========

0.8.0 2016-06-14 - Beta
-----------------------

First beta release.

* Forms - Fix 0 as initial value for number input
* Forms - Remove Roboto font fix hack on windows
* Frontend - module heareds fixed
* Admin - list sorting support
* Admin - fixedHeader fixed
* Admin - fix pagination display bug under dj19
* Admin - lost actions support
* Admin - added datetime today shortcut links
* Admin - added filter for select multiple field
* Admin - readonly fields support for inlines
* Admin - mansory layout for index page
* Admin - added app and model icons support
