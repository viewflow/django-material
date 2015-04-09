import json

from django import forms
from django.core.validators import MaxLengthValidator
from django_webtest import WebTest
from . import build_test_urls


class TestForm(forms.Form):
    test_field = forms.CharField(validators=[MaxLengthValidator(20)])


class TestTextInput(WebTest):
    csrf_checks = False
    default_form = TestForm
    urls = 'tests.integration.tests.test_textinput_field'

    def test_default_usecase(self):
        page = self.app.get(self.test_default_usecase.url)

        self.assertIn('id="id_test_field_container"', page.body)

        form = page.form
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

    def test_render_with_value(self):
        form = self.app.get(self.test_missing_value_error_rendered.url).form
        form['test_field'] = 'a'*21
        response = form.submit()

        self.assertIn('value="{}"'.format('a'*21), response.body)
        self.assertIn('Ensure this value has at most 20 characters', response.body)


urlpatterns = build_test_urls(TestTextInput)
