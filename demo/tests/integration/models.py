from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe


@python_2_unicode_compatible
class Ocean(models.Model):
    name = models.CharField(max_length=250, primary_key=True)
    area = models.BigIntegerField()
    slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Sea(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey('self', blank=True, null=True)
    ocean = models.ForeignKey(Ocean)

    area = models.BigIntegerField(help_text=mark_safe('km&#178;'))
    avg_depth = models.IntegerField(help_text='meters', null=True, blank=True)
    max_depth = models.IntegerField(help_text='meters', null=True, blank=True)

    basin_countries = models.ManyToManyField(
        'Country', related_name='seas', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Continent(models.Model):
    name = models.CharField(max_length=250, primary_key=True)
    area = models.BigIntegerField(help_text=mark_safe('km&#178;'))
    population = models.BigIntegerField()
    population_density = models.DecimalField(decimal_places=2, max_digits=8)

    largest_country = models.OneToOneField(
        'Country', related_name='+', blank=True, null=True)
    biggest_city = models.OneToOneField(
        'City', blank=True, null=True)
    longest_river = models.CharField(max_length=250, blank=True, null=True)
    biggest_mountain = models.CharField(max_length=250, blank=True, null=True)

    oceans = models.ManyToManyField(Ocean)
    hemisphere = models.CharField(
        max_length=5, choices=(
            ('NORTH', 'North'),
            ('SOUTH', 'South'),
            ('BOTH', 'Both')))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


@python_2_unicode_compatible
class Country(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=250)
    independence_day = models.DateField(null=True, blank=True)
    gay_friendly = models.NullBooleanField()
    continent = models.ForeignKey(
        Continent, null=True, related_name='countries')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(max_length=250)
    is_capital = models.BooleanField(default=False)
    population = models.BigIntegerField()
    country = models.ForeignKey(
        Country, related_name='cities')

    class Meta:
        verbose_name_plural = 'cities'
        unique_together = ('name', 'country')
        ordering = ['name']

    def __str__(self):
        return self.name
