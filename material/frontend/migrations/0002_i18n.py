# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='module',
            options={'verbose_name_plural': 'modules', 'verbose_name': 'module'},
        ),
        migrations.AlterField(
            model_name='module',
            name='installed',
            field=models.BooleanField(default=True, verbose_name='installed'),
        ),
        migrations.AlterField(
            model_name='module',
            name='label',
            field=models.SlugField(verbose_name='label'),
        ),
    ]
