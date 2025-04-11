from django import forms
from viewflow.forms import Layout, Row
from . import Form


class CommentForm(Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"leading-icon": "account_box"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"leading-icon": "email"}))
    website = forms.URLField(
        widget=forms.URLInput(attrs={"leading-icon": "card_travel"})
    )
    comment = forms.CharField(widget=forms.Textarea())
    layout = Layout(Row("name", "email"), "website", "comment")
