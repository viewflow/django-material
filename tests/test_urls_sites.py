from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import NoReverseMatch, path, reverse
from django.views.generic import TemplateView

from material.urls import Viewset, route
from material.urls.sites import Application, AppMenuMixin, Site


class TestAppMenuMixin(AppMenuMixin, Viewset):
    """Test implementation of AppMenuMixin."""

    app_name = "test_menu"
    
    page_path = path("page/", TemplateView.as_view(template_name="material/base.html"), name="page")


class TestApplicationNoTitle(Application):
    """Test Application implementation with no title."""

    app_name = "app_no_title"

    page_path = path("page/", TemplateView.as_view(template_name="material/base.html"), name="page")


class TestApplication(Application):
    """Test Application implementation with title."""

    app_name = "app_with_title"
    title = "Test App"

    page_path = path("page/", TemplateView.as_view(template_name="material/base.html"), name="page")


class TestSiteNoTitle(Site):
    """Test Site implementation with no title."""

    app_name = "site_no_title"

    page_path = path("page/", TemplateView.as_view(template_name="material/base.html"), name="page")


class TestSite(Site):
    """Test Site implementation with title."""

    app_name = "site_with_title"
    title = "Test Site"

    page_path = path("page/", TemplateView.as_view(template_name="material/base.html"), name="page")
    app_path = route("app/", TestApplication())


class ModelWithUrl:
    """Simple model class for testing get_absolute_url functionality."""

    def __init__(self, pk=1):
        self.pk = pk


class ModelViewset(Viewset):
    """Test viewset with model for get_absolute_url testing."""

    model = ModelWithUrl

    def get_object_url(self, request, obj):
        return f"/model/{obj.pk}/"


# Root viewset for URL configuration
class RootViewset(Viewset):
    site_path = route("site/", TestSite())
    site_no_title_path = route("site-no-title/", TestSiteNoTitle())


urlconfig = RootViewset()
site_config = urlconfig.site_path.viewset

urlpatterns = [path("", urlconfig.urls)]


@override_settings(ROOT_URLCONF=__name__)
class SiteTests(TestCase):
    """Tests for Site class functionality."""

    def test_site_title(self):
        """Test site title is set correctly."""
        self.assertEqual(site_config.title, "Test Site")
        self.assertEqual(urlconfig.site_no_title_path.viewset.title, "Test site no title")

    def test_site_menu_items(self):
        """Test site menu_items returns applications."""
        menu_items = list(site_config.menu_items())
        self.assertEqual(len(menu_items), 1)
        self.assertIsInstance(menu_items[0], Application)

    def test_site_has_view_permission(self):
        """Test site permission check."""
        # Create a user for permission tests
        user = User.objects.create_user(username="testuser", password="password")

        # Default case should allow access
        self.assertTrue(site_config.has_view_permission(user))

        # Test with permission set
        site_with_perm = TestSite(permission="auth.view_user")
        self.assertFalse(site_with_perm.has_view_permission(user))

    def test_url_navigation(self):
        """Test navigating through site URLs."""
        # Test site root redirects to page
        response = self.client.get(reverse("site_with_title:index"))
        self.assertRedirects(response, "/site/page/")

        # Test site page
        response = self.client.get(reverse("site_with_title:page"))
        self.assertEqual(response.status_code, 200)

        # Test application redirect
        response = self.client.get(reverse("site_with_title:app_with_title:index"))
        self.assertRedirects(response, "/site/app/page/")


@override_settings(ROOT_URLCONF=__name__)
class ApplicationTests(TestCase):
    """Tests for Application class functionality."""

    def setUp(self):
        self.app = site_config.app_path.viewset

    def test_application_title(self):
        """Test application title is set correctly."""
        self.assertEqual(self.app.title, "Test App")

        # Create a new application with no title and test auto-generation
        app_no_title = TestApplicationNoTitle()
        self.assertEqual(app_no_title.title, "Test application no title")

    def test_application_menu_items(self):
        """Test application menu_items functionality."""
        # Create a mock app with menu items
        app = TestApplication()
        menu_mixin = TestAppMenuMixin()
        app.viewsets = [menu_mixin]
        app._children = [menu_mixin]

        menu_items = list(app.menu_items())
        self.assertEqual(len(menu_items), 1)
        self.assertIsInstance(menu_items[0], AppMenuMixin)

    def test_application_has_view_permission(self):
        """Test application permission check."""
        # Create a user for permission tests
        user = User.objects.create_user(username="testuser", password="password")

        # Default case should allow access
        self.assertTrue(self.app.has_view_permission(user))

        # Test with permission set
        app_with_perm = TestApplication(permission="auth.view_user")
        self.assertFalse(app_with_perm.has_view_permission(user))

        # Test with callable permission
        app_with_callable_perm = TestApplication(permission=lambda user: False)
        self.assertFalse(app_with_callable_perm.has_view_permission(user))


@override_settings(ROOT_URLCONF=__name__)
class AppMenuMixinTests(TestCase):
    """Tests for AppMenuMixin class functionality."""

    def test_title_generation(self):
        """Test title is generated correctly from class name."""
        mixin = TestAppMenuMixin()
        self.assertEqual(mixin.title, "Test app menu mixins")

    def test_has_view_permission(self):
        """Test default permission behavior."""
        mixin = TestAppMenuMixin()
        self.assertTrue(mixin.has_view_permission(None))


@override_settings(ROOT_URLCONF=__name__)
class SiteModelUrlTests(TestCase):
    """Tests for Site get_absolute_url functionality."""

    def setUp(self):
        """Setup test site with model viewset."""
        self.site = TestSite()
        self.model_viewset = ModelViewset()
        self.site.viewsets = [self.model_viewset]
        self.site._children = [self.model_viewset]

    def test_get_absolute_url(self):
        """Test getting absolute URL for a model object."""
        model = ModelWithUrl(pk=42)
        url = self.site.get_absolute_url(None, model)
        self.assertEqual(url, "/model/42/")

    def test_get_absolute_url_no_viewset(self):
        """Test exception when no viewset for model exists."""

        class UnknownModel:
            pass

        with self.assertRaises(NoReverseMatch):
            self.site.get_absolute_url(None, UnknownModel())
