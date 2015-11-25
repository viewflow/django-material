from django.contrib import admin
from material import Layout, Row, Fieldset
from material.admin.base import TabularInline

from . import models


class ShipmentItemInline(admin.TabularInline):
    model = models.ShipmentItem


@admin.register(models.Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name', 'city')

    layout = Layout(
        Row('first_name', 'last_name'),
        Row('email', 'phone'),
        Fieldset('Address',
                 Row('address'),
                 Row('city', 'state', 'zipcode'),
                 Row('country')),
        TabularInline(ShipmentItemInline)
    )

    inlines = [ShipmentItemInline]
