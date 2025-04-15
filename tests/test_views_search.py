from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import RequestFactory, TestCase
from django.views.generic import ListView

from material.views.search import (
    SearchableViewMixin,
    lookup_spawns_duplicates,
    construct_search,
    get_search_results,
)


class TestLookupSpawnsDuplicates(TestCase):
    def test_lookup_spawns_duplicates_with_m2m(self):
        """Test the lookup_spawns_duplicates function with a ManyToMany field."""
        # User.groups is a ManyToMany field
        opts = User._meta
        self.assertTrue(lookup_spawns_duplicates(opts, "groups"))

    def test_lookup_spawns_duplicates_with_direct_field(self):
        """Test the lookup_spawns_duplicates function with a direct field."""
        opts = User._meta
        self.assertFalse(lookup_spawns_duplicates(opts, "username"))

    def test_lookup_spawns_duplicates_with_nonexistent_field(self):
        """Test the lookup_spawns_duplicates function with a nonexistent field."""
        opts = User._meta
        # This will just return False since the field doesn't exist
        self.assertFalse(lookup_spawns_duplicates(opts, "nonexistent_field"))


class TestConstructSearch(TestCase):
    def test_construct_search_with_istartswith(self):
        """Test the construct_search function with startswith prefix."""
        opts = User._meta
        self.assertEqual(construct_search(opts, "^username"), "username__istartswith")

    def test_construct_search_with_iexact(self):
        """Test the construct_search function with exact prefix."""
        opts = User._meta
        self.assertEqual(construct_search(opts, "=username"), "username__iexact")

    def test_construct_search_with_search(self):
        """Test the construct_search function with search prefix."""
        opts = User._meta
        self.assertEqual(construct_search(opts, "@username"), "username__search")

    def test_construct_search_with_default_icontains(self):
        """Test the construct_search function with default behavior."""
        opts = User._meta
        self.assertEqual(construct_search(opts, "username"), "username__icontains")

    def test_construct_search_with_lookup(self):
        """Test the construct_search function with a lookup."""
        opts = User._meta
        # Test with a relationship lookup
        self.assertEqual(construct_search(opts, "groups__name"), "groups__name__icontains")


class TestGetSearchResults(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="johndoe", email="john@example.com", first_name="John", last_name="Doe"
        )
        self.user2 = User.objects.create_user(
            username="janedoe", email="jane@example.com", first_name="Jane", last_name="Doe"
        )
        self.user3 = User.objects.create_user(
            username="bobsmith", email="bob@example.com", first_name="Bob", last_name="Smith"
        )

    def test_get_search_results_with_single_field(self):
        """Test the get_search_results function with a single search field."""
        queryset = User.objects.all()
        search_fields = ["username"]
        search_term = "doe"

        results = get_search_results(queryset, search_fields, search_term)
        self.assertEqual(results.count(), 2)
        self.assertIn(self.user1, results)
        self.assertIn(self.user2, results)
        self.assertNotIn(self.user3, results)

    def test_get_search_results_with_multiple_fields(self):
        """Test the get_search_results function with multiple search fields."""
        queryset = User.objects.all()
        search_fields = ["first_name", "last_name"]
        search_term = "Doe"

        results = get_search_results(queryset, search_fields, search_term)
        self.assertEqual(results.count(), 2)
        self.assertIn(self.user1, results)
        self.assertIn(self.user2, results)
        self.assertNotIn(self.user3, results)

    def test_get_search_results_with_complex_term(self):
        """Test the get_search_results function with a complex search term."""
        queryset = User.objects.all()
        search_fields = ["first_name"]
        search_term = "'John'"  # Quoted search term

        results = get_search_results(queryset, search_fields, search_term)
        self.assertEqual(results.count(), 1)
        self.assertIn(self.user1, results)
        self.assertNotIn(self.user2, results)
        self.assertNotIn(self.user3, results)

    def test_get_search_results_with_multiple_terms(self):
        """Test the get_search_results function with multiple search terms."""
        queryset = User.objects.all()
        search_fields = ["first_name", "last_name"]
        search_term = "John Doe"  # Two terms

        results = get_search_results(queryset, search_fields, search_term)
        self.assertEqual(results.count(), 1)
        self.assertIn(self.user1, results)
        self.assertNotIn(self.user2, results)
        self.assertNotIn(self.user3, results)

    def test_get_search_results_with_prefix_notation(self):
        """Test the get_search_results function with prefix notation."""
        queryset = User.objects.all()
        search_fields = ["^username"]  # Starts with
        search_term = "j"

        results = get_search_results(queryset, search_fields, search_term)
        self.assertEqual(results.count(), 2)
        self.assertIn(self.user1, results)
        self.assertIn(self.user2, results)
        self.assertNotIn(self.user3, results)


class SearchableListView(SearchableViewMixin, ListView):
    """Test view class implementing SearchableViewMixin."""

    model = User
    search_fields = ["username", "first_name", "last_name"]


class TestSearchableViewMixin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(
            username="johndoe", email="john@example.com", first_name="John", last_name="Doe"
        )
        self.user2 = User.objects.create_user(
            username="janedoe", email="jane@example.com", first_name="Jane", last_name="Doe"
        )
        self.user3 = User.objects.create_user(
            username="bobsmith", email="bob@example.com", first_name="Bob", last_name="Smith"
        )

        self.view = SearchableListView()
        self.view.search_fields = ["username", "first_name", "last_name"]

    def test_search_enabled(self):
        """Test the search_enabled method."""
        self.assertTrue(self.view.search_enabled())

        self.view.search_fields = None
        self.assertFalse(self.view.search_enabled())

    def test_get_search_term(self):
        """Test the get_search_term method."""
        request = self.factory.get("/", {"_search": "john"})
        self.view.request = request
        self.assertEqual(self.view.get_search_term(), "john")

        request = self.factory.get("/")
        self.view.request = request
        self.assertIsNone(self.view.get_search_term())

    def test_get_queryset_with_search(self):
        """Test the get_queryset method with a search term."""
        request = self.factory.get("/", {"_search": "john"})

        # Setup a testable view instance that can be examined
        view = SearchableListView()
        view.request = request
        view.setup(request)
        view.object_list = None

        queryset = view.get_queryset()
        self.assertIsInstance(queryset, QuerySet)
        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.user1, queryset)
        self.assertNotIn(self.user2, queryset)
        self.assertNotIn(self.user3, queryset)

    def test_get_queryset_without_search(self):
        """Test the get_queryset method without a search term."""
        request = self.factory.get("/")

        # Setup a testable view instance
        view = SearchableListView()
        view.request = request
        view.setup(request)
        view.object_list = None

        queryset = view.get_queryset()
        self.assertIsInstance(queryset, QuerySet)
        self.assertEqual(queryset.count(), 3)
        self.assertIn(self.user1, queryset)
        self.assertIn(self.user2, queryset)
        self.assertIn(self.user3, queryset)
