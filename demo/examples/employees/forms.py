from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Employee, DeptManager, Title, Salary


class ChangeManagerForm(forms.Form):
    manager = forms.ModelChoiceField(queryset=Employee.objects.all()[:100], label=_('Manager'))

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department')
        super(ChangeManagerForm, self).__init__(*args, **kwargs)

    def save(self):
        new_manager = self.cleaned_data['manager']

        DeptManager.objects.filter(
            department=self.department
        ).set(
            department=self.department,
            employee=new_manager
        )


class ChangeTitleForm(forms.Form):
    position = forms.CharField(label=_('Position'))

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')
        super(ChangeTitleForm, self).__init__(*args, **kwargs)

    def save(self):
        new_title = self.cleaned_data['position']

        Title.objects.filter(
            employee=self.employee,
        ).set(
            employee=self.employee,
            title=new_title
        )


class ChangeSalaryForm(forms.Form):
    salary = forms.IntegerField(max_value=1000000, label=_('Salary'))

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')
        super(ChangeSalaryForm, self).__init__(*args, **kwargs)

    def save(self):
        new_salary = self.cleaned_data['salary']

        Salary.objects.filter(
            employee=self.employee,
        ).set(
            employee=self.employee,
            salary=new_salary,
        )
