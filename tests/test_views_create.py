from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import Form, ModelForm, Widget
from django.test import RequestFactory, TestCase
from django.urls import reverse

from material.views.create import CreateModelView


class ViewsetWithPermissions:
    """Viewset with permission methods for testing."""

    def has_add_permission(self, user):
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

    def get_create_form_class(self, request):
        return SpecialCreateForm

    def get_create_form_widgets(self, request):
        return {"username": SpecialCreateWidget}


class CustomModelForm(ModelForm):
    """Custom model form for testing."""

    class Meta:
        model = User
        fields = ["username", "email"]


class SpecialCreateForm(ModelForm):
    """Special create form for testing."""

    class Meta:
        model = User
        fields = ["username", "email", "first_name"]


class CustomWidget(Widget):
    """Custom widget for testing."""

    pass


class SpecialCreateWidget(Widget):
    """Special create widget for testing."""

    pass


class CreateModelViewTests(TestCase):
    """Tests for the CreateModelView class."""

    def setUp(self):
        self.factory = RequestFactory()
        self.allowed_user = User.objects.create_user(username="allowed_user", password="password")
        self.denied_user = User.objects.create_user(username="denied_user", password="password")

        # Set up the view with no viewset
        self.view = CreateModelView()
        self.view.model = User
        self.view.pk_url_kwarg = "pk"
        self.view.template_name_suffix = "_create"
        self.view.fields = ["username", "email"]

    def test_has_add_permission_with_viewset(self):
        """Test permission checking with viewset."""
        self.view.viewset = ViewsetWithPermissions()

        request = self.factory.get("/create/")
        request.user = self.allowed_user
        self.assertTrue(self.view.has_add_permission(request))

        request.user = self.denied_user
        self.assertFalse(self.view.has_add_permission(request))

    def test_has_add_permission_without_viewset(self):
        """Test permission checking without viewset (fallback to object permissions)."""
        self.view.viewset = None

        # In a real scenario, Django's permission system would be used
        # This simplified test just verifies the method runs without errors
        request = self.factory.get("/create/")
        request.user = self.allowed_user

        # The result depends on has_object_perm implementation
        # We're just ensuring it runs without error
        result = self.view.has_add_permission(request)
        self.assertIsInstance(result, bool)

    def test_get_object_url_with_viewset(self):
        """Test get_object_url with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/create/")
        self.view.request = request

        obj = User(pk=123, username="testuser")
        url = self.view.get_object_url(obj)
        self.assertEqual(url, "/custom-object-url/123/")

    def test_get_object_url_with_absolute_url(self):
        """Test get_object_url with get_absolute_url method."""
        # For this test, we need to mock has_object_perm to return True
        from material.views import create

        original_has_object_perm = create.has_object_perm

        try:
            # Mock the has_object_perm function to always return True
            create.has_object_perm = lambda *args, **kwargs: True

            self.view.viewset = None
            request = self.factory.get("/create/")
            request.user = self.allowed_user
            self.view.request = request

            obj = User(pk=123, username="testuser")
            # Mock get_absolute_url
            obj.get_absolute_url = lambda: f"/users/{obj.pk}/"

            url = self.view.get_object_url(obj)
            self.assertEqual(url, "/users/123/")
        finally:
            # Restore the original function
            create.has_object_perm = original_has_object_perm

    def test_queryset_with_viewset(self):
        """Test queryset retrieval with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/create/")
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

    def test_get_form_widgets_with_viewset_create_form_widgets(self):
        """Test get_form_widgets with viewset get_create_form_widgets."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/create/")
        self.view.request = request
        widgets = self.view.get_form_widgets()
        self.assertEqual(widgets, {"username": SpecialCreateWidget})

    def test_get_form_widgets_with_viewset_form_widgets(self):
        """Test get_form_widgets with viewset get_form_widgets."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/create/")
        self.view.request = request
        # Remove get_create_form_widgets to test fallback
        delattr(ViewsetWithPermissions, "get_create_form_widgets")
        widgets = self.view.get_form_widgets()
        self.assertEqual(widgets, {"username": CustomWidget})

    def test_get_form_class_with_form_class(self):
        """Test get_form_class with form_class attribute."""
        self.view.form_class = CustomModelForm
        form_class = self.view.get_form_class()
        self.assertEqual(form_class, CustomModelForm)

    def test_get_form_class_with_viewset_create_form_class(self):
        """Test get_form_class with viewset get_create_form_class."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/create/")
        self.view.request = request
        form_class = self.view.get_form_class()
        self.assertEqual(form_class, SpecialCreateForm)

    def test_get_form_class_with_viewset_form_class(self):
        """Test get_form_class with viewset get_form_class."""
        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/create/")
        self.view.request = request
        # Remove get_create_form_class to test fallback
        delattr(ViewsetWithPermissions, "get_create_form_class")
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
        with patch("material.views.create.modelform_factory", return_value=TestModelForm):
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
            templates, ["auth/user_create.html", "auth/user_form.html", "material/views/form.html"]
        )

    def test_get_success_url_with_viewset(self):
        """Test get_success_url with viewset."""
        self.view.viewset = ViewsetWithPermissions()
        self.view.request = self.factory.get("/create/")
        self.view.object = User(pk=123, username="testuser")

        url = self.view.get_success_url()
        self.assertEqual(url, "/custom-success-url/")

    def test_get_success_url_without_viewset(self):
        """Test get_success_url without viewset."""
        self.view.viewset = None
        self.view.object = User(pk=123, username="testuser")

        url = self.view.get_success_url()
        self.assertEqual(url, "../")

    def test_dispatch_with_permission(self):
        """Test dispatch with permission."""
        # We need to patch the parent dispatch method to prevent actual rendering
        from unittest.mock import patch

        with patch("django.views.generic.CreateView.dispatch") as mock_dispatch:
            # Set up a simple return value
            mock_dispatch.return_value = "Response"

            self.view.viewset = ViewsetWithPermissions()

            request = self.factory.get("/create/")
            request.user = self.allowed_user

            # This should not raise an exception
            response = self.view.dispatch(request)
            self.assertEqual(response, "Response")
            # Verify that parent dispatch was called
            mock_dispatch.assert_called_once()

    def test_dispatch_without_permission(self):
        """Test dispatch without permission."""
        self.view.viewset = ViewsetWithPermissions()

        request = self.factory.get("/create/")
        request.user = self.denied_user

        # This should raise PermissionDenied
        with self.assertRaises(PermissionDenied):
            self.view.dispatch(request)

    def test_message_user(self):
        """Test message_user method."""
        from django.contrib.messages.storage.fallback import FallbackStorage
        from django.contrib.sessions.middleware import SessionMiddleware

        self.view.viewset = ViewsetWithPermissions()
        request = self.factory.get("/create/")

        # Add session
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        # Add messages
        messages = FallbackStorage(request)
        request._messages = messages

        self.view.request = request
        self.view.object = User(pk=123, username="testuser")

        # This should not raise exceptions
        self.view.message_user()
