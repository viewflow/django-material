from django import forms

class CheckboxInputForm(forms.Form):
    field1 = forms.BooleanField(help_text="default", required=False)
    field2 = forms.BooleanField(help_text="initial value", initial=True)
    field3 = forms.BooleanField(help_text="disabled", disabled=True, initial=True)
    field4 = forms.BooleanField(help_text="on a row with textfield")
