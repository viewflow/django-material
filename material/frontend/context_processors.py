from . import modules as modules_registry


def modules(request):
    """Add current module and modules list to the template context."""
    module = None

    if request.resolver_match:
        module = getattr(request.resolver_match.url_name, 'module', None)

    return {
        'modules': modules_registry.available_modules(request.user) if hasattr(request, 'user') else [],
        'current_module': module,
    }
