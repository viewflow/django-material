from django import forms
from viewflow.forms import Layout, Row
from . import Form


class OrderForm(Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"leading-icon": "account_box"})
    )
    company = forms.CharField(
        widget=forms.TextInput(attrs={"leading-icon": "business"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"leading-icon": "email"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"leading-icon": "call"}))
    interest = forms.ChoiceField(
        choices=(
            (None, "Interested in"),
            ("D", "Design"),
            ("C", "Development"),
            ("I", "Illustration"),
            ("B", "Branding"),
            ("V", "Video"),
        )
    )
    budget = forms.ChoiceField(
        choices=(
            (None, "Budget"),
            ("S", "Less than $5000"),
            ("M", "$5000-$10000"),
            ("L", "$10000-$20000"),
            ("XL", "More than $20000"),
        )
    )
    start_date = forms.DateField(label="Expected start date")
    finish_date = forms.DateField(label="Expected finish date")
    attachment = forms.FileField(label="Include some file...")
    message = forms.CharField(widget=forms.Textarea)

    layout = Layout(
        "name",
        "company",
        "email",
        "phone",
        Row("interest", "budget"),
        Row("start_date", "finish_date"),
        "attachment",
        "message",
    )
