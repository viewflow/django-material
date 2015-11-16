from django.contrib import admin

from . import models


class ShipmentItemInline(admin.TabularInline):
    model = models.ShipmentItem


@admin.register(models.Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name', 'city')
    inlines = [ShipmentItemInline]
