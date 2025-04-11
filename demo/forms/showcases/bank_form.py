from django import forms
from viewflow.forms import Layout, FieldSet, Row, Column, Span
from . import COUNTRY_CHOICES, Form


class BankForm(Form):
    branch_name = forms.CharField()

    """ Personal Details """
    person_title = forms.ChoiceField(
        choices=(("Mr", "Mr."), ("Mrs.", "Mrs."), ("Ms.", "Ms.")), label="Title"
    )
    full_name = forms.CharField()
    date_of_birth = forms.DateField()
    email = forms.EmailField()
    parent_name = forms.CharField(label="In case of a minor please provide details")
    nationality = forms.ChoiceField(choices=COUNTRY_CHOICES)
    mobile_no = forms.CharField()
    existing_bank_account = forms.CharField()
    partner_name = forms.CharField(label="Name of father/spouse")

    """ Residential address """
    flat_building = forms.CharField(label="Flat no. and bldg. name")
    road_no = forms.CharField(label="Road no./name")
    area_and_landmark = forms.CharField(label="Area and landmark")
    telephone_residence = forms.CharField()
    city = forms.CharField()
    office = forms.CharField()
    fax = forms.CharField()
    pin_code = forms.CharField()

    """ Mailing Address """
    mailing_company_details = forms.CharField(
        label="Company name and department/ Flat no. and bldg. name"
    )
    mailing_road_no = forms.CharField(label="Road no./name")
    mailing_area_and_landmark = forms.CharField(label="Area and landmark")
    mailing_city = forms.CharField(label="City")
    mailing_mobile = forms.CharField(label="Mobile No.")
    mailing_telephone_residence = forms.CharField(label="Telephone Residence")
    mailing_office = forms.CharField(label="Office")
    mailing_fax = forms.CharField(label="Fax")
    mailing_pin_code = forms.CharField(label="Pin Code")
    mailing_email = forms.EmailField(label="E-mail")

    """ Details of Introduction by Existing Customer """
    introducer_name = forms.CharField(label="Customer Name")
    introducer_account_no = forms.CharField(label="Account No.")
    introducer_signature = forms.CharField(label="Introducer's signature")

    """ Account Details """
    account_type = forms.ChoiceField(
        choices=(("S", "Savings"), ("C", "Current"), ("F", "Fixed deposits")),
        label="Choice of account",
        widget=forms.RadioSelect(attrs={"inline": True}),
    )
    account_mode = forms.ChoiceField(
        choices=(("CS", "Cash"), ("CQ", "Cheque"), ("NF", "NEFT")),
        label="Mode of funding",
        widget=forms.RadioSelect(attrs={"inline": True}),
    )
    account_amount = forms.FloatField(label="Amount")

    """ Details of Fixed Deposit """
    deposit_type = forms.ChoiceField(
        choices=(("O", "Ordinary"), ("C", "Cumulative")),
        label="Types of deposit",
        widget=forms.RadioSelect(attrs={"inline": True}),
    )
    deposit_mode = forms.ChoiceField(
        choices=(("CS", "Cash"), ("CQ", "Cheque"), ("NF", "NEFT")),
        label="Mode of funding",
        widget=forms.RadioSelect(attrs={"inline": True}),
    )
    deposit_amount = forms.FloatField(label="Amount")
    deposit_no = forms.CharField(label="No. of deposits")
    deposit_individual_amount = forms.FloatField(label="Individual Deposit Amount")

    """ Personal Details """
    occupation = forms.ChoiceField(
        choices=(
            ("NE", "Non-executive"),
            ("HW", "Housewife"),
            ("RT", "Retired"),
            ("ST", "Student"),
            ("OT", "Other"),
            ("UN", "Unemployed"),
        ),
        widget=forms.RadioSelect,
    )
    job_title = forms.CharField()
    department = forms.CharField()
    nature_of_business = forms.CharField()
    education = forms.ChoiceField(
        choices=(("UG", "Under graduate"), ("GR", "Graduate"), ("OT", "Others")),
        widget=forms.RadioSelect,
    )
    monthly_income = forms.ChoiceField(
        choices=(
            ("000", "Zero Income"),
            ("L10", "Less than $10,000"),
            ("G10", "$10,000+"),
        ),
        widget=forms.RadioSelect,
    )
    martial_status = forms.ChoiceField(
        choices=(("M", "Married"), ("S", "Single")),
        widget=forms.RadioSelect(attrs={"inline": True}),
    )
    spouse_name = forms.CharField()

    """ Other existing bank accounts, if any """
    other_account1 = forms.CharField(label="Name of the Bank / branch")
    other_account2 = forms.CharField(label="Name of the Bank / branch")

    """ Reason for Account opening """
    reason = forms.CharField(label="Please specify", widget=forms.Textarea)

    """ Terms And Conditions """
    terms_accepted = forms.BooleanField(
        label="I/We confirm having read and understood the account rules of The Banking Corporation Limited"
        " ('the Bank'), and hereby agree to be bound by the terms and conditions and amendments governing the"
        " account(s) issued by the Bank from time-to-time."
    )

    layout = Layout(
        FieldSet("Please open an account at", "branch_name"),
        FieldSet(
            "Personal Details (Sole/First Accountholder/Minor)",
            Row(Span("person_title", desktop=2), Span("full_name", desktop=10)),
            Row(
                Column("date_of_birth", "email", "parent_name"),
                Column(
                    "nationality",
                    Row("mobile_no", "existing_bank_account"),
                    "partner_name",
                ),
            ),
        ),
        FieldSet(
            "Residential address",
            Row("flat_building", "road_no"),
            Row(Span("area_and_landmark", desktop=10), Span("city", desktop=2)),
            Row("telephone_residence", "office", "fax", "pin_code"),
        ),
        FieldSet(
            "Mailing Address (If different from the First Accountholder's address)",
            "mailing_company_details",
            Row(
                "mailing_road_no",
                "mailing_area_and_landmark",
                "mailing_city",
                "mailing_mobile",
            ),
            Row(
                "mailing_telephone_residence",
                "mailing_office",
                "mailing_fax",
                "mailing_pin_code",
            ),
            "mailing_email",
        ),
        FieldSet(
            "Details of Introduction by Existing Customer (If applicable)",
            Row("introducer_name", "introducer_account_no"),
            "introducer_signature",
        ),
        FieldSet(
            "Account Details", Row("account_type", "account_mode"), "account_amount"
        ),
        FieldSet(
            "Details of Fixed Deposit",
            Row("deposit_type", "deposit_mode"),
            Row(
                Span("deposit_amount", desktop=6),
                Span("deposit_no", desktop=3),
                Span("deposit_individual_amount", desktop=3),
            ),
        ),
        FieldSet(
            "Personal Details",
            Row("occupation", "education", "monthly_income"),
            "job_title",
            Row("department", "nature_of_business"),
            Row("martial_status", "spouse_name"),
        ),
        FieldSet(
            "Other existing bank accounts, if any",
            Row("other_account1", "other_account2"),
        ),
        FieldSet("Reason for Account opening", "reason"),
        FieldSet("Terms And Conditions", "terms_accepted"),
    )
