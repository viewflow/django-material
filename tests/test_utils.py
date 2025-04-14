import re
from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import User, Permission

from material.utils import (
    MARKER,
    DEFAULT,
    first_not_default,
    camel_case_to_underscore,
    camel_case_to_title,
    has_object_perm,
    strip_suffixes,
    viewprop,
    list_path_components,
)


class MarkerTests(TestCase):
    def test_marker_repr(self):
        marker = MARKER("TEST")
        self.assertEqual(repr(marker), "TEST")
        
    def test_marker_iter(self):
        marker = MARKER("TEST")
        self.assertEqual(list(marker), [])
        
    def test_marker_comparison(self):
        marker1 = MARKER("A")
        marker2 = MARKER("B")
        self.assertTrue(marker1 < marker2)
        self.assertTrue(marker1 < "C")


class DefaultValueTests(TestCase):
    def test_first_not_default_with_default(self):
        self.assertEqual(first_not_default(DEFAULT, "value", DEFAULT), "value")
        
    def test_first_not_default_all_default(self):
        self.assertEqual(first_not_default(DEFAULT, DEFAULT), DEFAULT)
        
    def test_first_not_default_empty(self):
        self.assertIsNone(first_not_default())


class CaseConversionTests(TestCase):
    def test_camel_to_underscore(self):
        self.assertEqual(camel_case_to_underscore("CamelCase"), "camel_case")
        self.assertEqual(camel_case_to_underscore("camelCase"), "camel_case")
        self.assertEqual(camel_case_to_underscore("CamelCaseXYZ"), "camel_case_xyz")
        
    def test_camel_to_title(self):
        self.assertEqual(camel_case_to_title("CamelCase"), "Camel case")
        self.assertEqual(camel_case_to_title("camelCase"), "Camel case")
        self.assertEqual(camel_case_to_title("CamelCaseXYZ"), "Camel case xyz")


class PermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        
    def test_has_object_perm_without_perm(self):
        self.assertFalse(has_object_perm(self.user, "view", User))
        
    def test_has_object_perm_with_perm(self):
        perm = Permission.objects.get(codename="view_user")
        self.user.user_permissions.add(perm)
        self.assertTrue(has_object_perm(self.user, "view", User))
        
    def test_has_object_perm_with_obj(self):
        with mock.patch.object(self.user, 'has_perm', side_effect=[False, True]):
            self.assertTrue(has_object_perm(self.user, "view", User, obj=self.user))


class StripSuffixesTests(TestCase):
    def test_strip_suffixes(self):
        self.assertEqual(strip_suffixes("filename.txt", [".txt", ".md"]), "filename")
        
    def test_strip_suffixes_multiple(self):
        self.assertEqual(strip_suffixes("filename.txt.bak", [".bak", ".txt"]), "filename")
        
    def test_strip_suffixes_whole_word(self):
        self.assertEqual(strip_suffixes("txt", [".txt", "txt"]), "txt")


class ViewPropTests(TestCase):
    def test_viewprop(self):
        class TestClass:
            @viewprop
            def prop(self):
                return "original"
                
        obj = TestClass()
        self.assertEqual(obj.prop, "original")
        obj.prop = "modified"
        self.assertEqual(obj.prop, "modified")


class PathComponentsTests(TestCase):
    def test_list_path_components_empty(self):
        self.assertEqual(list_path_components("simple/path"), [])
        
    def test_list_path_components_single(self):
        self.assertEqual(list_path_components("path/<str:pk>/"), ["pk"])
        
    def test_list_path_components_multiple(self):
        self.assertEqual(list_path_components("<str:pk>/<int:id>/"), ["pk", "id"])