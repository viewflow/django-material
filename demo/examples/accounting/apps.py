from django.apps import AppConfig
from material.frontend.apps import FrontendAppMixin


class Accounting(FrontendAppMixin, AppConfig):
    name = "demo.examples.accounting"
    icon = '<i class="mdi-action-payment"></i>'
