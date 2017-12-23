from datetime import date

from django.test import TestCase
from django.urls import reverse

from . import models


class Test(TestCase):
    def setUp(self):
        self.ocean = models.Ocean.objects.create(
            name="Atlantic",
            area=100,
            slug="atlantic",
            description="Atlantic Ocean",
            map_url="http://viewflow.io/static/logo.png",
        )

        self.sea = models.Sea.objects.create(
            name="Mediterranean Sea",
            ocean=self.ocean,
            area=138600,
            avg_depth=100,
            max_depth=100,
        )

        self.continent = models.Continent.objects.create(
            name="Africa",
            area="30370000",
            population=11000000000,
            population_density='4.2',
            longest_river='Irtysh',
            biggest_mountain='Neverest',
            hemisphere='BOTH'
        )
        self.country = models.Country.objects.create(
            code='RUS',
            name='Russian Federation',
            independence_day=date(1992, 6, 12),
            gay_friendly=False,
            continent=self.continent,
        )

        self.city = models.City.objects.create(
            name='Omsk',
            is_capital=False,
            population='1100000',
            country=self.country
        )

        self.continent.largest_country = self.country
        self.continent.biggest_city = self.city
        self.continent.save()
        self.continent.oceans.add(self.ocean)
        self.sea.basin_countries.add(self.country)

    def test_index_redirect(self):
        response = self.client.get(reverse('atlas:index'))
        self.assertRedirects(response, reverse('atlas:city:index'))

    def test_ocean_list_view(self):
        response = self.client.get(reverse('atlas:ocean:index'))
        self.assertEqual(response.status_code, 200)

    def test_sea_list_view(self):
        response = self.client.get(reverse('atlas:sea:index'))
        self.assertEqual(response.status_code, 200)

    def test_continent_list_view(self):
        response = self.client.get(reverse('atlas:continent:index'))
        self.assertEqual(response.status_code, 200)

    def test_country_list_view(self):
        response = self.client.get(reverse('atlas:country:index'))
        self.assertEqual(response.status_code, 200)

    def test_city_list_view(self):
        response = self.client.get(reverse('atlas:city:index'))
        self.assertEqual(response.status_code, 200)
