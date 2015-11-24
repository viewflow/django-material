import json

from django import forms
from django.test.utils import override_settings
from django_webtest import WebTest
from . import build_test_urls


class DecimalInputForm(forms.Form):
    test_field = forms.DecimalField(
        min_value=10,
        max_value=20,
        max_digits=5,
        decimal_places=3,
        widget=forms.NumberInput(attrs={'data-test': 'Test Attr'}))


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    default_form = DecimalInputForm

    def test_default_usecase(self):
        page = self.app.get(self.test_default_usecase.url)

        self.assertIn('id="id_test_field_container"', page.body.decode('utf-8'))
        self.assertIn('id="id_test_field"', page.body.decode('utf-8'))
        self.assertIn('max="20"', page.body.decode('utf-8'))
        self.assertIn('min="10"', page.body.decode('utf-8'))
        self.assertIn('step="0.001"', page.body.decode('utf-8'))
        self.assertIn('data-test="Test Attr"', page.body.decode('utf-8'))

        form = page.form
        self.assertIn('test_field', form.fields)

        form['test_field'] = 15
        response = json.loads(form.submit().body.decode('utf-8'))

        self.assertIn('cleaned_data', response)
        self.assertIn('test_field', response['cleaned_data'])
        self.assertEquals('15', response['cleaned_data']['test_field'])

    def test_invalid_value(self):
        form = self.app.get(self.test_invalid_value.url).form
        form['test_field'] = 0.12345
        response = form.submit()

        self.assertIn('value="0.12345"', response.body.decode('utf-8'))
        self.assertIn('Ensure that there are no more than 3 decimal places.', response.body.decode('utf-8'))


urlpatterns = build_test_urls(Test)
