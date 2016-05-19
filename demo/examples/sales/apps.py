from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class Sales(ModuleMixin, AppConfig):
    name = "demo.examples.sales"
    icon = '<i class="material-icons">call_end</i>'
