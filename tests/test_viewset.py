from django.urls import path, reverse
from django.views import generic
from django.test import TestCase, override_settings
from material.viewset import (
    Viewset, IndexViewMixin, NamedViewsetMixin,
    _get_viewset_index_url
)


class ProbeSubViewset(Viewset):
    sub_view = path(
        '', generic.TemplateView.as_view(), name="index"
    )


class ProbeViewset(NamedViewsetMixin, IndexViewMixin, Viewset):
    prove_view = path(
        'probe/', generic.TemplateView.as_view(), name="probe"
    )
    probe_viewset = ProbeSubViewset(prefix="sub")


@override_settings(ROOT_URLCONF=__name__)
class Test(TestCase):
    def test_viewset_named(self):
        self.assertEqual('probe', ProbeViewset().app_name)

    def test_index_url(self):
        index_url = _get_viewset_index_url(ProbeViewset())
        self.assertEqual('./probe/', index_url)

    def test_resolve_index_view(self):
        self.assertEqual('/', reverse('probe:index'))

    def test_resolve_view(self):
        self.assertEqual('/probe/', reverse('probe:probe'))

    def test_resolve_subview(self):
        self.assertEqual('/sub/', reverse('probe:probe:index'))


urlpatterns = [
    path('', ProbeViewset().urls)
]
