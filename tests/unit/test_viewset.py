from django.urls import path, reverse
from django.views import generic
from django.test import TestCase, override_settings
from material.viewset import (
    Viewset, IndexViewMixin, NamedViewsetMixin,
    _get_viewset_index_redirect_url
)


class ProbeSubViewset(Viewset):
    sub_url = path(
        '', generic.TemplateView.as_view(), name="index"
    )


class ProbeViewset(NamedViewsetMixin, IndexViewMixin, Viewset):
    probe_url = path(
        'probe/', generic.TemplateView.as_view(), name="probe"
    )
    probe_viewset = ProbeSubViewset(prefix="sub")


@override_settings(ROOT_URLCONF=__name__)
class Test(TestCase):
    def test_viewset_named(self):
        self.assertEqual('probe', ProbeViewset().app_name)

    def test_child_viewset_mount(self):
        parent_viewset = ProbeViewset()
        child_viewset = parent_viewset.probe_viewset

        # trigger child viewset mount
        self.assertTrue(parent_viewset.urls)

        self.assertEqual(parent_viewset, child_viewset._parent)
        self.assertEqual('probe', child_viewset.app_name)
        self.assertEqual('probe', child_viewset.namespace)

    def test_index_url(self):
        index_url = _get_viewset_index_redirect_url(ProbeViewset())
        self.assertEqual('./probe/', index_url)

    def test_resolve_index_view(self):
        self.assertEqual('/', reverse('probe:index'))

    def test_resolve_view(self):
        self.assertEqual('/probe/', reverse('probe:probe'))

    def test_resolve_subview(self):
        self.assertEqual('/sub/', reverse('probe:probe:index'))

    def test_reverse_child_viewset_url(self):
        parent_viewset = ProbeViewset()

        # Trigger child viewset mount
        self.assertTrue(parent_viewset.urls)

        sub_index_url = parent_viewset.probe_viewset.reverse('index')
        self.assertEqual('/sub/', sub_index_url)


urlpatterns = [
    path('', ProbeViewset().urls)
]
