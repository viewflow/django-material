from material import Layout, Row, Fieldset
from material.frontend.views import ModelViewSet
from . import models


class CityViewSet(ModelViewSet):
    model = models.City
    list_display = ('name', 'country', 'population')


class ContinentViewSet(ModelViewSet):
    model = models.Continent
    list_display = (
        'name', 'surrounded_oceans', 'countries_count',
        'area', 'population', )
    layout = Layout(
        'name',
        Fieldset('Details',
                 'area',
                 Row('oceans', 'hemisphere'),
                 Row('population', 'population_density')),
        Fieldset('Fun facts',
                 Row('largest_country', 'biggest_mountain'),
                 Row('biggest_city', 'longest_river'))
    )

    def surrounded_oceans(self, contintent):
        return ', '.join(ocean.name for ocean in contintent.oceans.all())

    def countries_count(self, contintent):
        return contintent.countries.count()


class CountryViewSet(ModelViewSet):
    model = models.Country
    list_display = (
        'tld', 'name', 'continent',
        'became_independent_in_20_century',
        'gay_friendly')
    list_display_links = ('tld', 'name', )

    def tld(self, country):
        return '.' + country.code.lower()
    tld.short_description = 'TLD'

    def became_independent_in_20_century(self, country):
        if country.independence_day:
            return 1900 <= country.independence_day.year <= 2000


class OceanViewSet(ModelViewSet):
    model = models.Ocean
    list_display = ('name', 'area', )


class SeaViewSet(ModelViewSet):
    model = models.Sea
    list_display = ('name', 'parent', 'ocean', 'sea_area', )
    layout = Layout(
        Row('name', 'parent'),
        'ocean',
        Row('area', 'avg_depth', 'max_depth'),
        'basin_countries'
    )

    def sea_area(self, sea):
        return None if sea.area == 0 else sea.area
