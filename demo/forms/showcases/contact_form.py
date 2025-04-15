from django import forms

from material.forms import Layout, Row
from material.forms.renderers import MaterialFormRenderer


class ContactForm(forms.Form):
    default_renderer = MaterialFormRenderer()
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"leading-icon": "account_box"},
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"leading-icon": "email"},
        ),
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={"leading-icon": "announcement"},
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
    )
    send_copy = forms.BooleanField(
        required=False,
        label="Send a copy to my e-mail address",
    )

    layout = Layout(
        Row("name", "email"),
        "subject",
        "message",
        "send_copy",
    )
