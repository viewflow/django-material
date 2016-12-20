from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class EmployeesConfig(ModuleMixin, AppConfig):
    name = 'demo.examples.employees'
    icon = '<i class="material-icons">people</i>'
