from django.conf.urls import url
from django.test.utils import override_settings
from django.views import generic
from django_webtest import WebTest
from .. import forms


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/checkout/')

        form = page.form
        form['first_name'] = 'John'
        form['last_name'] = 'Doe'
        form['email'] = 'john@doe.com'
        form['phone'] = '5-555-4200-11'
        form['country'] = 4
        form['city'] = 'Proudvill'
        form['post_code'] = '00520'
        form['address'] = 'Nowhere St, 5'
        form['additional_info'] = 'No info'
        form['card_type'] = 'V'
        form['card_holder'] = 'JOHN DOE'
        form['card_number'] = 'XXXX XXXX XXXX XXXX'
        form['card_ccv2'] = '000'
        form['card_exp_month'] = '1'
        form['card_exp_year'] = '1970'

        response = form.submit()
        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/checkout/')

        form = page.form

        form['email'] = 'john'
        form['card_ccv2'] = 'john'
        form['card_exp_year'] = 'john'

        response = form.submit()
        self.assertEquals('This field is required.', response.pyquery('#id_first_name_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_last_name_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_country_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_phone_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_city_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_post_code_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_address_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_additional_info_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_card_type_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_card_holder_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_card_number_container .errors').text())
        self.assertEquals('Enter a whole number.', response.pyquery('#id_card_ccv2_container .errors').text())
        self.assertEquals('Enter a whole number.', response.pyquery('#id_card_exp_year_container .errors').text())


urlpatterns = [
    url(r'^demo/checkout/$', generic.FormView.as_view(
        form_class=forms.CheckoutForm, success_url='/demo/checkout/', template_name="demo.html")),
]
