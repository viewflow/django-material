import json

from django import forms
from django.test.utils import override_settings
from django_webtest import WebTest
from . import build_test_urls

try:
    from django.forms.widgets import SelectDateWidget
except ImportError:
    # django 1.8
    from django.forms.extras import SelectDateWidget


class SelectForm(forms.Form):
    test_field = forms.DateField(
        widget=SelectDateWidget)
    data_field = forms.BooleanField(required=False, widget=forms.HiddenInput, initial=True,
                                    help_text='To produce non empty POST for empty test_field')


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    default_form = SelectForm

    def test_default_usecase(self):
        page = self.app.get(self.test_default_usecase.url)

        self.assertIn('id="id_test_field_container"', page.body.decode('utf-8'))
        self.assertIn('id="id_test_field_year"', page.body.decode('utf-8'))
        self.assertIn('id="id_test_field_month"', page.body.decode('utf-8'))
        self.assertIn('id="id_test_field_day"', page.body.decode('utf-8'))
        # self.assertIn('data-test="Test Attr"', page.body.decode('utf-8'))

        form = page.form
        self.assertIn('test_field_year', form.fields)
        self.assertIn('test_field_month', form.fields)
        self.assertIn('test_field_day', form.fields)

        form['test_field_year'] = '2021'
        form['test_field_month'] = '1'
        form['test_field_day'] = '13'
        response = json.loads(form.submit().body.decode('utf-8'))

        self.assertIn('cleaned_data', response)
        self.assertIn('test_field', response['cleaned_data'])
        self.assertEqual('2021-01-13', response['cleaned_data']['test_field'])


urlpatterns = build_test_urls(Test)
