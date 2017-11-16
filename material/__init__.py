from django.conf import settings as django_settings

from .layout import Layout, Row, Column, Fieldset, Span
from .ptml import Icon
from .settings import material_settings
from .sites import Site, Application, AppViewset
from .viewset import Viewset, viewprop


__title__ = 'Django-Material'
__version__ = '2.0a1'
__author__ = 'Mikhail Podgurskiy'
__license__ = 'AGPL'
__copyright__ = 'Copyright 2017 Mikhail Podgurskiy'


if material_settings.AUTOREGISTER:
    # Register site middleware
    site_middleware = 'material.middleware.SiteMiddleware'
    if site_middleware not in django_settings.MIDDLEWARE:
        django_settings.MIDDLEWARE += (site_middleware, )
    turbolinks_middleware = 'material.middleware.TurbolinksMiddleware'
    if turbolinks_middleware not in django_settings.MIDDLEWARE:
        django_settings.MIDDLEWARE += (turbolinks_middleware, )

__all__ = (
    'Layout', 'Row', 'Column', 'Fieldset', 'Span', 'Icon',
    'Viewset', 'Site', 'Application', 'AppViewset', 'viewprop',
)
