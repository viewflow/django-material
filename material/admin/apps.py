from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MaterialAdminConfig(AppConfig):
    name = 'material.admin'
    label = "material_admin"
    verbose_name = _("Material Admin")
