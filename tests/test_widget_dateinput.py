import json

from django import forms
from django.test.utils import override_settings
from django_webtest import WebTest
from . import build_test_urls


class DateInputForm(forms.Form):
    test_field = forms.DateField(
        widget=forms.DateInput(attrs={'data-test': 'Test Attr'}))
    data_field = forms.BooleanField(required=False, widget=forms.HiddenInput, initial=True,
                                    help_text='To produce non empty POST for empty test_field')


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    default_form = DateInputForm

    def test_default_usecase(self):
        page = self.app.get(self.test_default_usecase.url)

        body = page.pyquery('#id_test_field_container').outerHtml()
        self.assertIn('id="id_test_field_container"', body)
        self.assertIn('id="id_test_field"', body)
        self.assertIn('data-test="Test Attr"', body)

        form = page.form
        self.assertIn('test_field', form.fields)

        form['test_field'] = '2012-01-01'
        response = json.loads(form.submit().body.decode('utf-8'))

        self.assertIn('cleaned_data', response)
        self.assertIn('test_field', response['cleaned_data'])
        self.assertEquals('2012-01-01', response['cleaned_data']['test_field'])

    def test_invalid_value(self):
        form = self.app.get(self.test_invalid_value.url).form
        response = form.submit()
        form['data_field'] = 1
        response = form.submit()

        self.assertIn('This field is required.', response.body.decode('utf-8'))

    def test_part_group_class(self):
        page = self.app.get(self.test_part_group_class.url)

        self.assertIn('class="yellow required checkbox-field col s12"', page.body.decode('utf-8'))

    test_part_group_class.template = '''
        {% form %}
             {% attr form.test_field 'group' class override %}yellow required checkbox-field col s12{% endattr %}
        {% endform %}
    '''

    def test_part_add_group_class(self):
        page = self.app.get(self.test_part_add_group_class.url)

        self.assertIn('class="input-field col s12 required deep-purple lighten-5"',
                      page.pyquery('#id_test_field_container').outerHtml())

    test_part_add_group_class.template = '''
        {% form %}
             {% attr form.test_field 'group' class append %}deep-purple lighten-5{% endattr %}
        {% endform %}
    '''

    def test_part_prefix(self):
        response = self.app.get(self.test_part_prefix.url)
        self.assertIn('<i class="mdi-communication-email prefix"></i>', response.body.decode('utf-8'))

    test_part_prefix.template = '''
        {% form %}
             {% part form.test_field prefix %}<i class="mdi-communication-email prefix"></i>{% endpart %}
        {% endform %}
    '''

    def test_part_add_control_class(self):
        response = self.app.get(self.test_part_add_control_class.url)
        self.assertIn('class="orange"', response.body.decode('utf-8'))

    test_part_add_control_class.template = '''
        {% form %}
             {% attr form.test_field 'widget' class append %}orange{% endattr %}
        {% endform %}
    '''

    def test_part_label(self):
        response = self.app.get(self.test_part_label.url)
        self.assertIn('<label for="id_test_field">My label</label>', response.body.decode('utf-8'))

    test_part_label.template = '''
        {% form %}
             {% part form.test_field label %}<label for="id_test_field">My label</label>{% endpart %}
        {% endform %}
    '''

    def test_part_add_label_class(self):
        response = self.app.get(self.test_part_add_label_class.url)
        self.assertIn('class="green-text"', response.body.decode('utf-8'))

    test_part_add_label_class.template = '''
        {% form %}
             {% attr form.test_field 'label' class append %}green-text{% endattr %}
        {% endform %}
    '''

    def test_part_help_text(self):
        response = self.app.get(self.test_part_help_text.url)
        self.assertIn('<small class="help-block">My help</small>', response.body.decode('utf-8'))

    test_part_help_text.template = '''
        {% form %}
             {% part form.test_field help_text %}<small class="help-block">My help</small>{% endpart %}
        {% endform %}
    '''

    def test_part_errors(self):
        response = self.app.get(self.test_part_errors.url)
        self.assertIn('<div class="errors"><small class="error">My Error</small></div>', response.body.decode('utf-8'))

    test_part_errors.template = '''
        {% form %}
             {% part form.test_field  errors%}<div class="errors"><small class="error">My Error</small></div>{% endpart %}
        {% endform %}
    '''


urlpatterns = build_test_urls(Test)
