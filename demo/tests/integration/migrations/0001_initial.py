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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('name', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('area', models.BigIntegerField(help_text='km&#178;')),
                ('population', models.BigIntegerField()),
                ('population_density', models.DecimalField(max_digits=8, decimal_places=2)),
                ('longest_river', models.CharField(blank=True, max_length=250, null=True)),
                ('biggest_mountain', models.CharField(blank=True, max_length=250, null=True)),
                ('hemisphere', models.CharField(max_length=5, choices=[('NORTH', 'North'), ('SOUTH', 'South'), ('BOTH', 'Both')])),
                ('biggest_city', models.OneToOneField(blank=True, null=True, to='integration.City')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('independence_day', models.DateField(blank=True, null=True)),
                ('gay_friendly', models.NullBooleanField()),
                ('continent', models.ForeignKey(null=True, related_name='countries', to='integration.Continent')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Ocean',
            fields=[
                ('name', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('area', models.BigIntegerField()),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Sea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=250)),
                ('area', models.BigIntegerField(help_text='km&#178;')),
                ('avg_depth', models.IntegerField(help_text='meters', null=True, blank=True)),
                ('max_depth', models.IntegerField(help_text='meters', null=True, blank=True)),
                ('basin_countries', models.ManyToManyField(blank=True, to='integration.Country', related_name='seas')),
                ('ocean', models.ForeignKey(to='integration.Ocean')),
                ('parent', models.ForeignKey(blank=True, null=True, to='integration.Sea')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='continent',
            name='largest_country',
            field=models.OneToOneField(blank=True, null=True, related_name='+', to='integration.Country'),
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
