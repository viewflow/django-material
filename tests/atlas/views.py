from material.views import ModelViewSet

from . import models

class CityViewset(ModelViewSet):
    model = models.City
    list_display = ('name', 'country', 'population')


class ContinentViewSet(ModelViewSet):
    model = models.Continent


class CountryViewset(ModelViewSet):
    model = models.Country

