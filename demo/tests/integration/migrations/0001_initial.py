# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('is_capital', models.BooleanField(default=False)),
                ('population', models.BigIntegerField()),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, max_length=250)),
                ('area', models.BigIntegerField(help_text='km&#178;')),
                ('population', models.BigIntegerField()),
                ('population_density', models.DecimalField(decimal_places=2, max_digits=8)),
                ('longest_river', models.CharField(max_length=250, blank=True, null=True)),
                ('biggest_mountain', models.CharField(max_length=250, blank=True, null=True)),
                ('hemisphere', models.CharField(max_length=5, choices=[('NORTH', 'North'), ('SOUTH', 'South'), ('BOTH', 'Both')])),
                ('biggest_city', models.OneToOneField(on_delete=models.CASCADE, blank=True, null=True, to='integration.City')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('independence_day', models.DateField(blank=True, null=True)),
                ('gay_friendly', models.NullBooleanField()),
                ('continent', models.ForeignKey(to='integration.Continent', on_delete=models.CASCADE, related_name='countries', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Ocean',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, max_length=250)),
                ('area', models.BigIntegerField()),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('map_url', models.URLField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Sea',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('area', models.BigIntegerField(help_text='km&#178;')),
                ('avg_depth', models.IntegerField(help_text='meters', blank=True, null=True)),
                ('max_depth', models.IntegerField(help_text='meters', blank=True, null=True)),
                ('basin_countries', models.ManyToManyField(to='integration.Country', blank=True, related_name='seas')),
                ('ocean', models.ForeignKey(to='integration.Ocean', on_delete=models.CASCADE)),
                ('parent', models.ForeignKey(on_delete=models.CASCADE, blank=True, null=True, to='integration.Sea')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='continent',
            name='largest_country',
            field=models.OneToOneField(to='integration.Country', on_delete=models.CASCADE, blank=True, null=True, related_name='+'),
        ),
        migrations.AddField(
            model_name='continent',
            name='oceans',
            field=models.ManyToManyField(to='integration.Ocean'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='integration.Country', on_delete=models.CASCADE, related_name='cities'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('name', 'country')]),
        ),
    ]
