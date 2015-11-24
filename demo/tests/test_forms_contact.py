from django.conf.urls import url
from django.views import generic
from django.test.utils import override_settings
from django_webtest import WebTest
from .. import forms


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/contact/')

        form = page.form
        form['name'] = 'admin'
        form['email'] = 'admin@admin.com'
        form['subject'] = 'Test Message'
        form['message'] = 'Message body'
        form['send_copy'] = 1

        response = form.submit()

        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/contact/')

        form = page.form
        form['email'] = 'admin'

        response = form.submit()

        self.assertEquals('This field is required.', response.pyquery('#id_name_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_subject_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_subject_container .errors').text())


urlpatterns = [
    url(r'^demo/contact/$', generic.FormView.as_view(
        form_class=forms.ContactForm, success_url='/demo/contact/', template_name="demo.html")),
]
