import inspect
from datetime import date
from decimal import Decimal
from django.conf.urls import url
from django.http import JsonResponse, HttpResponse
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import six


DEFAULT_TEMPLATE = """
{% form %}{% endform %}
"""


class PythonObjectEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if (isinstance(obj, (date, list, dict, str, int, float, bool, type(None), Decimal)) or
                isinstance(obj, six.string_types)):
            return DjangoJSONEncoder.default(self, obj)
        return '{}'.format(type(obj).__name__)


@csrf_exempt
def test_view(request, form_cls, template_content):
    form = form_cls(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        return JsonResponse({'cleaned_data': form.cleaned_data}, encoder=PythonObjectEncoder)
    else:
        context = Context({'form': form})

        template = Template('''
            {{% load static material_form %}}
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Material Design for Django Forms and Admin</title>
                {{% include 'material/includes/material_css.html' %}}
            </head>
            <body>
                <div class="container expand-on-small-only" style="width:500px">
                    <form method="POST" enctype="multipart/form-data">
                        {}
                        <button class="" type="submit">Submit</button>
                    </form>
                </div>
                <script src="{{% static 'material/admin/js/jquery-2.1.4.min.js' %}}" type="text/javascript"></script>
                {{% include 'material/includes/material_js.html' %}}
            </body>
            </html>
            '''.format(template_content))
        return HttpResponse(template.render(context))


def build_test_urls(testcase_cls):
    urls = []

    tests = inspect.getmembers(
        testcase_cls,
        lambda member: callable(member) and member.__name__.startswith('test_'))

    for name, test in tests:
        if hasattr(test, 'url'):
            url_path = test.url
        else:
            url_path = r'^test/{}/$'.format(name[5:])
            if hasattr(test, 'im_func'):
                test.im_func.url = '/test/{}/'.format(name[5:])
            else:
                test.url = '/test/{}/'.format(name[5:])

        if hasattr(test, 'template'):
            template_content = test.template
        else:
            template_content = DEFAULT_TEMPLATE
            if hasattr(test, 'im_func'):
                test.im_func.template = template_content
            else:
                test.template = template_content

        if hasattr(test, 'form'):
            form_cls = test.form
        else:
            form_cls = testcase_cls.default_form
            if hasattr(test, 'im_func'):
                test.im_func.form_cls = form_cls
            else:
                test.form_cls = form_cls

        urls.append(url(url_path, test_view, {
            'template_content': template_content,
            'form_cls': form_cls
        }))

    return urls
