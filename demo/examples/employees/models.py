from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from .managers import TemporalQuerySet


@python_2_unicode_compatible
class Department(models.Model):
    dept_no = models.CharField(_('code'), primary_key=True, max_length=4)
    dept_name = models.CharField(_('name'), unique=True, max_length=40)

    class Meta:
        verbose_name = _('department')
        verbose_name_plural = _('departments')
        db_table = 'departments'
        ordering = ['dept_no']

    def __str__(self):
        return self.dept_name


@python_2_unicode_compatible
class DeptEmp(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, db_column='emp_no', verbose_name=_('employee'))
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_no', verbose_name=_('department'))
    from_date = models.DateField(_('from'))
    to_date = models.DateField(_('to'))

    objects = TemporalQuerySet.as_manager()

    class Meta:
        verbose_name = _('department employee')
        verbose_name_plural = _('department employees')
        db_table = 'dept_emp'

    def __str__(self):
        return "{} - {}".format(self.employee, self.department)


@python_2_unicode_compatible
class DeptManager(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, db_column='emp_no', verbose_name=_('employee'))
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_no', verbose_name=_('department'))
    from_date = models.DateField(_('from'))
    to_date = models.DateField(_('to'))

    objects = TemporalQuerySet.as_manager()

    class Meta:
        verbose_name = _('department manager')
        verbose_name_plural = _('department managers')
        db_table = 'dept_manager'
        ordering = ['-from_date']

    def __str__(self):
        return "{} - {}".format(self.employee, self.department)


@python_2_unicode_compatible
class Employee(models.Model):
    emp_no = models.IntegerField(_('employee number'), primary_key=True)
    birth_date = models.DateField(_('birthday'))
    first_name = models.CharField(_('first name'), max_length=14)
    last_name = models.CharField(_('last name'), max_length=16)
    gender = models.CharField(_('gender'), max_length=1)
    hire_date = models.DateField(_('hire date'))

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
        db_table = 'employees'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


@python_2_unicode_compatible
class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_no', verbose_name=_('employee'))
    salary = models.IntegerField(_('salary'))
    from_date = models.DateField(_('from'))
    to_date = models.DateField(_('to'))

    objects = TemporalQuerySet.as_manager()

    class Meta:
        db_table = 'salaries'
        ordering = ['-from_date']
        verbose_name = _('salary')
        verbose_name_plural = _('salaries')

    def __str__(self):
        return "{} - {}".format(self.employee, self.salary)


@python_2_unicode_compatible
class Title(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_no', verbose_name=_('employee'))
    title = models.CharField(_('title'), max_length=50)
    from_date = models.DateField(_('from'))
    to_date = models.DateField(_('to'), blank=True, null=True)

    objects = TemporalQuerySet.as_manager()

    class Meta:
        verbose_name = _('title')
        verbose_name_plural = _('titles')
        db_table = 'titles'

    def __str__(self):
        return "{} - {}".format(self.employee, self.title)
