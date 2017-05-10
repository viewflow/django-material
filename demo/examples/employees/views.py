import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext, ugettext_lazy as _

from material.frontend.views import ModelViewSet, ListModelView

from . import models, forms


@login_required
def change_manager(request, department_pk):
    department = get_object_or_404(models.Department, pk=department_pk)
    form = forms.ChangeManagerForm(department=department, data=request.POST or None)

    if form.is_valid():
        form.save()

    return render(request, 'employees/change_manager.html', {
        'form': form,
        'department': department,
        'model': models.Department
    })


@login_required
def change_salary(request, employee_pk):
    employee = get_object_or_404(models.Employee, pk=employee_pk)
    form = forms.ChangeSalaryForm(employee=employee, data=request.POST or None)

    if form.is_valid():
        form.save()

    salaries = employee.salary_set.all().order_by('from_date')
    salary_data = {
        'labels': [salary.from_date.strftime('%Y-%m-%d') for salary in salaries],
        'datasets': [
            {'data': [salary.salary for salary in salaries], 'label': ugettext('Salary History')}
        ]
    }

    return render(request, 'employees/change_salary.html', {
        'form': form,
        'employee': employee,
        'salary_history': json.dumps(salary_data),
        'model': models.Employee
    })


@login_required
def change_title(request, employee_pk):
    employee = get_object_or_404(models.Employee, pk=employee_pk)
    form = forms.ChangeTitleForm(employee=employee, data=request.POST or None)

    if form.is_valid():
        form.save()

    return render(request, 'employees/change_title.html', {
        'form': form,
        'employee': employee,
        'model': models.Employee
    })


class DepartmentEmployesListView(ListModelView):
    model = models.Employee
    list_display = ('emp_no', 'first_name', 'last_name', 'current_salary')
    template_name = 'employees/department_employees.html'

    def get_queryset(self):
        today = timezone.now().date()
        department = get_object_or_404(models.Department, pk=self.kwargs['department_pk'])
        queryset = super(DepartmentEmployesListView, self).get_queryset()

        return queryset.filter(
            deptemp__department=department,
            deptemp__from_date__lte=today,
            deptemp__to_date__gt=today
        )

    def get_context_data(self, **kwargs):
        department = get_object_or_404(models.Department, pk=self.kwargs['department_pk'])
        return super(DepartmentEmployesListView, self).get_context_data(
            department=department, **kwargs)


class EmployeeViewSet(ModelViewSet):
    model = models.Employee
    list_display = ('emp_no', 'first_name', 'last_name', 'birth_date', 'current_salary')

    change_salary_view = [
        r'^(?P<employee_pk>.+)/change_salary/$',
        change_salary,
        '{model_name}_change_salary'
    ]

    change_title_view = [
        r'^(?P<employee_pk>.+)/change_title/$',
        change_title,
        '{model_name}_change_title'
    ]

    def current_salary(self, obj):
        salary = obj.salary_set.current()
        return salary.salary if salary is not None else 0
    current_salary.short_description = _('current salary')


class DepartmentViewSet(ModelViewSet):
    model = models.Department
    list_display = ('dept_no', 'dept_name', 'manager', 'employees')

    change_manager_view = [
        r'^(?P<department_pk>.+)/change_manager/$',
        change_manager,
        '{model_name}_change_manager'
    ]

    employees_list_view = [
        r'^(?P<department_pk>.+)/employees/$',
        DepartmentEmployesListView.as_view(viewset=EmployeeViewSet()),
        '{model_name}_employees'
    ]

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
