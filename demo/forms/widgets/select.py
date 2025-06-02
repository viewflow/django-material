from django import forms
from material.forms.layout import Layout, Row, Span


class SelectForm(forms.Form):
    title = "Select"
    subtitle = "Widget options demo"

    CHOICES = ((None, "Select a fruit"), (1, "Apple"), (2, "Orange"), (3, "Watermelon"))
    FLOAT_CHOICES = (
        (None, ""),
        (1.1, "Perfect"),
        (1.0, "Good"),
        (0.8, "Bad"),
    )
    GROUPED_CHOICES = (
        (None, [(7, "Mikhail")]),
        ("Team 1", [(1, "Joe"), (2, "Bob"), (3, "Marie")]),
        ("Team 2", [(4, "Anatoliy"), (5, "Svetlana"), (6, "Olga")]),
    )
    LONG_CHOICES = ((n, n) for n in range(100))

    field1 = forms.ChoiceField(help_text="default", choices=CHOICES, required=False)
    field2 = forms.ChoiceField(help_text="initial value", choices=CHOICES, initial=2)
    field3 = forms.ChoiceField(help_text="float choices", choices=FLOAT_CHOICES)
    field4 = forms.ChoiceField(help_text="groups", choices=GROUPED_CHOICES)
    field5 = forms.ChoiceField(help_text="long choices list", choices=LONG_CHOICES)
    field6 = forms.TypedChoiceField(
        help_text="coerce to int", coerce=int, choices=CHOICES
    )
    field7 = forms.ChoiceField(
        help_text="prefix",
        choices=CHOICES,
        widget=forms.Select(attrs={"leading-icon": "account_box"}),
    )
    field8 = forms.ChoiceField(help_text="on a row with textfield", choices=CHOICES)
    textfield = forms.CharField(
        help_text="with select", widget=forms.TextInput(attrs={"leading-icon": "edit"})
    )
    field9 = forms.ChoiceField(
        help_text="disabled", disabled=True, choices=CHOICES, initial=3
    )

    layout = Layout(
        "field1",
        "field2",
        "field3",
        "field4",
        "field5",
        "field6",
        "field7",
        Row("textfield", Span("field8", desktop=3)),
        "field9",
    )

    def clean_field5(self):
        data = self.cleaned_data["field5"]
        if data == "0":
            raise forms.ValidationError("Please, do not select zero")
        return data

