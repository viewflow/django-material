from unittest import mock

from django.test import TestCase
from django import forms

from material.forms import Layout, Row, Column, Span, FieldSet
from material.views.base import (
    _collect_elements,
    FormLayoutMixin,
    Action,
    BulkActionForm,
)


class TestModelA(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    active = forms.BooleanField(required=False)


class TestModelAWithLayout(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    active = forms.BooleanField(required=False)

    layout = Layout(
        Row(
            Column(
                "name",
                "description",
            ),
            Span("active"),
        )
    )


class CollectElementsTests(TestCase):
    def test_collect_elements_from_layout(self):
        """Test that field names are collected correctly from a layout."""
        layout = Layout(
            Row(
                Column(
                    "field1",
                    "field2",
                ),
                Span("field3"),
            ),
            "field4",
        )

        fields = _collect_elements(layout)
        self.assertEqual(sorted(fields), ["field1", "field2", "field3", "field4"])

    def test_collect_elements_nested_layout(self):
        """Test that field names are collected from deeply nested layouts."""
        layout = Layout(
            Row(
                Column(
                    FieldSet(
                        "Group 1",
                        "field1",
                        "field2",
                    ),
                ),
                Column(
                    "field3",
                    Row(
                        "field4",
                        "field5",
                    ),
                ),
            ),
        )

        fields = _collect_elements(layout)
        self.assertEqual(sorted(fields), ["field1", "field2", "field3", "field4", "field5"])

    def test_collect_elements_empty_layout(self):
        """Test collecting elements from an empty layout."""
        layout = Layout()
        fields = _collect_elements(layout)
        self.assertEqual(fields, [])


class FormLayoutMixinTests(TestCase):
    def test_layout_property_with_form_having_layout(self):
        """Test that layout property returns the form's layout."""
        mixin = FormLayoutMixin()
        mixin.form_class = TestModelAWithLayout

        self.assertEqual(mixin.layout, TestModelAWithLayout.layout)

    def test_layout_property_with_form_without_layout(self):
        """Test that layout property returns None when form has no layout."""
        mixin = FormLayoutMixin()
        mixin.form_class = TestModelA

        self.assertIsNone(mixin.layout)

    def test_fields_property_with_form_having_layout(self):
        """Test that fields property returns fields from layout."""
        mixin = FormLayoutMixin()
        mixin.form_class = TestModelAWithLayout

        fields = mixin.fields
        self.assertEqual(sorted(fields), ["active", "description", "name"])

    def test_fields_property_with_form_without_layout(self):
        """Test that fields property returns '__all__' when no layout exists."""
        mixin = FormLayoutMixin()
        mixin.form_class = TestModelA

        self.assertEqual(mixin.fields, "__all__")

    def test_fields_property_with_no_form_class(self):
        """Test that fields property returns '__all__' when no form class is set."""
        mixin = FormLayoutMixin()
        mixin.form_class = None

        self.assertEqual(mixin.fields, "__all__")


class ActionTests(TestCase):
    def test_action_with_url(self):
        """Test creating an action with a URL."""
        action = Action("Edit", url="/edit/")

        self.assertEqual(action.name, "Edit")
        self.assertEqual(action.url, "/edit/")
        self.assertIsNone(action.viewname)
        self.assertIsNone(action.icon)

    def test_action_with_viewname(self):
        """Test creating an action with a viewname."""
        action = Action("Delete", viewname="delete_view")

        self.assertEqual(action.name, "Delete")
        self.assertIsNone(action.url)
        self.assertEqual(action.viewname, "delete_view")
        self.assertIsNone(action.icon)

    def test_action_with_icon(self):
        """Test creating an action with an icon."""
        action = Action("Download", url="/download/", icon="file_download")

        self.assertEqual(action.name, "Download")
        self.assertEqual(action.url, "/download/")
        self.assertIsNone(action.viewname)
        self.assertEqual(action.icon, "file_download")

    def test_action_without_url_or_viewname_raises_error(self):
        """Test that creating an action without URL or viewname raises an error."""
        with self.assertRaises(AssertionError):
            Action("Invalid")


class BulkActionFormTests(TestCase):
    def test_form_initialization(self):
        """Test that the form is initialized correctly with model fields."""
        from django.contrib.auth.models import User

        form = BulkActionForm(model=User)

        self.assertIn("pk", form.fields)
        self.assertIn("select_all", form.fields)
        self.assertIsInstance(form.fields["pk"], forms.ModelMultipleChoiceField)
        self.assertIsInstance(form.fields["select_all"], forms.CharField)
        self.assertFalse(form.fields["pk"].required)
        self.assertFalse(form.fields["select_all"].required)
