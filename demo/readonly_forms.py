from datetime import date
from django.template import Template

from . import forms


class LoginForm(forms.LoginForm):
    initial = {
        'email': 'john@doe.com',
        'password': 'password',
        'keep_logged': True
    }

    template = Template("""
    {% form template='material/readonly/form.html' %}
        {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.password prefix %}<i class="material-icons prefix">lock</i>{% endpart %}
        {% attr form.keep_logged 'group' class append %}right-align{% endattr %}
    {% endform %}
    """)


class RegistrationForm(forms.RegistrationForm):
    initial = {
        'username': 'jdoe',
        'email': 'john@doe.com',
        'password': 'password',
        'password_confirm': 'password',
        'first_name': 'John',
        'last_name': 'Doe',
        'gender': 'O',
        'receive_news': False,
        'agree_toc': True
    }

    template = Template("""
    {% form template='material/readonly/form.html' %}
        {% part form.username prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
        {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.password %}{% endpart %}
        {% part form.password_confirm %}{% endpart %}
    {% endform %}
    """)


class ContactForm(forms.ContactForm):
    initial = {
        'name': 'John Doe',
        'email': 'john@doe.com',
        'subject': 'Viewflow order question',
        'message': 'Can we pay over SWIFT?',
        'send_copy': True
    }

    template = Template("""
    {% form template='material/readonly/form.html' %}
        {% part form.name prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
        {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.subject prefix %}<i class="material-icons prefix">announcement</i>{% endpart %}
        {% part form.message prefix %}<i class="material-icons prefix">message</i>{% endpart %}
        {% attr form.send_copy 'group' class append %}right-align{% endattr %}
    {% endform %}
    """)


class OrderForm(forms.OrderForm):
    initial = {
        'name': 'John Doe',
        'company': 'Engineering and Manufacture Ltd',
        'email': 'john@doe.com',
        'phone': '+1-555-5555-555',
        'interest': 'C',
        'budget': 'M',
        'start_date': date(2018, 1, 1),
        'finish_date': date(2018, 1, 31),
        'message': 'Hi, would like to develop and ERP sustem basaed on the Viewflow Suite.',
    }

    template = Template("""
    {% form template='material/readonly/form.html' %}
        {% part form.name prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
        {% part form.company prefix %}<i class="material-icons prefix">business</i>{% endpart %}
        {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.phone prefix %}<i class="material-icons prefix">call</i>{% endpart %}
    {% endform %}
    """)


class CheckoutForm(forms.CheckoutForm):
    initial = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@doe.com',
        'phone': '+1-555-5555-555',
        'country': 'United States',
        'city': 'New York',
        'post_code': '0501',
        'address': 'Nowhere st 5',
        'additional_info': 'Keep calm and Carry On',
        'card_type': 'V',
        'card_holder': 'John Doe',
        'card_number': '4012888888881881',
        'card_ccv2': '321',
        'card_exp_month': 1,
        'card_exp_year': 2038,
    }

    template = Template("""
    {% form template='material/readonly/form.html' %}
        {% part form.first_name prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
        {% part form.last_name prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
        {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.phone prefix %}<i class="material-icons prefix">call</i>{% endpart %}
        {% part form.card_type label %}{% endpart %}
    {% endform %}
    """)


class CommentForm(forms.CommentForm):
    initial = {
        'name': 'John Doe',
        'email': 'john@doe.com',
        'website': 'https//me.johndoe',
        'comment': 'Thank you for the amazing framework!',
    }

    template = Template("""
    {% form template='material/readonly/form.html' %}
        {% part form.name prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
        {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.website prefix %}<i class="material-icons prefix">card_travel</i>{% endpart %}
        {% part form.comment prefix %}<i class="material-icons prefix">chat</i>{% endpart %}
    {% endform %}
    """)


class BankForm(forms.BankForm):
    initial = {
        'branch_name': 'Main branch',
        # Personal Details
        'person_title': 'Mr',
        'full_name': 'John Doe',
        'date_of_birth': date(1983, 8, 2),
        'email': 'john@doe.com',
        'parent_name': '-',
        'nationality': 'COUNTRY_CHOICES',
        'mobile_no': '+1-555-5555-555',
        'existing_bank_account': '-',
        'partner_name': '-',

        # Residential address
        'flat_bulding': '',
        'road_no': '',
        'area_and_landmark': '',
        'telephone_residence': '',
        'city': '',
        'office': '',
        'fax': '',
        'pin_code': '',

        # Mailing Address
        'mailing_company_details': '',
        'mailing_road_no': '',
        'mailing_area_and_landmark': '',
        'mailing_city': '',
        'mailing_mobile': '',
        'mailing_telephone_residence': '',
        'mailing_office': '',
        'mailing_fax': '',
        'mailing_pin_code': '',
        'mailing_email': '',

        # Details of Introduction by Existing Customer
        'introducer_name': '',
        'introducer_account_no': '',
        'introducer_signature': '',

        # Account Details
        'account_type': 'F',
        'account_mode': 'CQ',
        'account_amount': '',

        # Details of Fixed Deposit
        'deposit_type': '0',
        'deposit_mode': 'NF',
        'deposit_amount': 100000,
        'deposit_no': '',
        'deposit_individual_amount': 1000,

        # Personal Details
        'occupation': 'HW',
        'job_title': '',
        'department': '',
        'nature_of_business': '',
        'education': 'GR',
        'montly_income': 'G10',
        'martial_status': 'M',
        'spouse_name': '',

        # Other existing bank accounts, if any
        'other_account1': '',
        'other_account2': '',

        # Reason for Account opening
        'reason': '',

        # Terms And Conditions
        'terms_accepted': True
    }

    template = Template("""
    {% form template='material/readonly/form.html' %}
        {% attr form.account_type 'group' class append %}inline{% endattr %}
        {% attr form.account_mode 'group' class append %}inline{% endattr %}
        {% attr form.deposit_type 'group' class append %}inline{% endattr %}
        {% attr form.deposit_mode 'group' class append %}inline{% endattr %}
        {% attr form.martial_status 'group' class append %}inline{% endattr %}
    {% endform %}
    """)

