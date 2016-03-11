from django.contrib import admin
from . import models


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['label', 'installed']
    readonly_fields = ['label']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
