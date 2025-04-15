from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from material.views.delete import DeleteModelView


class ViewsetWithPermissions:
    """Viewset with permission methods for testing."""

    def has_delete_permission(self, user, obj=None):
        return user.username == "allowed_user"

    def get_queryset(self, request):
        return User.objects.all()

    def get_success_url(self, request):
        return "/custom-success-url/"


class DeleteModelViewTests(TestCase):
    """Tests for the DeleteModelView class."""

    def setUp(self):
        self.factory = RequestFactory()

        self.allowed_user = User.objects.create_user(username="allowed_user", password="password")
        self.denied_user = User.objects.create_user(username="denied_user", password="password")
        self.test_user = User.objects.create_user(username="test_user", password="password")

        # Set up the view with no viewset
        self.view = DeleteModelView()
        self.view.model = User
        self.view.pk_url_kwarg = "pk"
        self.view.template_name_suffix = "_delete"

    def test_has_delete_permission_with_viewset(self):
        """Test permission checking with viewset."""
        self.view.viewset = ViewsetWithPermissions()

        request = self.factory.get("/delete/1/")
        request.user = self.allowed_user
        self.assertTrue(self.view.has_delete_permission(request))

        request.user = self.denied_user
        self.assertFalse(self.view.has_delete_permission(request))

    def test_has_delete_permission_without_viewset(self):
        """Test permission checking without viewset (fallback to object permissions)."""
        self.view.viewset = None

        # In a real scenario, Django's permission system would be used
        # This simplified test just verifies the method runs without errors
        request = self.factory.get("/delete/1/")
        request.user = self.allowed_user

        # The result depends on has_object_perm implementation
        # We're just ensuring it runs without error
        result = self.view.has_delete_permission(request)
        self.assertIsInstance(result, bool)

    def test_queryset_with_viewset(self):
        """Test queryset retrieval with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/delete/1/")
        self.view.request = request

        queryset = self.view.queryset
        self.assertIsNotNone(queryset)

    def test_queryset_without_viewset(self):
        """Test queryset retrieval without viewset."""
        self.view.viewset = None
        queryset = self.view.queryset
        self.assertIsNone(queryset)

    def test_get_template_names_with_template_name(self):
        """Test template names with template_name set."""
        self.view.template_name = "custom_template.html"
        templates = self.view.get_template_names()
        self.assertEqual(templates, ["custom_template.html"])

    def test_get_template_names_without_template_name(self):
        """Test template names without template_name set."""
        self.view.template_name = None

        templates = self.view.get_template_names()
        self.assertEqual(templates, ["auth/user_delete.html", "material/views/confirm_delete.html"])

    def test_get_success_url_with_viewset(self):
        """Test get_success_url with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        self.view.request = self.factory.get("/delete/1/")

        url = self.view.get_success_url()
        self.assertEqual(url, "/custom-success-url/")

    def test_get_success_url_without_viewset(self):
        """Test get_success_url without viewset."""
        self.view.viewset = None

        url = self.view.get_success_url()
        self.assertEqual(url, "../")
