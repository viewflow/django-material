from django.conf.urls import url
from django.views import generic
from django.test.utils import override_settings
from django_webtest import WebTest
from .. import forms


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/order/')

        form = page.form
        form['name'] = 'John Doe'
        form['company'] = 'Viewflow'
        form['email'] = 'john@viewflow.io'
        form['phone'] = '5-555-4200-11'
        form['interest'] = 'D'
        form['budget'] = 'S'
        form['start_date'] = '2015-06-01'
        form['finish_date'] = '2030-06-01'
        form['message'] = 'Test Message'

        response = form.submit(upload_files=[('attachment', __file__)])

        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/order/')

        form = page.form
        form['email'] = 'john'
        form['start_date'] = 'XXX'
        form['finish_date'] = 'XXX'

        response = form.submit()
        self.assertEquals('This field is required.', response.pyquery('#id_name_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_company_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_phone_container .errors').text())
        self.assertEquals('Enter a valid date.', response.pyquery('#id_start_date_container .errors').text())
        self.assertEquals('Enter a valid date.', response.pyquery('#id_finish_date_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_message_container .errors').text())


urlpatterns = [
    url(r'^demo/order/$', generic.FormView.as_view(
        form_class=forms.OrderForm, success_url='/demo/order/', template_name="demo.html")),
]
