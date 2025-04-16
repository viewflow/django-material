from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import Form, ModelForm, Widget
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from material.views.update import UpdateModelView


class ViewsetWithPermissions:
    """Viewset with permission methods for testing."""

    def has_change_permission(self, user, obj=None):
        return user.username == "allowed_user"

    def get_queryset(self, request):
        return User.objects.all()

    def get_success_url(self, request, obj=None):
        return "/custom-success-url/"

    def get_object_url(self, request, obj):
        return f"/custom-object-url/{obj.pk}/"

    def get_form_class(self, request):
        return CustomModelForm

    def get_form_widgets(self, request):
        return {"username": CustomWidget}

    def get_update_form_class(self, request):
        return SpecialUpdateForm

    def get_update_form_widgets(self, request):
        return {"username": SpecialUpdateWidget}

    def get_update_page_actions(self, request, obj):
        return [{"label": "Special Action", "url": f"/special-action/{obj.pk}/", "style": "filled"}]


class CustomModelForm(ModelForm):
    """Custom model form for testing."""

    class Meta:
        model = User
        fields = ["username", "email"]


class SpecialUpdateForm(ModelForm):
    """Special update form for testing."""

    class Meta:
        model = User
        fields = ["username", "email", "first_name"]


class CustomWidget(Widget):
    """Custom widget for testing."""

    pass


class SpecialUpdateWidget(Widget):
    """Special update widget for testing."""

    pass


class UpdateModelViewTests(TestCase):
    """Tests for the UpdateModelView class."""

    def setUp(self):
        self.factory = RequestFactory()
        self.allowed_user = User.objects.create_user(username="allowed_user", password="password")
        self.denied_user = User.objects.create_user(username="denied_user", password="password")
        self.test_user = User.objects.create_user(username="test_user", password="password")

        # Set up the view with no viewset
        self.view = UpdateModelView()
        self.view.model = User
        self.view.pk_url_kwarg = "pk"
        self.view.template_name_suffix = "_update"
        self.view.fields = ["username", "email"]
        self.view.kwargs = {"pk": self.test_user.pk}

    def test_has_change_permission_with_viewset(self):
        """Test permission checking with viewset."""
        self.view.viewset = ViewsetWithPermissions()

        request = self.factory.get(f"/update/{self.test_user.pk}/")
        request.user = self.allowed_user
        self.assertTrue(self.view.has_change_permission(request, self.test_user))

        request.user = self.denied_user
        self.assertFalse(self.view.has_change_permission(request, self.test_user))

    def test_has_change_permission_without_viewset(self):
        """Test permission checking without viewset (fallback to object permissions)."""
        self.view.viewset = None

        # In a real scenario, Django's permission system would be used
        # This simplified test just verifies the method runs without errors
        request = self.factory.get(f"/update/{self.test_user.pk}/")
        request.user = self.allowed_user

        # The result depends on has_object_perm implementation
        # We're just ensuring it runs without error
        result = self.view.has_change_permission(request, self.test_user)
        self.assertIsInstance(result, bool)

    def test_get_object_url_with_viewset(self):
        """Test get_object_url with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get(f"/update/{self.test_user.pk}/")
        self.view.request = request

        url = self.view.get_object_url(self.test_user)
        self.assertEqual(url, f"/custom-object-url/{self.test_user.pk}/")

    def test_get_object_url_with_absolute_url(self):
        """Test get_object_url with get_absolute_url method."""
        # For this test, we need to mock has_change_permission to return True
        from material.views import update

        original_has_perm = UpdateModelView.has_change_permission

        try:
            # Override the method to always return True
            UpdateModelView.has_change_permission = lambda self, request, obj=None: True

            self.view.viewset = None
            request = self.factory.get(f"/update/{self.test_user.pk}/")
            self.view.request = request

            # Mock get_absolute_url
            self.test_user.get_absolute_url = lambda: f"/users/{self.test_user.pk}/"

            url = self.view.get_object_url(self.test_user)
            self.assertEqual(url, f"/users/{self.test_user.pk}/")
        finally:
            # Restore the original method
            UpdateModelView.has_change_permission = original_has_perm

    def test_get_page_actions_with_viewset(self):
        """Test get_page_actions with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get(f"/update/{self.test_user.pk}/")
        self.view.request = request
        self.view.object = self.test_user

        actions = self.view.get_page_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["label"], "Special Action")
        self.assertEqual(actions[0]["url"], f"/special-action/{self.test_user.pk}/")
        self.assertEqual(actions[0]["style"], "filled")

    def test_get_page_actions_with_page_actions(self):
        """Test get_page_actions with page_actions attribute."""
        self.view.viewset = None
        self.view.page_actions = [
            {"label": "Default Action", "url": "/default-action/", "style": "text"}
        ]
        self.view.object = self.test_user

        actions = self.view.get_page_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["label"], "Default Action")
        self.assertEqual(actions[0]["url"], "/default-action/")
        self.assertEqual(actions[0]["style"], "text")

    def test_queryset_with_viewset(self):
        """Test queryset retrieval with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get(f"/update/{self.test_user.pk}/")
        self.view.request = request

        queryset = self.view.queryset
        self.assertIsNotNone(queryset)

    def test_queryset_without_viewset(self):
        """Test queryset retrieval without viewset."""
        self.view.viewset = None
        queryset = self.view.queryset
        self.assertIsNone(queryset)

    def test_get_form_widgets_with_form_widgets(self):
        """Test get_form_widgets with form_widgets attribute."""
        widgets = {"username": CustomWidget}
        self.view.form_widgets = widgets
        self.assertEqual(self.view.get_form_widgets(), widgets)

    def test_get_form_widgets_with_viewset_update_form_widgets(self):
        """Test get_form_widgets with viewset get_update_form_widgets."""
        # Make a copy of the class to avoid modifying the original for other tests
        import copy

        viewset_class = copy.copy(ViewsetWithPermissions)

        # Ensure the method returns what we expect
        viewset_class.get_update_form_widgets = lambda self, request: {
            "username": SpecialUpdateWidget
        }

        self.view.viewset = viewset_class()
        request = self.factory.get(f"/update/{self.test_user.pk}/")
        self.view.request = request
        widgets = self.view.get_form_widgets()
        self.assertEqual(widgets, {"username": SpecialUpdateWidget})

    def test_get_form_widgets_with_viewset_form_widgets(self):
        """Test get_form_widgets with viewset get_form_widgets."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get(f"/update/{self.test_user.pk}/")
        self.view.request = request
        # Remove get_update_form_widgets to test fallback
        delattr(ViewsetWithPermissions, "get_update_form_widgets")
        widgets = self.view.get_form_widgets()
        self.assertEqual(widgets, {"username": CustomWidget})

    def test_get_form_class_with_form_class(self):
        """Test get_form_class with form_class attribute."""
        self.view.form_class = CustomModelForm
        form_class = self.view.get_form_class()
        self.assertEqual(form_class, CustomModelForm)

    def test_get_form_class_with_viewset_update_form_class(self):
        """Test get_form_class with viewset get_update_form_class."""
        # Make a copy of the class to avoid modifying the original for other tests
        import copy

        viewset_class = copy.copy(ViewsetWithPermissions)

        # Ensure the method returns what we expect
        viewset_class.get_update_form_class = lambda self, request: SpecialUpdateForm

        self.view.viewset = viewset_class()
        request = self.factory.get(f"/update/{self.test_user.pk}/")
        self.view.request = request
        form_class = self.view.get_form_class()
        self.assertEqual(form_class, SpecialUpdateForm)

    def test_get_form_class_with_viewset_form_class(self):
        """Test get_form_class with viewset get_form_class."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get(f"/update/{self.test_user.pk}/")
        self.view.request = request
        # Remove get_update_form_class to test fallback
        delattr(ViewsetWithPermissions, "get_update_form_class")
        form_class = self.view.get_form_class()
        self.assertEqual(form_class, CustomModelForm)

    def test_get_form_class_with_modelform_factory(self):
        """Test get_form_class with modelform_factory."""
        # For this test, we need to mock modelform_factory to return a proper form
        from unittest.mock import patch
        from django.forms import ModelForm as DjangoModelForm

        class TestModelForm(DjangoModelForm):
            class Meta:
                model = User
                fields = ["username", "email"]

        # Patch modelform_factory to return our test form
        with patch("material.views.update.modelform_factory", return_value=TestModelForm):
            self.view.viewset = None
            form_class = self.view.get_form_class()

            # Check that we got the right form class
            self.assertEqual(form_class, TestModelForm)

            # Create an instance and check fields
            form = form_class()
            self.assertIn("username", form.fields)
            self.assertIn("email", form.fields)

    def test_get_template_names_with_template_name(self):
        """Test template names with template_name set."""
        self.view.template_name = "custom_template.html"
        templates = self.view.get_template_names()
        self.assertEqual(templates, ["custom_template.html"])

    def test_get_template_names_without_template_name(self):
        """Test template names without template_name set."""
        self.view.template_name = None

        templates = self.view.get_template_names()
        self.assertEqual(
            templates, ["auth/user_update.html", "auth/user_form.html", "material/views/form.html"]
        )

    def test_get_success_url_with_viewset(self):
        """Test get_success_url with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        self.view.request = self.factory.get(f"/update/{self.test_user.pk}/")
        self.view.object = self.test_user

        url = self.view.get_success_url()
        self.assertEqual(url, "/custom-success-url/")

    def test_get_success_url_without_viewset(self):
        """Test get_success_url without viewset."""
        self.view.viewset = None
        self.view.object = self.test_user

        url = self.view.get_success_url()
        self.assertEqual(url, "../")

    def test_get_object_with_invalid_pk(self):
        """Test get_object with invalid pk."""
        self.view.viewset = None
        self.view.request = self.factory.get("/update/invalid/")
        self.view.request.user = self.allowed_user

        # Setup kwargs with a non-existent ID
        self.view.kwargs = {"pk": "999999"}

        with self.assertRaises(Http404):
            self.view.get_object()

    def test_get_object_without_permission(self):
        """Test get_object without permission."""
        from unittest.mock import patch

        # Mock has_change_permission to return False
        with patch.object(UpdateModelView, "has_change_permission", return_value=False):
            self.view.viewset = None
            self.view.kwargs = {
                "pk": str(self.test_user.pk)
            }  # Convert to string to avoid unquote issue
            self.view.request = self.factory.get(f"/update/{self.test_user.pk}/")

            with self.assertRaises(PermissionDenied):
                self.view.get_object()

    def test_message_user(self):
        """Test message_user method."""
        from django.contrib.messages.storage.fallback import FallbackStorage
        from django.contrib.sessions.middleware import SessionMiddleware

        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get(f"/update/{self.test_user.pk}/")

        # Add session
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        # Add messages
        messages = FallbackStorage(request)
        request._messages = messages

        self.view.request = request
        self.view.object = self.test_user

        # This should not raise exceptions
        self.view.message_user()
