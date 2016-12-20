from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import TemporalQuerySet


class Department(models.Model):
    dept_no = models.CharField(primary_key=True, max_length=4)
    dept_name = models.CharField(unique=True, max_length=40)

    class Meta:
        db_table = 'departments'
        ordering = ['dept_no']

    def __str__(self):
        return self.dept_name


class DeptEmp(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, db_column='emp_no')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_no')
    from_date = models.DateField()
    to_date = models.DateField()

    objects = TemporalQuerySet.as_manager()

    class Meta:
        db_table = 'dept_emp'


class DeptManager(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, db_column='emp_no')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_no')
    from_date = models.DateField()
    to_date = models.DateField()

    objects = TemporalQuerySet.as_manager()

    class Meta:
        db_table = 'dept_manager'
        ordering = ['-from_date']


class Employee(models.Model):
    emp_no = models.IntegerField(primary_key=True)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=16)
    gender = models.CharField(max_length=1)
    hire_date = models.DateField()

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_no')
    salary = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()

    objects = TemporalQuerySet.as_manager()

    class Meta:
        db_table = 'salaries'
        ordering = ['-from_date']
        verbose_name = _('Salary')
        verbose_name_plural = _('Salaries')


class Title(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_no')
    title = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)

    objects = TemporalQuerySet.as_manager()

    class Meta:
        db_table = 'titles'
