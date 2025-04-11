from django import forms
from material.forms.renderers import MaterialFormRenderer


class LoginForm(forms.Form):
    default_renderer = MaterialFormRenderer()
    email = forms.EmailField(widget=forms.EmailInput(attrs={"leading-icon": "email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"leading-icon": "lock"})
    )
    keep_logged = forms.BooleanField(required=False, label="Keep me logged in")

    #  {% attr form.keep_logged 'group' class append %}right-align{% endattr %}

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if cleaned_data.get("email") == "john@doe.com":
            raise forms.ValidationError("John, come on. You are blocked.")
