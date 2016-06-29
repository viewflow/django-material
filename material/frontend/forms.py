from django import forms
from django.forms import BaseFormSet


class DatatableRequestForm(forms.Form):
    draw = forms.IntegerField()
    start = forms.IntegerField()
    length = forms.IntegerField()
