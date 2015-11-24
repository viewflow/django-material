from django import forms
from django.test.utils import override_settings
from django_webtest import WebTest
from material import Layout, Row, Column
from . import build_test_urls


class LayoutForm(forms.Form):
    test_field1 = forms.CharField()
    test_field2 = forms.CharField()
    test_field3 = forms.CharField()
    test_field4 = forms.CharField()
    test_field5 = forms.CharField()

    layout = Layout(Row('test_field1', 'test_field2'),
                    Row('test_field3', Column('test_field4', 'test_field5')))


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    default_form = LayoutForm

    def test_field_part_override(self):
        """
        Issue #19
        """
        response = self.app.get(self.test_field_part_override.url)
        self.assertIn('NO FIELD', response.content.decode('utf-8'))

    test_field_part_override.template = """
        {% form %}
             {% part form.test_field1 %}NO FIELD{% endpart %}
        {% endform %}
    """

urlpatterns = build_test_urls(Test)
