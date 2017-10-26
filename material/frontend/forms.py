import re

from django import forms


ORDER_RE = re.compile(r'datatable-order\[(\d+)\]\[(\w+)\]')


class DatatableRequestForm(forms.Form):
    """Sanitize  incoming datatables request."""

    draw = forms.IntegerField()
    start = forms.IntegerField()
    length = forms.IntegerField()

    def clean_ordering(self):
        order = {}
        for key, value in self.data.items():
            if key.startswith('datatable-order['):
                match = ORDER_RE.match(key)
                pos, attr = match.groups()
                if pos not in order:
                    order[pos] = {}
                order[pos][attr] = value

        self.cleaned_data['ordering'] = [spec[1] for spec in sorted(order.items())]

    def clean(self):
        self.clean_ordering()
        return self.cleaned_data
