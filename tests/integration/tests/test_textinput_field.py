import json

from django import forms
from django_webtest import WebTest
from . import build_test_urls


class TestForm(forms.Form):
    test_field = forms.CharField()


class TestTextInput(WebTest):
    csrf_checks = False
    default_form = TestForm
    urls = 'tests.integration.tests.test_textinput_field'

    def test_default_usecase(self):
        form = self.app.get(self.test_default_usecase.url).form
        self.assertIn('test_field', form.fields)
        form['test_field'] = 'TEST CONTENT'
        response = json.loads(form.submit().body.decode('utf-8'))

        self.assertIn('cleaned_data', response)
        self.assertIn('test_field', response['cleaned_data'])
        self.assertEquals('TEST CONTENT', response['cleaned_data']['test_field'])

    def test_missing_value_error_rendered(self):
        form = self.app.get(self.test_missing_value_error_rendered.url).form
        response = form.submit()
        self.assertIn('This field is required.', response.body.decode('utf-8'))

    def test_prefix_rendered(self):
        response = self.app.get(self.test_prefix_rendered.url)
        self.assertIn('<i class="mdi-communication-email prefix"></i>', response.body.decode('utf-8'))

    test_prefix_rendered.template = '''
        {% form %}
             {% part form.test_field prefix %}<i class="mdi-communication-email prefix"></i>{% endpart %}
        {% endform %}
    '''

urlpatterns = build_test_urls(TestTextInput)
