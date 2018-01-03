from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from material import ModelViewset

from . import models


class EmployeeViewset(ModelViewset):
    model = models.Employee
    list_columns = (
        'no', 'first_name', 'last_name',
        'birth_date', 'current_salary'
    )

    def no(self, obj):
        return '#{}'.format(obj.pk)

    def current_salary(self, obj):
        salary = obj.salary_set.current()
        return salary.salary if salary is not None else 0
    current_salary.short_description = _('current salary')


class DepartmentViewset(ModelViewset):
    model = models.Department
    list_columns = (
        'dept_no', 'dept_name', 'manager', 'employees'
    )

    def manager(self, obj, today=None):
        if today is None:
            today = timezone.now().date()
        manager = obj.deptmanager_set.filter(
            from_date__lte=today,
            to_date__gt=today
        ).first()
        return manager.employee if manager is not None else ''

    def employees(self, obj):
        return obj.deptemp_set.count()
    employees.short_description = _('employees')
