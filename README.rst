===============
Django Material
===============

Material design for Django Forms and Admin. Template driven.

.. image:: https://img.shields.io/pypi/v/django-material.svg
    :target: https://pypi.python.org/pypi/django-material
.. image:: https://img.shields.io/pypi/wheel/django-material.svg
    :target: https://pypi.python.org/pypi/django-material
.. image:: https://img.shields.io/pypi/status/django-material.svg
    :target: https://pypi.python.org/pypi/django-material
.. image:: https://travis-ci.org/viewflow/django-material.svg
    :target: https://travis-ci.org/viewflow/django-material
.. image:: https://img.shields.io/pypi/pyversions/django-material.svg
    :target: https://pypi.python.org/pypi/django-material
.. image:: https://img.shields.io/pypi/l/Django.svg
    :target: https://raw.githubusercontent.com/viewflow/django-material/master/LICENSE.txt
.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/viewflow/django-material
   :target: https://gitter.im/viewflow/django-material?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Django-Material works with Django 1.8/1.9/1.10

Tested with:

.. image:: demo/static/img/browserstack_small.png
  :target:  http://browserstack.com/

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

Documentation
=============

http://docs.viewflow.io/material_forms.html

License
=======

Django Material is an Open Source project licensed under the terms of the `BSD3 license <https://github.com/viewflow/django-material/blob/master/LICENSE.txt>`_

Django Material Pro has a commercial-friendly license and distributed as part of Viewflow Pro


Changelog
=========

0.11.0 2016-12-13 - Beta
------------------------

* Forms - Default theme secondary color changed to green
* Frontend - Added `startmodule` management command
* Frontend - Added list view actions (PRO)
* Frontend - Integration with django-filters (PRO)
* Frontend - Active page highlight fixed under IE/Safari
* Admin - Fix ManyToMany field height
* Admin - Fix change form markup
