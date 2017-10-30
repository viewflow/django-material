from django.urls import path
from django.views import generic
from django.test import TestCase, override_settings
from material import Site, Application


class ProbeApplication(Application):
    index_view = path(
        '',
        generic.TemplateView.as_view(
            template_name='material/base.html')
    )


probe_site = Site(apps=[
    ProbeApplication()
])


@override_settings(ROOT_URLCONF=__name__)
class Test(TestCase):
    def test_site_match_injected(self):
        response = self.client.get('/probe/')
        match = response.wsgi_request.resolver_match

        self.assertTrue(hasattr(match, 'site'))
        self.assertEqual(match.site, probe_site)

        self.assertTrue(hasattr(match, 'app'))
        self.assertEqual(type(match.app), ProbeApplication)


urlpatterns = [
    path('', probe_site.urls)
]
