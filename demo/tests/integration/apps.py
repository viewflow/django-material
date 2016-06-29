from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class IntegrationAppConfig(ModuleMixin, AppConfig):
    name = 'demo.tests.integration'
    icon = '<i class="material-icons">flag</i>'
