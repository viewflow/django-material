from django import forms
from material import (
    Layout, Row, Fieldset, Icon,
    MaterialTextInput, MaterialEmailInput, MaterialPasswordInput
)


class RegistrationForm(forms.Form):
    title = "Registration Form"

    username = forms.CharField(
        widget=MaterialTextInput(prefix=Icon('account_box'))
    )
    email = forms.EmailField(
        label="Email Address",
        widget=MaterialEmailInput(prefix=Icon('email'))
    )
    password = forms.CharField(
        widget=MaterialPasswordInput(prefix=Icon('lock_open'))
    )
    password_confirm = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput
    )
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=((None, ''), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')

    layout = Layout(
        'username', 'email',
        Row('password', 'password_confirm'),
        Fieldset(
            'Personal details',
            Row('first_name', 'last_name'),
            'gender'
        ),
        'receive_news', 'agree_toc'
    )
