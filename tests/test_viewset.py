from django.urls import path
from django.views import generic
from django.test import TestCase
from material.viewset import Viewset, _get_viewset_index_url


class Test(TestCase):
    def test_viewset_index_url(self):
        class SampleViewset(Viewset):
            first_view = path(
                '/first/<int:pk>/', generic.TemplateView.as_view()
            )

            third_view = path(
                '/third/', generic.TemplateView.as_view()
            )

            second_view = path(
                '/second/', generic.TemplateView.as_view()
            )

        index_url = _get_viewset_index_url(SampleViewset())
        self.assertEqual('/third/', index_url)
