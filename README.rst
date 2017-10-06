===============
Django-Material
===============

Material Design for Django applications

Based on `Google Material Compoments for the web <https://material.io/components/web/>`_

This is django-material version 2 rewrite, replaces MaterializeCSS library with Google MDC.
Work in progress.

Features
========

* Awesome forms
    * Complex adaptive form layouts
* TODO


Demo
====

To checkout and run demo localy, you need to have
`git <https://git-scm.com/>`_ and `tox
<https://tox.readthedocs.io/en/latest/>`_ tools installed.

.. code:: bash

    git clone -b v2 https://github.com/viewflow/django-material.git
    cd django-material

    TOXENV=py36-dj20 tox -- python manage.py migrate --settings=demo.settings
    TOXENV=py36-dj20 tox -- python manage.py runserver --settings=demo.settings


License
=======

Django-Material is an Open Source project licensed under the terms of the
AGPL license - `The GNU Affero General Public License v3.0 <http://www.gnu.org/licenses/agpl-3.0.html>`_
