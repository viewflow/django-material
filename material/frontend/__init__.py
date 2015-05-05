from .base import Module, InstallableModule  # NOQA
from .urlconf import ModuleURLResolver  # NOQA
from .registry import default_registry


def autodiscover(module_to_search='modules', register_to=None, on_ready=lambda register_to: register_to.ready()):
    """
    Autoload apps modules.py. If you don't need django 1.6
    could be replace by `django.utils.module_loading.autodiscover_modules`
    """
    import copy
    from importlib import import_module
    from django.conf import settings
    from django.utils.module_loading import module_has_submodule

    register_to = register_to or default_registry

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)

        if register_to:
            before_import_registry = copy.copy(register_to._registry)

        try:
            import_module('%s.%s' % (app, module_to_search))
        except:
            if register_to:
                register_to._registry = before_import_registry

            if module_has_submodule(mod, module_to_search):
                raise

    if on_ready:
        on_ready(register_to)


default_app_config = 'material.frontend.apps.ModulesDiscoverConfig'
