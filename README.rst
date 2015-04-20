Django Material
===============

Material design for Django Forms and Admin. Template driven.

.. image:: https://travis-ci.org/viewflow/django-material.svg
    :target: https://travis-ci.org/viewflow/django-material

Features
========

* Strong python/html code separation
* Easy redefinition of particular fields rendering
* Complex form layout support

Demo: http://forms.viewflow.io/

.. image:: .screen.png
   :width: 400px


Installation
============

django-material tested with Python 2.7/3.3, django 1.6/1.7::

    pip install django-material

And add it into INSTALLED_APPS settings

.. code-block:: python

    INSTALLED_APPS = (
         'material',
         'material.admin',
         ...
    )

*NOTE:* 'material.admin' must be added before 'django.contrib.admin'


Quick start
===========

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
=============

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
======

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
===============

Material forms library provides  LayoutMixin for model form views, populates
form fields list directly from layout object

.. code-block:: python

    from django import generic
    from viewform import LayoutMixin

    class SampleView(LayoutMixin, generic.ModelFormView):
        layout = Layout(...)


Changelog
=========
0.2.1 - 2015-04-20

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
