from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class Sales(ModuleMixin, AppConfig):
    name = "demo.examples.sales"
    icon = '<i class="mdi-communication-quick-contacts-dialer"></i>'
