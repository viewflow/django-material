from django import forms
from material.forms import Layout, Row
from material.forms.renderers import MaterialFormRenderer
from . import Form


class CommentForm(forms.Form):
    default_renderer = MaterialFormRenderer()
    name = forms.CharField(widget=forms.TextInput(attrs={"leading-icon": "account_box"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"leading-icon": "email"}))
    website = forms.URLField(widget=forms.URLInput(attrs={"leading-icon": "card_travel"}))
    comment = forms.CharField(widget=forms.Textarea())
    layout = Layout(Row("name", "email"), "website", "comment")
