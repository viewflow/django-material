from django.contrib import admin
from . import models


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):  # noqa D102
    actions = None
    icon = '<i class="material-icons">view_module</i>'
    list_display = ['label', 'installed']
    readonly_fields = ['label']

    def has_add_permission(self, request):
        """Module added automatically during the database migration."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Module deletion is no allowed."""
        return False
