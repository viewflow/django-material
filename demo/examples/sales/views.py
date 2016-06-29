from django.views.generic import CreateView
from material import LayoutMixin, Layout, Fieldset, Row, Span2, Span5, Span7

from .models import Shipment


class NewShipmentView(LayoutMixin, CreateView):
    title = "New Shipment"
    model = Shipment
    layout = Layout(
        Row('first_name', 'last_name', 'email'),
        Row('phone'),
        Fieldset('Address',
                 Row(Span7('address'), Span5('zipcode')),
                 Row(Span5('city'), Span2('state'), Span5('country'))),
    )
