from collections.abc import Sequence
from typing import Any, TypeVar

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model, Q, QuerySet
from django.db.models.constants import LOOKUP_SEP
from django.db.models.options import Options
from django.http import HttpRequest
from django.utils.text import smart_split, unescape_string_literal


def lookup_spawns_duplicates(opts: Options, lookup_path: str) -> bool:
    """
    Return True if the given lookup path spawns duplicates.

    Based on django.contrib.admin.utils.lookup_spawns_duplicates.
    """
    lookup_fields = lookup_path.split(LOOKUP_SEP)
    # Go through the fields (following all relations) and look for an m2m.
    for field_name in lookup_fields:
        if field_name == "pk":
            field_name = opts.pk.name
        try:
            field = opts.get_field(field_name)
        except FieldDoesNotExist:
            # Ignore query lookups.
            continue
        else:
            if hasattr(field, "path_infos"):
                # This field is a relation; update opts to follow the relation.
                path_info = field.path_infos
                opts = path_info[-1].to_opts
                if any(path.m2m for path in path_info):
                    # This field is a m2m relation so duplicates must be
                    # handled.
                    return True
    return False


def construct_search(opts: Options, field_name: str) -> str:
    """
    Construct the search field path for a given field name.

    Implementation similar to django.contrib.admin.options.ModelAdmin.get_search_results.

    Args:
        opts: The _meta attribute of a model class
        field_name: The name of the field to search on

    Returns:
        A field path that can be used for searching
    """
    if field_name.startswith("^"):
        return f"{field_name[1:]}__istartswith"
    elif field_name.startswith("="):
        return f"{field_name[1:]}__iexact"
    elif field_name.startswith("@"):
        return f"{field_name[1:]}__search"

    # Use field_name if it includes a lookup.
    lookup_fields = field_name.split(LOOKUP_SEP)

    # Go through the fields, following all relations.
    prev_field = None
    for path_part in lookup_fields:
        if path_part == "pk":
            path_part = opts.pk.name
        try:
            field = opts.get_field(path_part)
        except FieldDoesNotExist:
            # Use valid query lookups.
            if prev_field and prev_field.get_lookup(path_part):
                return field_name
        else:
            prev_field = field
            if hasattr(field, "path_infos"):
                # Update opts to follow the relation.
                opts = field.path_infos[-1].to_opts

    # Otherwise, use the field with icontains.
    return f"{field_name}__icontains"


M = TypeVar("M", bound=Model)


def get_search_results(
    queryset: QuerySet[M], search_fields: Sequence[str], search_term: str
) -> QuerySet[M]:
    """
    Filter the queryset based on search term and fields.

    Implementation similar to django.contrib.admin.options.ModelAdmin.get_search_results.

    Args:
        queryset: The queryset to filter
        search_fields: List of field names to search on
        search_term: The search term to filter by

    Returns:
        Filtered queryset that matches the search criteria
    """
    opts = queryset.model._meta

    orm_lookups = [construct_search(opts, str(search_field)) for search_field in search_fields]

    for bit in smart_split(search_term):
        if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
            bit = unescape_string_literal(bit)
        or_queries = Q(
            *((orm_lookup, bit) for orm_lookup in orm_lookups),
            _connector=Q.OR,
        )
        queryset = queryset.filter(or_queries)

    may_have_duplicates = any(
        lookup_spawns_duplicates(opts, search_spec) for search_spec in orm_lookups
    )

    if may_have_duplicates:
        queryset = queryset.distinct()

    return queryset


class SearchableViewMixin:
    """
    Mixin for ListView to enable search capabilities.

    Adds search functionality to a ListView by filtering the queryset based on
    search terms from the request.
    """

    search_fields: Sequence[str] | None = None
    request: HttpRequest

    def search_enabled(self) -> bool:
        """
        Check if search is enabled for this view.

        Returns:
            True if search_fields is defined, False otherwise
        """
        return self.search_fields is not None

    def get_search_term(self) -> str | None:
        """
        Get the search term from the request.

        Returns:
            The search term from the request, or None if not present
        """
        return self.request.GET.get("_search")

    def get_queryset(self) -> QuerySet[Any]:
        """
        Get the queryset filtered by search terms if applicable.

        Returns:
            The queryset, possibly filtered by search terms
        """
        queryset = super().get_queryset()  # type: ignore
        search_term = self.get_search_term()

        if self.search_enabled() and search_term:
            assert self.search_fields is not None
            queryset = get_search_results(queryset, self.search_fields, search_term)

        return queryset
