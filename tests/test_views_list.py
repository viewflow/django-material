from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import QuerySet
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from material.views.list import (
    BaseColumn,
    BulkActionsMixin,
    DataSourceColumn,
    FilterableViewMixin,
    Icon,
    ListModelView,
    ModelFieldColumn,
    ObjectAttrColumn,
    OrderableListViewMixin,
    _get_method_attr,
)


class IconTests(TestCase):
    """Tests for the Icon class."""

    def test_str_representation(self):
        """Test the string representation of an icon."""
        icon = Icon("check")
        self.assertEqual(str(icon), '<span class="material-symbols-rounded">check</span>')


class GetMethodAttrTests(TestCase):
    """Tests for the _get_method_attr function."""

    def test_get_method_attr_direct(self):
        """Test getting an attribute directly from a method."""

        class TestClass:
            def method(self):
                pass

            method.attribute = "value"

        instance = TestClass()
        result = _get_method_attr(instance, "method", "attribute")
        self.assertEqual(result, "value")

    def test_get_method_attr_direct(self):
        """Test getting an attribute directly from an object."""

        class TestClass:
            method_attribute = "value"

        instance = TestClass()
        result = _get_method_attr(instance, "method_attribute", "value", "default")
        self.assertEqual(result, "default")

    def test_get_method_attr_default(self):
        """Test getting a default value for a non-existent attribute."""

        class TestClass:
            def method(self):
                pass

        instance = TestClass()
        result = _get_method_attr(instance, "method", "nonexistent", "default")
        self.assertEqual(result, "default")


class ModelFieldColumnTests(TestCase):
    """Tests for the ModelFieldColumn class."""

    def test_get_value(self):
        """Test getting a value from a model field."""
        user = User(username="testuser")
        field = User._meta.get_field("username")
        column = ModelFieldColumn(field)

        self.assertEqual(column.get_value(user), "testuser")

    def test_header(self):
        """Test getting a header from a model field."""
        field = User._meta.get_field("username")
        column = ModelFieldColumn(field)

        self.assertEqual(column.header(), "Username")

    def test_column_type_number(self):
        """Test getting the column type for a number field."""
        field = models.IntegerField()
        column = ModelFieldColumn(field)

        self.assertEqual(column.column_type(), "numeric")

    def test_column_type_boolean(self):
        """Test getting the column type for a boolean field."""
        field = models.BooleanField()
        column = ModelFieldColumn(field)

        self.assertEqual(column.column_type(), "boolean")

    def test_column_type_text(self):
        """Test getting the column type for a text field."""
        field = models.CharField()
        column = ModelFieldColumn(field)

        self.assertEqual(column.column_type(), "text")

    def test_orderby(self):
        """Test getting the ordering field."""
        field = User._meta.get_field("username")
        column = ModelFieldColumn(field)

        self.assertEqual(column.orderby(), "username")

    def test_format_value_choice(self):
        """Test formatting a choice field value."""
        field = models.IntegerField(choices=[(1, "One"), (2, "Two")])
        # Setting flatchoices via property is not possible, so mock it
        from unittest.mock import patch, PropertyMock

        with patch(
            "django.db.models.fields.Field.flatchoices", new_callable=PropertyMock
        ) as mock_flatchoices:
            mock_flatchoices.return_value = [(1, "One"), (2, "Two")]
            column = ModelFieldColumn(field)
            self.assertEqual(column.format_value(None, 1), "One")

    def test_format_value_boolean(self):
        """Test formatting a boolean field value."""
        field = models.BooleanField()
        column = ModelFieldColumn(field)

        self.assertEqual(column.format_value(None, True), str(Icon("check")))
        self.assertEqual(column.format_value(None, False), str(Icon("close")))
        self.assertEqual(column.format_value(None, None), "")


class DataSourceColumnTests(TestCase):
    """Tests for the DataSourceColumn class."""

    def test_get_value_attribute(self):
        """Test getting a value from an attribute."""

        class TestSource:
            attribute = "value"

        source = TestSource()
        column = DataSourceColumn(source, "attribute")

        self.assertEqual(column.get_value(None), "value")

    def test_get_value_callable(self):
        """Test getting a value from a callable."""

        class TestSource:
            def method(self, obj):
                return obj

        source = TestSource()
        column = DataSourceColumn(source, "method")

        self.assertEqual(column.get_value("test"), "test")

    def test_get_value_empty(self):
        """Test getting an empty value."""

        class TestSource:
            def method(self, obj):
                return None

            method.empty_value = "empty"

        source = TestSource()
        column = DataSourceColumn(source, "method")

        self.assertEqual(column.get_value(None), "empty")

    def test_header_verbose_name(self):
        """Test getting a header from verbose_name."""

        class TestSource:
            attribute = "value"

        source = TestSource()
        column = DataSourceColumn(source, "attribute", verbose_name="Custom Name")

        self.assertEqual(column.header(), "Custom Name")

    def test_header_short_description(self):
        """Test getting a header from short_description."""

        class AttrWithDescription(str):
            short_description = "Short Description"

        class TestSource:
            attribute = AttrWithDescription("value")

        source = TestSource()
        column = DataSourceColumn(source, "attribute")

        self.assertEqual(column.header(), "Short Description")

    def test_header_function_name(self):
        """Test getting a header from a callable function name."""

        class TestSource:
            def descriptive_name_function(self, obj=None):
                return "value"

        source = TestSource()
        column = DataSourceColumn(source, "descriptive_name_function")

        self.assertEqual(column.header(), "Descriptive name function")

    def test_column_type(self):
        """Test getting the column type."""

        class AttrWithColumnType(str):
            column_type = "special"

        class TestSource:
            attribute = AttrWithColumnType("value")

        source = TestSource()
        column = DataSourceColumn(source, "attribute")

        self.assertEqual(column.column_type(), "special")

    def test_column_type_boolean(self):
        """Test getting the column type for a boolean attribute."""

        class BooleanAttribute:
            boolean = True

            def __init__(self, value):
                self.value = value

            def __bool__(self):
                return bool(self.value)

        class TestSource:
            attribute = BooleanAttribute(True)

        source = TestSource()
        column = DataSourceColumn(source, "attribute")

        self.assertEqual(column.column_type(), "boolean")


class ObjectAttrColumnTests(TestCase):
    """Tests for the ObjectAttrColumn class."""

    def test_get_value_attribute(self):
        """Test getting a value from an object attribute."""

        class TestObject:
            attribute = "value"

        obj = TestObject()
        column = ObjectAttrColumn(TestObject, "attribute")

        self.assertEqual(column.get_value(obj), "value")

    def test_get_value_callable(self):
        """Test getting a value from a callable object attribute."""

        class TestObject:
            def method(self):
                return "result"

        obj = TestObject()
        column = ObjectAttrColumn(TestObject, "method")

        self.assertEqual(column.get_value(obj), "result")


class MockViewset:
    """Mock viewset for testing."""

    def has_view_permission(self, user, obj=None):
        return user.username == "allowed_user"

    def get_queryset(self, request):
        return User.objects.all()

    def get_list_page_actions(self, request):
        return [{"label": "New", "url": "/new/", "style": "filled"}]

    def get_list_bulk_actions(self, request):
        return [{"label": "Delete", "url": "/delete/", "style": "outlined"}]

    def get_object_url(self, request, obj):
        return f"/users/{obj.pk}/"


class ListModelViewTests(TestCase):
    """Tests for the ListModelView class."""

    def setUp(self):
        self.factory = RequestFactory()
        self.allowed_user = User.objects.create_user(username="allowed_user", password="password")
        self.denied_user = User.objects.create_user(username="denied_user", password="password")
        self.test_user = User.objects.create_user(username="test_user", password="password")

        # Set up the view
        self.view = ListModelView()
        self.view.model = User
        self.view.columns = ["username", "email", "is_active"]

    def test_has_view_permission_with_viewset(self):
        """Test permission checking with viewset."""
        self.view.viewset = MockViewset()

        self.assertTrue(self.view.has_view_permission(self.allowed_user))
        self.assertFalse(self.view.has_view_permission(self.denied_user))

    def test_has_view_permission_without_viewset(self):
        """Test permission checking without viewset."""
        self.view.viewset = None

        # In a real scenario, Django's permission system would be used
        # This just tests that the method runs without errors
        result = self.view.has_view_permission(self.allowed_user)
        self.assertIsInstance(result, bool)

    def test_get_columns(self):
        """Test getting columns."""
        self.assertEqual(self.view.get_columns(), ["username", "email", "is_active"])

        self.view.columns = None
        self.assertEqual(self.view.get_columns(), ["__str__"])

    def test_get_object_link_columns(self):
        """Test getting object link columns."""
        # First test default behavior
        self.assertEqual(self.view.get_object_link_columns(), "username")

        # Test with explicit setting - need to clear the cache first
        from importlib import reload
        from material.views import list as list_module

        reload(list_module)  # This resets the cache

        # Re-setup the view with new object_link_columns
        self.view = list_module.ListModelView()
        self.view.model = User
        self.view.columns = ["username", "email", "is_active"]
        self.view.object_link_columns = ["username", "email"]

        self.assertEqual(self.view.get_object_link_columns(), ["username", "email"])

    def test_get_column_def_str(self):
        """Test getting a column definition for __str__."""
        column = self.view.get_column_def("__str__")
        self.assertIsInstance(column, ObjectAttrColumn)
        self.assertEqual(column.attr_name, "__str__")

    def test_get_column_def_field(self):
        """Test getting a column definition for a model field."""
        column = self.view.get_column_def("username")
        self.assertIsInstance(column, ModelFieldColumn)
        self.assertEqual(column.attr_name, "username")

    def test_get_column_def_method(self):
        """Test getting a column definition for a model method."""
        column = self.view.get_column_def("get_username")
        self.assertIsInstance(column, ObjectAttrColumn)
        self.assertEqual(column.attr_name, "get_username")

    def test_get_object_url(self):
        """Test getting the object URL."""
        self.view.viewset = MockViewset()
        self.view.request = self.factory.get("/")

        url = self.view.get_object_url(self.test_user)
        self.assertEqual(url, f"/users/{self.test_user.pk}/")

    def test_list_columns(self):
        """Test getting the list of columns."""
        columns = self.view.list_columns
        self.assertIsInstance(columns, dict)
        self.assertEqual(len(columns), 3)
        self.assertIn("username", columns)
        self.assertIn("email", columns)
        self.assertIn("is_active", columns)

    def test_format_value(self):
        """Test formatting a value."""
        self.view.request = self.factory.get("/")

        # Mock the get_object_url method
        self.view.get_object_url = lambda obj: f"/users/{obj.pk}/"

        column = self.view.get_column_def("username")
        formatted = self.view.format_value(self.test_user, column, "test_user")

        # Should be a link since username is the default link column
        self.assertIn(f'href="/users/{self.test_user.pk}/"', formatted)
        self.assertIn("test_user", formatted)

    def test_get_page_actions(self):
        """Test getting page actions."""
        self.view.viewset = MockViewset()
        self.view.request = self.factory.get("/")

        actions = self.view.get_page_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["label"], "New")
        self.assertEqual(actions[0]["url"], "/new/")

        # Test with custom page actions
        self.view.page_actions = [{"label": "Custom", "url": "/custom/", "style": "text"}]
        actions = self.view.get_page_actions()
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]["label"], "Custom")

    def test_queryset(self):
        """Test getting the queryset."""
        # Create a fresh instance of MockViewset for this test
        self.view.viewset = MockViewset()
        self.view.request = self.factory.get("/")

        queryset = self.view.queryset
        self.assertIsInstance(queryset, QuerySet)

        # Create a completely new view without a viewset
        view_without_viewset = ListModelView()
        view_without_viewset.model = User
        view_without_viewset.request = self.factory.get("/")
        # Ensure viewset is None
        view_without_viewset.viewset = None
        # Call queryset property
        result = view_without_viewset.queryset
        self.assertIsNone(result)

    def test_get_template_names(self):
        """Test getting template names."""
        self.view.template_name = None

        templates = self.view.get_template_names()
        self.assertEqual(templates, ["auth/user_list.html", "material/views/list.html"])

        self.view.template_name = "custom.html"
        templates = self.view.get_template_names()
        self.assertEqual(templates, ["custom.html"])

    def test_dispatch_with_permission(self):
        """Test dispatch with permission."""
        from unittest.mock import patch, MagicMock

        with patch.object(ListModelView, "has_view_permission", return_value=True):
            request = self.factory.get("/")
            request.user = MagicMock()  # Add mock user to request
            self.view.request = request

            # Mock the parent dispatch method
            with patch("django.views.generic.ListView.dispatch") as mock_dispatch:
                mock_dispatch.return_value = "Response"

                response = self.view.dispatch(request)
                self.assertEqual(response, "Response")
                mock_dispatch.assert_called_once()

    def test_dispatch_without_permission(self):
        """Test dispatch without permission."""
        from unittest.mock import patch, MagicMock

        with patch.object(ListModelView, "has_view_permission", return_value=False):
            request = self.factory.get("/")
            request.user = MagicMock()  # Add mock user to request
            self.view.request = request

            with self.assertRaises(PermissionDenied):
                self.view.dispatch(request)


class OrderableListViewMixinTests(TestCase):
    """Tests for the OrderableListViewMixin."""

    def setUp(self):
        self.factory = RequestFactory()

        # Define a proper test column class
        class TestColumn(BaseColumn):
            def __init__(self, attr_name):
                super().__init__(attr_name)

            def orderby(self):
                return "name"

            def header(self):
                return "Name"

            def column_type(self):
                return "text"

            def get_value(self, obj):
                return getattr(obj, self.attr_name, "")

        # Set up a view with the mixin
        class TestView(OrderableListViewMixin):
            ordering = "name"
            request = None

            def __init__(self):
                self.list_columns = {"name": TestColumn("name")}

        self.view = TestView()

    def test_get_ordering_from_request(self):
        """Test getting ordering from request parameters."""
        self.view.request = self.factory.get("/?_orderby=name")
        self.assertEqual(self.view.get_ordering(), ["name"])

        self.view.request = self.factory.get("/?_orderby=-name")
        self.assertEqual(self.view.get_ordering(), ["-name"])

    def test_get_ordering_default(self):
        """Test getting default ordering."""
        self.view.request = self.factory.get("/")
        self.assertEqual(self.view.get_ordering(), ["name"])

        self.view.ordering = ["name", "email"]
        self.assertEqual(self.view.get_ordering(), ["name", "email"])

    def test_columns_order(self):
        """Test getting column ordering."""
        # Test ascending order
        self.view.request = self.factory.get("/?_orderby=name")
        column = list(self.view.list_columns.values())[0]
        ordering = self.view.columns_order
        self.assertIn(column, ordering)
        self.assertEqual(ordering[column], "asc")

        # Create a new view instance to test descending order
        # This avoids cached_property issues
        class TestColumn(BaseColumn):
            def __init__(self, attr_name):
                super().__init__(attr_name)

            def orderby(self):
                return "name"

            def header(self):
                return "Name"

            def column_type(self):
                return "text"

            def get_value(self, obj):
                return getattr(obj, self.attr_name, "")

        class TestView(OrderableListViewMixin):
            ordering = "name"
            request = None

            def __init__(self):
                self.list_columns = {"name": TestColumn("name")}

        desc_view = TestView()
        desc_view.request = self.factory.get("/?_orderby=-name")
        desc_column = list(desc_view.list_columns.values())[0]
        desc_ordering = desc_view.columns_order
        self.assertEqual(desc_ordering[desc_column], "desc")


class BulkActionsMixinTests(TestCase):
    """Tests for the BulkActionsMixin."""

    def setUp(self):
        self.factory = RequestFactory()

        # Set up a view with the mixin
        class TestView(BulkActionsMixin):
            request = None

        self.view = TestView()
        self.view.request = self.factory.get("/")

    def test_get_bulk_actions_empty(self):
        """Test getting bulk actions when none are defined."""
        actions = self.view.get_bulk_actions()
        self.assertEqual(actions, [])

    def test_get_bulk_actions_from_instance(self):
        """Test getting bulk actions from the instance."""
        self.view.bulk_actions = [{"label": "Delete", "url": "/delete/"}]

        actions = self.view.get_bulk_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["label"], "Delete")

    def test_get_bulk_actions_from_viewset(self):
        """Test getting bulk actions from a viewset."""
        self.view.viewset = MockViewset()

        actions = self.view.get_bulk_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["label"], "Delete")

    def test_get_bulk_actions_combined(self):
        """Test getting bulk actions from both instance and viewset."""
        self.view.viewset = MockViewset()
        self.view.bulk_actions = [{"label": "Archive", "url": "/archive/"}]

        actions = self.view.get_bulk_actions()
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]["label"], "Archive")
        self.assertEqual(actions[1]["label"], "Delete")
