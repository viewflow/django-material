from django import forms
from material.forms import Layout, Row, Span
from material.forms.renderers import MaterialFormRenderer


class CheckboxInputForm(forms.Form):
    field1 = forms.BooleanField(help_text="default", required=False)
    field2 = forms.BooleanField(help_text="initial value", initial=True)
    field3 = forms.BooleanField(help_text="disabled", disabled=True, initial=True)
    field4 = forms.BooleanField(
        help_text="on a row with textfield",
        widget=forms.CheckboxInput(attrs={"color": "secondary"}),
    )
    textfield = forms.CharField(
        help_text="with boolean", widget=forms.TextInput(attrs={"leading-icon": "edit"})
    )

    default_renderer = MaterialFormRenderer()

    layout = Layout(
        "field1",
        "field2",
        "field3",
        Row(Span("textfield", desktop=9), Span("field4", desktop=3)),
    )
