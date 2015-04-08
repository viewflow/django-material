import inspect
from django.conf.urls import url
from django.http import JsonResponse, HttpResponse
from django.template import Context, Template

DEFAULT_TEMPLATE = """
{% form %}{% endform %}
"""


def test_view(request, form_cls, template_content):
    form = form_cls(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        return JsonResponse({'cleaned_data': form.cleaned_data})
    else:
        context = Context({'form': form})

        template = Template(
            '{{% load material_form %}}<form method="POST">{{% csrf_token %}}{}</form>'
            .format(template_content))
        return HttpResponse(template.render(context))


def build_test_urls(testcase_cls):
    urls = []
    tests = inspect.getmembers(
        testcase_cls,
        lambda member: inspect.ismethod(member) and member.__name__.startswith('test_'))

    for name, test in tests:
        if hasattr(test, 'url'):
            url_path = test.url
        else:
            url_path = r'^test/{}/$'.format(name[5:])
            test.im_func.url = '/test/{}/'.format(name[5:])

        if hasattr(test, 'template'):
            template_content = test.template
        else:
            template_content = DEFAULT_TEMPLATE
            test.im_func.template = template_content

        if hasattr(test, 'form'):
            form_cls = test.form
        else:
            form_cls = testcase_cls.default_form
            test.im_func.form = form_cls

        urls.append(url(url_path, test_view, {
            'template_content': template_content,
            'form_cls': form_cls
        }))

    return urls
