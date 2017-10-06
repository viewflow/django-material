from django import forms
from material import Layout, Row, Fieldset


class RegistrationForm(forms.Form):
    title = "Registration Form"

    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=((None, ''), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')

    layout = Layout(
        'username', 'email',
        Row('password', 'password_confirm'),
        Fieldset(
            'Pesonal details',
            Row('first_name', 'last_name'),
            'gender'
        ),
        'receive_news', 'agree_toc'
    )
