from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class Accounting(ModuleMixin, AppConfig):
    name = "demo.examples.accounting"
    icon = '<i class="material-icons">payment</i>'
