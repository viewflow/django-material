from django import forms
from material.forms import Layout, Row
from material.forms.renderers import MaterialFormRenderer


class AddressForm(forms.Form):
    default_renderer = MaterialFormRenderer()
    line_1 = forms.CharField(max_length=250)
    line_2 = forms.CharField(max_length=250)
    state = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    zipcode = forms.CharField(max_length=10)

    layout = Layout(
        "line_1",
        "line_2",
        "state",
        Row("city", "zipcode"),
    )


class ProfileForm(forms.Form):
    default_renderer = MaterialFormRenderer()
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    # Commented out to fix import error
    # address = FormField(form_class=AddressForm)

    layout = Layout(
        "username",
        Row("first_name", "last_name"),
        # Commented out until FormField is implemented
        # , "address"
    )
