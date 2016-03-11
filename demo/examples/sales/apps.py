from django.apps import AppConfig
from material.frontend.apps import FrontendAppMixin


class Sales(FrontendAppMixin, AppConfig):
    name = "demo.examples.sales"
    icon = '<i class="mdi-communication-quick-contacts-dialer"></i>'
