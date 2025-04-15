from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from material.views.detail import DetailModelView


class ViewsetWithPermissions:
    """Viewset with permission methods for testing."""

    def has_view_permission(self, user, obj=None):
        return user.username == "allowed_user"

    def has_change_permission(self, user, obj=None):
        return user.username == "allowed_user"

    def get_queryset(self, request):
        return User.objects.all()

    def get_detail_page_actions(self, request, obj):
        return [{"label": "Test Action", "url": "/test-action/", "style": "text"}]

    def get_detail_page_object_actions(self, request, obj):
        return [{"label": "Object Action", "url": "/object-action/", "style": "filled"}]

    def get_change_url(self, request, pk):
        return f"/custom-change-url/{pk}/"


class DetailModelViewTests(TestCase):
    """Tests for the DetailModelView class."""

    def setUp(self):
        self.factory = RequestFactory()

        self.allowed_user = User.objects.create_user(username="allowed_user", password="password")
        self.denied_user = User.objects.create_user(username="denied_user", password="password")
        self.test_user = User.objects.create_user(username="test_user", password="password")

        # Set up the view with no viewset
        self.view = DetailModelView()
        self.view.model = User
        self.view.pk_url_kwarg = "pk"
        self.view.template_name_suffix = "_detail"

    def test_has_view_permission_with_viewset(self):
        """Test permission checking with viewset."""
        self.view.viewset = ViewsetWithPermissions()

        request = self.factory.get("/detail/1/")
        request.user = self.allowed_user
        self.assertTrue(self.view.has_view_permission(request.user))

        request.user = self.denied_user
        self.assertFalse(self.view.has_view_permission(request.user))

    def test_has_view_permission_without_viewset(self):
        """Test permission checking without viewset (fallback to object permissions)."""
        self.view.viewset = None

        # In a real scenario, Django's permission system would be used
        # This simplified test just verifies the method runs without errors
        request = self.factory.get("/detail/1/")
        request.user = self.allowed_user

        # The result depends on has_object_perm implementation
        # We're just ensuring it runs without error
        result = self.view.has_view_permission(request.user)
        self.assertIsInstance(result, bool)

    def test_get_object_data(self):
        """Test get_object_data method."""
        self.view.object = self.test_user
        data = self.view.get_object_data()

        # Convert to dict for easier testing
        data_dict = {field_name: field_value for field_name, field_value in data.items()}

        # Verify the data contains basic user fields
        self.assertIn("Username", data_dict)
        self.assertEqual(data_dict["Username"], "test_user")

    def test_get_page_actions_with_viewset(self):
        """Test get_page_actions with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        self.view.request = self.factory.get("/detail/1/")
        self.view.object = self.test_user

        actions = self.view.get_page_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["label"], "Test Action")
        self.assertEqual(actions[0]["url"], "/test-action/")
        self.assertEqual(actions[0]["style"], "text")

    def test_get_page_actions_with_class_actions(self):
        """Test get_page_actions with class actions."""
        self.view.viewset = None
        self.view.page_actions = [
            {"label": "Class Action", "url": "/class-action/", "style": "filled"}
        ]

        actions = self.view.get_page_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["label"], "Class Action")
        self.assertEqual(actions[0]["url"], "/class-action/")
        self.assertEqual(actions[0]["style"], "filled")

    def test_get_object_actions_with_viewset(self):
        """Test get_object_actions with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        self.view.request = self.factory.get("/detail/1/")
        self.view.object = self.test_user

        actions = self.view.get_object_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["label"], "Object Action")
        self.assertEqual(actions[0]["url"], "/object-action/")
        self.assertEqual(actions[0]["style"], "filled")

    def test_get_object_actions_with_class_actions(self):
        """Test get_object_actions with class actions."""
        self.view.viewset = None
        self.view.object_actions = [
            {"label": "Class Object Action", "url": "/class-object-action/", "style": "tonal"}
        ]

        actions = self.view.get_object_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["label"], "Class Object Action")
        self.assertEqual(actions[0]["url"], "/class-object-action/")
        self.assertEqual(actions[0]["style"], "tonal")

    def test_get_object_change_link_with_viewset(self):
        """Test get_object_change_link with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/detail/1/")
        request.user = self.allowed_user
        self.view.request = request
        self.view.object = self.test_user

        url = self.view.get_object_change_link
        self.assertEqual(url, f"/custom-change-url/{self.test_user.pk}/")

    def test_get_object_change_link_without_permission(self):
        """Test get_object_change_link without permission."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/detail/1/")
        request.user = self.denied_user
        self.view.request = request
        self.view.object = self.test_user

        url = self.view.get_object_change_link
        self.assertIsNone(url)

    def test_get_object_with_invalid_pk(self):
        """Test get_object with invalid pk."""
        self.view.kwargs = {"pk": "invalid"}

        with self.assertRaises(Http404):
            self.view.get_object()

    def test_get_template_names_with_template_name(self):
        """Test template names with template_name set."""
        self.view.template_name = "custom_template.html"
        templates = self.view.get_template_names()
        self.assertEqual(templates, ["custom_template.html"])

    def test_get_template_names_without_template_name(self):
        """Test template names without template_name set."""
        self.view.template_name = None

        templates = self.view.get_template_names()
        self.assertEqual(templates, ["auth/user_detail.html", "material/views/detail.html"])
