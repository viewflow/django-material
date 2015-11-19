from django.conf.urls import url
from django.views import generic
from django.test.utils import override_settings
from django_webtest import WebTest
from .. import forms


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/comment/')

        form = page.form
        form['name'] = 'John Doe'
        form['email'] = 'john@doe.com'
        form['website'] = 'http://me.johndoe'
        form['comment'] = 'Test comment'

        response = form.submit()
        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/comment/')

        form = page.form
        form['email'] = 'john'
        form['website'] = '_no_way_'

        response = form.submit()
        self.assertEquals('This field is required.', response.pyquery('#id_name_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('Enter a valid URL.', response.pyquery('#id_website_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_comment_container .errors').text())


urlpatterns = [
    url(r'^demo/comment/$', generic.FormView.as_view(
        form_class=forms.CommentForm, success_url='/demo/comment/', template_name="demo.html")),
]
