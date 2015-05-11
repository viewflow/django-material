import inspect
from importlib import import_module

from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import module_has_submodule, import_string

from .base import Module
from .registry import modules as modules_registry


class BaseModulesConfig(AppConfig):
    name = 'material.frontend'
    viebose_name = 'Site Modules'


class ModulesDiscoverConfig(BaseModulesConfig):
    """
    Default AppConfig for material.frontend which does autodiscovery
    """
    def ready(self):
        modules = []
        modules_list = getattr(settings, 'MODULES', None)

        if not modules_list:
            # install all existing frontend modules
            for app in settings.INSTALLED_APPS:
                app_package = import_module(app)

                try:
                    package = import_module('{}.modules'.format(app))
                    package_modules = inspect.getmembers(
                        package, lambda o: inspect.isclass(o) and issubclass(o, Module) and o != Module)
                    modules.extend(module.instance for _, module in package_modules)
                except:
                    if module_has_submodule(app_package, 'modules'):
                        raise
        else:
            # explicit fronend modules list
            for module_name in modules_list:
                package_module = import_string(module_name)
                modules.append(package_module.instance)

        for module in modules:
            modules_registry.register(module)

        # initialization
        for module in modules:
            module.ready()

        super(ModulesDiscoverConfig, self).ready()
