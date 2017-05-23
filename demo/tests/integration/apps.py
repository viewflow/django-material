from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _


class IntegrationAppConfig(ModuleMixin, AppConfig):
    name = 'demo.tests.integration'
    icon = '<i class="material-icons">extension</i>'
    verbose_name = _("CRUD sample")

    def has_perm(self, user):
        return user.is_superuser
