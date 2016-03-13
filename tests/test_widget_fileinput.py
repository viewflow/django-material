import json

from django import forms
from django.test.utils import override_settings
from django_webtest import WebTest
from . import build_test_urls


class FileInputForm(forms.Form):
    test_field = forms.FileField()
    data_field = forms.BooleanField(required=False, widget=forms.HiddenInput,
                                    help_text='To produce non empty POST for empty test_field')


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    default_form = FileInputForm

    def test_default_usecase(self):
        page = self.app.get(self.test_default_usecase.url)

        self.assertIn('id="id_test_field_container"', page.body.decode('utf-8'))
        self.assertIn('id="id_test_field"', page.body.decode('utf-8'))

        form = page.form
        self.assertIn('test_field', form.fields)

        response = form.submit(upload_files=[('test_field', __file__)])
        response = json.loads(response.body.decode('utf-8'))

        self.assertIn('cleaned_data', response)
        self.assertIn('test_field', response['cleaned_data'])
        self.assertEquals('InMemoryUploadedFile', response['cleaned_data']['test_field'])

    def test_invalid_value(self):
        form = self.app.get(self.test_invalid_value.url).form
        form['data_field'] = '1'
        response = form.submit()
        self.assertIn('This field is required.', response.body.decode('utf-8'))

    def test_part_group_class(self):
        page = self.app.get(self.test_part_group_class.url)

        self.assertIn('class="yellow required input-field file-field col s12"', page.body.decode('utf-8'))

    test_part_group_class.template = '''
        {% form %}
             {% attr form.test_field 'group' class override %}yellow required input-field file-field col s12{% endattr %}
        {% endform %}
    '''

    def test_part_add_group_class(self):
        page = self.app.get(self.test_part_add_group_class.url)

        self.assertIn('class="input-field file-field col s12 required deep-purple lighten-5"', page.body.decode('utf-8'))

    test_part_add_group_class.template = '''
        {% form %}
             {% attr form.test_field 'group' class append %}deep-purple lighten-5{% endattr %}
        {% endform %}
    '''

    def test_part_prefix(self):
        response = self.app.get(self.test_part_prefix.url)
        self.assertIn('<span>DATA</span>', response.body.decode('utf-8'))

    test_part_prefix.template = '''
        {% form %}
             {% part form.test_field prefix %}<span>DATA</span>{% endpart %}
        {% endform %}
    '''

    def test_part_add_control_class(self):
        response = self.app.get(self.test_part_add_control_class.url)
        self.assertIn('class="file-path orange"', response.body.decode('utf-8'))

    test_part_add_control_class.template = '''
        {% form %}
             {% attr form.test_field 'widget' class append %}orange{% endattr %}
        {% endform %}
    '''

    def _test_part_label(self):  # TODO Label for file inputs
        response = self.app.get(self.test_part_label.url)
        self.assertIn('<label for="id_test_field">My label</label>', response.body.decode('utf-8'))

    _test_part_label.template = '''
        {% form %}
             {% part form.test_field label %}<label for="id_test_field">My label</label>{% endpart %}
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
