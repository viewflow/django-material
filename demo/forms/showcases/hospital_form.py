import datetime

from django import forms
from viewflow.forms import Layout, Row, Column, Span, FieldSet, FormSetField
from . import QUESTION_CHOICES, CARDIOVASCULAR_RISK_CHOICES, APNIA_RISK_CHOICES, Form


class HospitalRegistrationForm(Form):
    class EmergencyContractForm(forms.Form):
        name = forms.CharField()
        relationship = forms.ChoiceField(
            choices=(
                ("SPS", "Spouse"),
                ("PRT", "Partner"),
                ("FRD", "Friend"),
                ("CLG", "Colleague"),
            )
        )
        daytime_phone = forms.CharField()
        evening_phone = forms.CharField(required=False)

    EmergencyContractFormSet = forms.formset_factory(
        EmergencyContractForm, extra=1, can_delete=True
    )

    registration_date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(),
    )
    full_name = forms.CharField()
    birth_date = forms.DateField()
    height = forms.IntegerField(help_text="cm")
    weight = forms.IntegerField(help_text="kg")
    primary_care_physician = forms.CharField(
        widget=forms.TextInput(attrs={"leading-icon": "face"})
    )
    date_of_last_appointment = forms.DateField(widget=forms.DateInput())
    home_phone = forms.CharField(widget=forms.TextInput(attrs={"leading-icon": "call"}))
    work_phone = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"leading-icon": "call"})
    )

    procedural_questions = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False,
        choices=QUESTION_CHOICES,
        label=None,
    )

    cardiovascular_risks = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"columns": 2}),
        required=False,
        choices=CARDIOVASCULAR_RISK_CHOICES,
        label=None,
    )

    apnia_risks = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"columns": 3}),
        required=False,
        choices=APNIA_RISK_CHOICES,
        label=None,
    )

    emergency_contacts = FormSetField(EmergencyContractFormSet, label=None)

    layout = Layout(
        Row(
            Column("full_name", "birth_date", Row("height", "weight"), desktop=8),
            "registration_date",
        ),
        Row(Span("primary_care_physician", desktop=8), "date_of_last_appointment"),
        Row("home_phone", "work_phone"),
        FieldSet("Procedural Questions", "procedural_questions"),
        FieldSet("Clinical Predictores of Cardiovascular Risk", "cardiovascular_risks"),
        FieldSet("Clinical Predictors of sleep Apnia Risk", "apnia_risks"),
        "emergency_contacts",
    )
