from datetime import date

from django.test import TestCase
from django.urls import reverse

from . import models


class Test(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))

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
        with self.assertNumQueries(4):  # count & select list + session & user
            response = self.client.get(reverse('atlas:sea:index'))
        self.assertEqual(response.status_code, 200)

    def test_sea_add_view(self):
        test_data = {
            'name': "Baltic Sea",
            'ocean': self.ocean.pk,
            'area': 138600,
            'avg_depth': 100,
            'max_depth': 100,
        }
        response = self.client.post(reverse('atlas:sea:add'), test_data)
        self.assertEqual(response.status_code, 302)
        models.Sea.objects.get(**test_data)

    def test_sea_change_view(self):
        test_data = {
            'name': "Baltic Sea",
            'ocean': self.ocean.pk,
            'area': 138600,
            'avg_depth': 100,
            'max_depth': 100,
        }
        response = self.client.post(reverse('atlas:sea:change', args=[self.sea.pk]), test_data)
        self.assertEqual(response.status_code, 302)
        models.Sea.objects.get(
            pk=self.sea.pk,
            **test_data
        )

    def test_sea_delete_view(self):
        response = self.client.post(reverse('atlas:sea:delete', args=[self.sea.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(models.Sea.objects.filter(pk=self.sea.pk))

    def test_continent_list_view(self):
        response = self.client.get(reverse('atlas:continent:index'))
        self.assertEqual(response.status_code, 200)

    def test_continent_add_view(self):
        test_data = {
            'name': "Antarctica",
            'area': 30370000,
            'population': 11000000000,
            'population_density': '4.2',
            'hemisphere': 'BOTH',
            'oceans': [self.ocean.pk]
        }
        response = self.client.post(reverse('atlas:continent:add'), test_data)
        self.assertEqual(response.status_code, 302)
        continent = models.Continent.objects.get(
            name="Antarctica",
            area=30370000,
            population=11000000000,
            population_density='4.2',
            hemisphere='BOTH',
        )
        self.assertEqual(
            list(continent.oceans.values_list('pk', flat=True)),
            [self.ocean.pk])

    def test_continent_change_view(self):
        test_data = {
            'name': "Antarctica",
            'area': 30370000,
            'population': 11000000000,
            'population_density': '4.2',
            'longest_river': 'Irtysh',
            'biggest_mountain': 'Neverest',
            'hemisphere': 'BOTH',
            'oceans': [self.ocean.pk]
        }
        response = self.client.post(reverse('atlas:continent:change', args=[self.continent.pk]), test_data)
        self.assertEqual(response.status_code, 302)
        models.Continent.objects.get(
            name="Antarctica",
            area=30370000,
            population=11000000000,
            population_density='4.2',
            longest_river='Irtysh',
            biggest_mountain='Neverest',
            hemisphere='BOTH',
        )

    def test_country_list_view(self):
        response = self.client.get(reverse('atlas:country:index'))
        self.assertEqual(response.status_code, 200)

    def test_country_add_view(self):
        test_data = {
            'code': 'UK',
            'name': 'United Kingdom',
            'independence_day': '5/1/1707',
            'gay_friendly': True,
            'continent': self.continent.pk,
        }
        response = self.client.post(reverse('atlas:country:add'), test_data)
        self.assertEqual(response.status_code, 302)
        models.Country.objects.get(
            code='UK', name='United Kingdom',
            independence_day=date(1707, 5, 1),
            gay_friendly=True,
            continent=self.continent
        )

    def test_country_change_view(self):
        test_data = {
            'code': 'UK',
            'name': 'United Kingdom',
            'independence_day': '5/1/1707',
            'gay_friendly': True,
            'continent': self.continent.pk,
        }
        response = self.client.post(reverse('atlas:country:change', args=[self.country.pk]), test_data)
        self.assertEqual(response.status_code, 302)
        models.Country.objects.get(
            pk=self.country.pk,
            code='UK',
            name='United Kingdom',
            independence_day=date(1707, 5, 1),
            gay_friendly=True,
            continent=self.continent
        )

    def test_country_delete_view(self):
        response = self.client.post(reverse('atlas:country:delete', args=[self.country.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(models.Country.objects.filter(pk=self.country.pk))

    def test_city_list_view(self):
        response = self.client.get(reverse('atlas:city:index'))
        self.assertEqual(response.status_code, 200)

    def test_city_detail_view(self):
        response = self.client.get(reverse('atlas:city:detail', args=[self.city.pk]))
        self.assertEqual(response.status_code, 200)

    def test_city_add_view(self):
        test_data = {
            'name': 'Vancouver',
            'is_capital': False,
            'population': 8000000,
            'country': self.country.pk
        }
        response = self.client.post(reverse('atlas:city:add'), test_data)
        self.assertEqual(response.status_code, 302)
        models.City.objects.get(**test_data)

    def test_city_change_view(self):
        test_data = {
            'name': 'Vancouver',
            'is_capital': False,
            'population': 8000000,
            'country': self.country.pk
        }
        response = self.client.post(reverse('atlas:city:change', args=[self.city.pk]), test_data)
        self.assertEqual(response.status_code, 302)
        models.City.objects.get(
            pk=self.city.pk,
            **test_data
        )

    def test_city_delete_view(self):
        response = self.client.post(reverse('atlas:city:delete', args=[self.city.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(models.City.objects.filter(pk=self.city.pk))
