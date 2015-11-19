from django.conf.urls import url
from django.views import generic
from django.test.utils import override_settings
from django_webtest import WebTest
from .. import forms


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/registration/')

        form = page.form
        form['username'] = 'admin'
        form['email'] = 'admin@admin.com'
        form['password'] = 'admin'
        form['password_confirm'] = 'admin'
        form['first_name'] = 'Super'
        form['last_name'] = 'Admin'
        form['gender'] = 'M'
        form['receive_news'] = 1
        form['agree_toc'] = 1

        response = form.submit()

        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/registration/')

        form = page.form
        form['email'] = 'admin'

        response = form.submit()

        self.assertEquals('This field is required.', response.pyquery('#id_username_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_password_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_password_confirm_container .errors').text())


urlpatterns = [
    url(r'^demo/registration/$', generic.FormView.as_view(
        form_class=forms.RegistrationForm, success_url='/demo/registration/', template_name="demo.html")),
]
