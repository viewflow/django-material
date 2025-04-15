from django import forms
from material.forms import Layout, Row, Span
from material.forms.renderers import MaterialFormRenderer


class TextInputForm(forms.Form):
    title = "TextInput"
    subtitle = "Widget options demo"

    field1 = forms.CharField(help_text="default", required=False)
    field2 = forms.CharField(help_text="initial value", initial="Initial value")
    field3 = forms.CharField(help_text="length between 5-10", min_length=5, max_length=10)
    field4 = forms.CharField(
        help_text="prefix icon", widget=forms.TextInput(attrs={"leading_icon": "edit"})
    )
    field5 = forms.CharField(
        help_text="suffix icon",
        widget=forms.TextInput(attrs={"trailing_icon": "perm_contact_calendar"}),
    )
    field6 = forms.CharField(initial="No help text")
    field7 = forms.CharField(help_text="disabled", disabled=True, initial="Not editable")

    default_renderer = MaterialFormRenderer()

    layout = Layout("field1", "field2", "field3", "field4", "field5", Row("field6", "field7"))

    def clean_field5(self):
        data = self.cleaned_data["field5"]
        if data != "1":
            raise forms.ValidationError("Please, input 1!")
        return data
