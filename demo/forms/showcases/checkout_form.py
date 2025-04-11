from django import forms
from viewflow.forms import Layout, FieldSet, Row, Column, Span, DependentModelSelect
from cookbook.crud101.atlas.models import Country
from . import COUNTRY_CHOICES, Form


class CheckoutForm(Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"leading-icon": "account_box"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"leading-icon": "account_box"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"leading-icon": "email"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"leading-icon": "call"}))
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    city = forms.CharField(
        widget=forms.Select(
            attrs={
                "tag": "vf-field-select-dependent",
                "parent": "country",
            },
        )
    )
    post_code = forms.CharField(
        widget=forms.Select(
            attrs={
                "tag": "vf-field-select-dependent",
                "parent": "city",
            },
        )
    )
    address = forms.CharField()
    additional_info = forms.CharField(widget=forms.Textarea)
    card_type = forms.ChoiceField(
        choices=(("V", "Visa"), ("M", "MasterCard"), ("P", "Paypal")),
        widget=forms.RadioSelect,
        label=None,
    )
    card_holder = forms.CharField(label="Name on card")
    card_number = forms.CharField(label="Card number")
    card_ccv2 = forms.IntegerField(label="CVV2")
    card_exp_month = forms.ChoiceField(
        choices=(
            (1, "January"),
            (2, "February"),
            (3, "March"),
            (4, "April"),
            (5, "May"),
            (6, "June"),
            (7, "July"),
            (8, "August"),
            (9, "September"),
            (10, "October"),
            (11, "November"),
            (12, "December"),
        )
    )
    card_exp_year = forms.IntegerField(label="Year")

    layout = Layout(
        Row("first_name", "last_name"),
        Row("email", "phone"),
        Row(
            Span("country", desktop=5),
            Span("city", desktop=5),
            Span("post_code", desktop=2),
        ),
        "address",
        "additional_info",
        FieldSet(
            "Card Details",
            Row(
                Column("card_type", desktop=4),
                Column(
                    "card_holder",
                    Row(Span("card_number", desktop=10), Span("card_ccv2", desktop=2)),
                    Row("card_exp_month", "card_exp_year"),
                    desktop=8,
                ),
            ),
        ),
    )

    # css = """
    # @media only screen and (min-width : 601px) {
    #     #id_card_type_container {
    #         margin-top: 40px;
    #         margin-left: 50px;
    #   }
    # """
