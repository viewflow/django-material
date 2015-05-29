import extra_views
from material import LayoutMixin, Layout, Fieldset, Inline, Row, Span2, Span5, Span7

from .models import Shipment, ShipmentItem


class ItemInline(extra_views.InlineFormSet):
    model = ShipmentItem
    fields = ['name', 'quantity']


class NewShipmentView(LayoutMixin,
                      extra_views.NamedFormsetsMixin,
                      extra_views.CreateWithInlinesView):
    title = "New Shipment"
    model = Shipment
    layout = Layout(
        Row('first_name', 'last_name', 'email'),
        Row('phone'),
        Fieldset('Address',
                 Row(Span7('address'), Span5('zipcode')),
                 Row(Span5('city'), Span2('state'), Span5('country'))),
        Inline('Shipment Items', ItemInline),
    )

