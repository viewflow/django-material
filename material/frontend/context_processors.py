from . import modules as modules_registry


def modules(request):
    if not hasattr(request, 'user'):
        raise ValueError('modules context processor requires "django.contrib.auth.contex_processors.auth"'
                         'to be in TEMPLATE_CONTEXT_PROCESSORS in your settings file.')

    module = None

    if request.resolver_match:
        module = request.resolver_match.kwargs.get('module', None)
        if module:
            module = module.user_module(request.user)

    return {
        'modules': modules_registry.available_modules(request.user),
        'current_module': module,
    }
