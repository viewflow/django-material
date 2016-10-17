from . import modules as modules_registry


def modules(request):
    """Add current module and modules list to the template context."""
    if not hasattr(request, 'user'):
        raise ValueError('modules context processor requires "django.contrib.auth.contex_processors.auth"'
                         'to be in TEMPLATE_CONTEXT_PROCESSORS in your settings file.')

    module = None

    if request.resolver_match:
        module = getattr(request.resolver_match.url_name, 'module', None)

    return {
        'modules': modules_registry.available_modules(request.user),
        'current_module': module,
    }
