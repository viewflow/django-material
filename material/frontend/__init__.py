from django.conf import settings

from .urlconf import ModuleURLResolver, frontend_url
from .registry import modules


__all__ = (
    'ModuleURLResolver', 'frontend_url', 'modules'
)

default_app_config = 'material.frontend.apps.MaterialFrontendConfig'


if getattr(settings, 'MATERIAL_FRONTEND_AUTOREGISTER', True):
    # Register middleware
    if 'material.frontend.middleware.SmoothNavigationMiddleware' not in settings.MIDDLEWARE:
        settings.MIDDLEWARE += ('material.frontend.middleware.SmoothNavigationMiddleware',)

    # Context processors
    for engine in settings.TEMPLATES:
        if engine['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
            if 'OPTIONS' not in engine:
                engine['OPTIONS'] = {}
            if 'context_processors' not in engine['OPTIONS']:
                engine['OPTIONS']['context_processors'] = []
            if 'material.frontend.context_processors.modules' not in engine['OPTIONS']['context_processors']:
                engine['OPTIONS']['context_processors'].append('material.frontend.context_processors.modules')
