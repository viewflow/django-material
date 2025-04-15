from django import forms

from material.forms import FieldSet, Layout, Row
from material.forms.renderers import MaterialFormRenderer


class RegistrationForm(forms.Form):
    default_renderer = MaterialFormRenderer()
    username = forms.CharField(widget=forms.TextInput(attrs={"leading-icon": "account_box"}))
    email = forms.EmailField(
        label="Email Address", widget=forms.EmailInput(attrs={"leading-icon": "email"})
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"leading-icon": "lock_open"}))
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=((None, ""), ("F", "Female"), ("M", "Male"), ("O", "Other")))
    receive_news = forms.BooleanField(
        required=False, label="I want to receive news and special offers"
    )
    agree_toc = forms.BooleanField(required=True, label="I agree with the Terms and Conditions")

    layout = Layout(
        "username",
        "email",
        Row("password", "password_confirm"),
        FieldSet(
            "Personal details",
            Row("first_name", "last_name"),
            "gender",
            "receive_news",
            "agree_toc",
        ),
    )
