from django import forms
from viewflow.forms import ModelForm, ForeignKeyFormField
from . import models


class ContinentForm(ModelForm):
    name = forms.CharField(disabled=True)

    class Meta:
        fields = ['name', 'area']
        model = models.Continent


class CountryForm(ModelForm):
    continent = ForeignKeyFormField(ContinentForm)

    class Meta:
        fields = '__all__'
        model = models.Country
