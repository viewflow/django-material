from django import forms


class DatatableRequestForm(forms.Form):
    """Sanitize  incoming datatables request."""

    draw = forms.IntegerField()
    start = forms.IntegerField()
    length = forms.IntegerField()
