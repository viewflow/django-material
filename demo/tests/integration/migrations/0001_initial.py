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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('is_capital', models.BooleanField(default=False)),
                ('population', models.IntegerField()),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('name', models.CharField(primary_key=True, max_length=250, serialize=False)),
                ('area', models.IntegerField(help_text='km&#178;')),
                ('population', models.IntegerField()),
                ('population_density', models.DecimalField(max_digits=8, decimal_places=2)),
                ('longest_river', models.CharField(blank=True, max_length=250, null=True)),
                ('biggest_mountain', models.CharField(blank=True, max_length=250, null=True)),
                ('hemisphere', models.CharField(max_length=5, choices=[('NORTH', 'North'), ('SOUTH', 'South'), ('BOTH', 'Both')])),
                ('biggest_city', models.OneToOneField(null=True, blank=True, to='integration.City')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('independence_day', models.DateField(blank=True, null=True)),
                ('gay_friendly', models.NullBooleanField()),
                ('continent', models.ForeignKey(null=True, to='integration.Continent', related_name='countries')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Ocean',
            fields=[
                ('name', models.CharField(primary_key=True, max_length=250, serialize=False)),
                ('area', models.IntegerField()),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Sea',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('area', models.IntegerField(help_text='km&#178;')),
                ('avg_depth', models.IntegerField(help_text='meters')),
                ('max_depth', models.IntegerField(help_text='meters')),
                ('basin_countries', models.ManyToManyField(blank=True, to='integration.Country', related_name='seas')),
                ('ocean', models.ForeignKey(to='integration.Ocean')),
                ('parent', models.ForeignKey(null=True, blank=True, to='integration.Sea')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='continent',
            name='largest_country',
            field=models.OneToOneField(null=True, blank=True, to='integration.Country', related_name='+'),
        ),
        migrations.AddField(
            model_name='continent',
            name='oceans',
            field=models.ManyToManyField(to='integration.Ocean'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='integration.Country', related_name='cities'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('name', 'country')]),
        ),
    ]
