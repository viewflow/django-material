from django.db import models


class Shipment(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()

    # shipment address
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment)
    name = models.CharField(max_length=250)
    quantity = models.IntegerField(default=1)
