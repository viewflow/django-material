import json

from django import forms
from django.conf.urls import url
from django.http import JsonResponse, HttpResponse
from django.template import Context, Template
from django_webtest import WebTest


class TestForm(forms.Form):
    test_field = forms.CharField()


def test_view(request, form_cls=TestForm, template_content='{% form %}{% endform %}'):
    form = form_cls(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        return JsonResponse({'cleaned_data': form.cleaned_data})
    else:
        context = Context({'form': form})

        template = Template(
            '{{% load material_form %}}<form method="POST">{{% csrf_token %}}{}</form>'
            .format(template_content))
        return HttpResponse(template.render(context))


class TestSubmitSucceed(WebTest):
    csrf_checks = False
    urls = 'tests.integration.tests.test_textinput_field'

    def test_submit_valid_data_succeed(self):
        form = self.app.get('/test/submit/').form
        self.assertIn('test_field', form.fields)
        form['test_field'] = 'TEST CONTENT'
        response = json.loads(form.submit().body)

        self.assertIn('cleaned_data', response)
        self.assertIn('test_field', response['cleaned_data'])
        self.assertEquals('TEST CONTENT', response['cleaned_data']['test_field'])

    def test_missing_value_error_rendered(self):
        form = self.app.get('/test/missing/').form
        response = form.submit()
        self.assertIn('This field is required.', response.body)

    def test_prefix_rendered(self):
        response = self.app.get('/test/prefix/')
        self.assertIn('PREFIX', response.body)

    test_prefix_rendered.template = '''
        {% form %}
             {% part form.test_field prefix %}PREFIX{% endpart %}
        {% endform %}
    '''


urlpatterns = [
    url(r'^test/submit/$', test_view),
    url(r'^test/missing/$', test_view),
    url(r'^test/prefix/$', test_view, {'template_content': TestSubmitSucceed.test_prefix_rendered.template}),
]
