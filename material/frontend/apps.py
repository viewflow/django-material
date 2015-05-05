from django.apps import AppConfig


class BaseModulesConfig(AppConfig):
    name = 'material.frontend'
    viebose_name = 'Site Modules'


class ModulesDiscoverConfig(BaseModulesConfig):
    """
    Default AppConfig for material.frontend which does autodiscovery
    """
    def ready(self):
        super(ModulesDiscoverConfig, self).ready()
        self.module.autodiscover()
