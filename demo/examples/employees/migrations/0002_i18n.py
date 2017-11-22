# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name_plural': 'departments', 'verbose_name': 'department', 'ordering': ['dept_no']},
        ),
        migrations.AlterModelOptions(
            name='deptemp',
            options={'verbose_name_plural': 'department employees', 'verbose_name': 'department employee'},
        ),
        migrations.AlterModelOptions(
            name='deptmanager',
            options={'verbose_name_plural': 'department managers', 'verbose_name': 'department manager', 'ordering': ['-from_date']},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name_plural': 'employees', 'verbose_name': 'employee'},
        ),
        migrations.AlterModelOptions(
            name='salary',
            options={'verbose_name_plural': 'salaries', 'verbose_name': 'salary', 'ordering': ['-from_date']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'verbose_name_plural': 'titles', 'verbose_name': 'title'},
        ),
        migrations.AlterField(
            model_name='department',
            name='dept_name',
            field=models.CharField(max_length=40, verbose_name='name', unique=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='dept_no',
            field=models.CharField(serialize=False, max_length=4, verbose_name='code', primary_key=True),
        ),
        migrations.AlterField(
            model_name='deptemp',
            name='department',
            field=models.ForeignKey(db_column='dept_no', on_delete=models.CASCADE, verbose_name='department', to='employees.Department'),
        ),
        migrations.AlterField(
            model_name='deptemp',
            name='employee',
            field=models.ForeignKey(db_column='emp_no', on_delete=models.CASCADE, verbose_name='employee', to='employees.Employee'),
        ),
        migrations.AlterField(
            model_name='deptemp',
            name='from_date',
            field=models.DateField(verbose_name='from'),
        ),
        migrations.AlterField(
            model_name='deptemp',
            name='to_date',
            field=models.DateField(verbose_name='to'),
        ),
        migrations.AlterField(
            model_name='deptmanager',
            name='department',
            field=models.ForeignKey(db_column='dept_no', on_delete=models.CASCADE, verbose_name='department', to='employees.Department'),
        ),
        migrations.AlterField(
            model_name='deptmanager',
            name='employee',
            field=models.ForeignKey(db_column='emp_no', on_delete=models.CASCADE, verbose_name='employee', to='employees.Employee'),
        ),
        migrations.AlterField(
            model_name='deptmanager',
            name='from_date',
            field=models.DateField(verbose_name='from'),
        ),
        migrations.AlterField(
            model_name='deptmanager',
            name='to_date',
            field=models.DateField(verbose_name='to'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='birth_date',
            field=models.DateField(verbose_name='birthday'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_no',
            field=models.IntegerField(serialize=False, verbose_name='employee number', primary_key=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(max_length=14, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(max_length=1, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(verbose_name='hire date'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(max_length=16, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='employee',
            field=models.ForeignKey(db_column='emp_no', on_delete=models.CASCADE, verbose_name='employee', to='employees.Employee'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='from_date',
            field=models.DateField(verbose_name='from'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='salary',
            field=models.IntegerField(verbose_name='salary'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='to_date',
            field=models.DateField(verbose_name='to'),
        ),
        migrations.AlterField(
            model_name='title',
            name='employee',
            field=models.ForeignKey(db_column='emp_no', on_delete=models.CASCADE, verbose_name='employee', to='employees.Employee'),
        ),
        migrations.AlterField(
            model_name='title',
            name='from_date',
            field=models.DateField(verbose_name='from'),
        ),
        migrations.AlterField(
            model_name='title',
            name='title',
            field=models.CharField(max_length=50, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='title',
            name='to_date',
            field=models.DateField(blank=True, null=True, verbose_name='to'),
        ),
    ]
