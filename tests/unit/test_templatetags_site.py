from django.template import Template, Context
from django.test import TestCase, override_settings
from django.urls import path
from django.views import generic
from material import Viewset


class ProbeViewset(Viewset):
    probe_url = path(
        'probe/', generic.TemplateView.as_view(), name="probe"
    )


@override_settings(ROOT_URLCONF=__name__)
class Test(TestCase):
    def test_reverse_viewset_url(self):
        template = Template(
            "{% load material_site %}{% viewset_url viewset 'probe' %}"
        )
        result = template.render(Context({'viewset': probe_viewset}))
        self.assertEqual('/viewset/probe/', result)

    def test_reverse_viewset_url_as_variable(self):
        template = Template(
            "{% load material_site %}{% viewset_url viewset 'probe' as var %}{{ var }}"
        )
        result = template.render(Context({'viewset': probe_viewset}))
        self.assertEqual('/viewset/probe/', result)

    def test_reverse_unknown_url_as_variable(self):
        template = Template(
            "{% load material_site %}{% viewset_url viewset 'unknown' as var %}{{ var|default:'NONE' }}"
        )
        result = template.render(Context({'viewset': probe_viewset}))
        self.assertEqual('NONE', result)


probe_viewset = ProbeViewset(app_name='test')

urlpatterns = [
    path('viewset/', probe_viewset.urls)
]
