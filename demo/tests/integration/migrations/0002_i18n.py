# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integration', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'cities', 'verbose_name': 'city', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='continent',
            options={'verbose_name_plural': 'continents', 'verbose_name': 'continent', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'countries', 'verbose_name': 'country', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='ocean',
            options={'verbose_name_plural': 'oceans', 'verbose_name': 'ocean', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='sea',
            options={'verbose_name_plural': 'seas', 'verbose_name': 'sea', 'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(related_name='cities', on_delete=models.CASCADE, verbose_name='country', to='integration.Country'),
        ),
        migrations.AlterField(
            model_name='city',
            name='is_capital',
            field=models.BooleanField(default=False, verbose_name='is capital city'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=250, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='city',
            name='population',
            field=models.BigIntegerField(verbose_name='population'),
        ),
        migrations.AlterField(
            model_name='continent',
            name='area',
            field=models.BigIntegerField(help_text='km&#178;', verbose_name='area'),
        ),
        migrations.AlterField(
            model_name='continent',
            name='biggest_city',
            field=models.OneToOneField(verbose_name='biggest city', on_delete=models.CASCADE, blank=True, null=True, to='integration.City'),
        ),
        migrations.AlterField(
            model_name='continent',
            name='biggest_mountain',
            field=models.CharField(blank=True, null=True, max_length=250, verbose_name='biggest mountain'),
        ),
        migrations.AlterField(
            model_name='continent',
            name='largest_country',
            field=models.OneToOneField(related_name='+', on_delete=models.CASCADE, verbose_name='largest country', blank=True, null=True, to='integration.Country'),
        ),
        migrations.AlterField(
            model_name='continent',
            name='longest_river',
            field=models.CharField(blank=True, null=True, max_length=250, verbose_name='longest river'),
        ),
        migrations.AlterField(
            model_name='continent',
            name='name',
            field=models.CharField(serialize=False, max_length=250, verbose_name='name', primary_key=True),
        ),
        migrations.AlterField(
            model_name='continent',
            name='oceans',
            field=models.ManyToManyField(to='integration.Ocean', verbose_name='oceans'),
        ),
        migrations.AlterField(
            model_name='continent',
            name='population',
            field=models.BigIntegerField(verbose_name='population'),
        ),
        migrations.AlterField(
            model_name='continent',
            name='population_density',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='population density'),
        ),
        migrations.AlterField(
            model_name='country',
            name='code',
            field=models.CharField(max_length=3, verbose_name='code', unique=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='continent',
            field=models.ForeignKey(related_name='countries', on_delete=models.CASCADE, verbose_name='continent', null=True, to='integration.Continent'),
        ),
        migrations.AlterField(
            model_name='country',
            name='gay_friendly',
            field=models.NullBooleanField(verbose_name='gay friendly'),
        ),
        migrations.AlterField(
            model_name='country',
            name='independence_day',
            field=models.DateField(blank=True, null=True, verbose_name='independence day'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=250, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='ocean',
            name='area',
            field=models.BigIntegerField(verbose_name='area'),
        ),
        migrations.AlterField(
            model_name='ocean',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='ocean',
            name='map_url',
            field=models.URLField(verbose_name='map url'),
        ),
        migrations.AlterField(
            model_name='ocean',
            name='name',
            field=models.CharField(serialize=False, max_length=250, verbose_name='name', primary_key=True),
        ),
        migrations.AlterField(
            model_name='ocean',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='sea',
            name='area',
            field=models.BigIntegerField(help_text='km&#178;', verbose_name='area'),
        ),
        migrations.AlterField(
            model_name='sea',
            name='avg_depth',
            field=models.IntegerField(blank=True, null=True, help_text='meters', verbose_name='average depth'),
        ),
        migrations.AlterField(
            model_name='sea',
            name='max_depth',
            field=models.IntegerField(blank=True, null=True, help_text='meters', verbose_name='maximum depth'),
        ),
        migrations.AlterField(
            model_name='sea',
            name='name',
            field=models.CharField(max_length=250, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='sea',
            name='ocean',
            field=models.ForeignKey(to='integration.Ocean', on_delete=models.CASCADE, verbose_name='ocean'),
        ),
        migrations.AlterField(
            model_name='sea',
            name='parent',
            field=models.ForeignKey(verbose_name='parent', on_delete=models.CASCADE, blank=True, null=True, to='integration.Sea'),
        ),
    ]
