# Copyright (c) 2017-2025, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

import datetime
import decimal
from collections.abc import Iterator, Sequence
from functools import cache
from typing import Any

from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.db import models
from django.forms.utils import pretty_name
from django.http import HttpRequest, HttpResponse
from django.utils import formats, timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.views import generic

from material.utils import has_object_perm, viewprop


class Icon:
    """Icon class for displaying Material Design icons."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f'<span class="material-symbols-rounded">{self.name}</span>'


def _get_method_attr(
    data_source: Any, method_name: str, attr_name: str, default: Any = None
) -> Any:
    """
    Get an attribute from a method of a data source.

    Args:
        data_source: The object to get the method from
        method_name: The name of the method
        attr_name: The name of the attribute to get from the method
        default: The default value to return if the attribute is not found

    Returns:
        The attribute value or default if not found
    """
    attr = getattr(data_source, method_name)

    # Direct attribute access
    if hasattr(attr, attr_name):
        return getattr(attr, attr_name)

    # Property getter function attribute access
    if isinstance(attr, property) and hasattr(attr, "fget"):
        fget = attr.fget
        if hasattr(fget, attr_name):
            return getattr(fget, attr_name)

    return default


class BaseColumn:
    """Base class for all column types in list views."""

    def __init__(self, attr_name: str) -> None:
        """
        Initialize a column with an attribute name.

        Args:
            attr_name: The name of the attribute to display in the column
        """
        self.attr_name = attr_name

    def get_value(self, obj: Any) -> Any:
        """
        Get the value to display in the column for an object.

        Args:
            obj: The object to get the value from

        Returns:
            The value to display

        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        raise NotImplementedError("subclasses must implement this method.")

    def header(self) -> str:
        """
        Get the header text for the column.

        Returns:
            The header text

        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        raise NotImplementedError("subclasses must implement this method")

    def column_type(self) -> str:
        """
        Get the type of the column for CSS styling.

        Returns:
            The column type (e.g., 'text', 'numeric', 'boolean')

        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        raise NotImplementedError("subclasses must implement this method")

    def orderby(self) -> str | models.Expression | None:
        """
        Get the field name to use for ordering by this column.

        Returns:
            The field name or None if not orderable

        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        raise NotImplementedError("subclasses must implement this method")

    def format_value(self, obj: Any, value: Any) -> str:
        """
        Format a value for display in the column.

        Args:
            obj: The object being displayed
            value: The value to format

        Returns:
            The formatted value as a string
        """
        if value is None:
            return ""
        elif isinstance(value, datetime.datetime):
            return formats.localize(timezone.localtime(value))
        elif isinstance(value, (datetime.date, datetime.time)):
            return formats.localize(value)
        elif isinstance(value, (int, float, decimal.Decimal)):
            return formats.number_format(value)
        elif isinstance(value, (list, tuple)):
            return ", ".join(force_str(v) for v in value)
        else:
            return force_str(value)


class ModelFieldColumn(BaseColumn):
    """
    Column for displaying a model field value.

    Field verbose name is used as the column header.
    """

    NUMBER_FIELD_TYPES = (
        models.IntegerField,
        models.DecimalField,
        models.FloatField,
    )

    BOOLEAN_FIELD_TYPES = (models.BooleanField, models.NullBooleanField)

    def __init__(self, model_field: models.Field) -> None:
        """
        Initialize a column for a model field.

        Args:
            model_field: The model field to display in this column
        """
        super().__init__(model_field.name)
        self.model_field = model_field

    def get_value(self, obj: models.Model) -> Any:
        """
        Get the value of the field for an object.

        Args:
            obj: The model instance to get the field value from

        Returns:
            The field value
        """
        return getattr(obj, self.model_field.name)

    def header(self) -> str:
        """
        Get the header text for the column from the field's verbose name.

        Returns:
            The capitalized verbose name of the field
        """
        try:
            return self.model_field.verbose_name.capitalize()
        except AttributeError:
            # field is likely a ForeignObjectRel
            return self.model_field.related_model._meta.verbose_name.capitalize()

    def column_type(self) -> str:
        """
        Get the column type based on the field type.

        Returns:
            'numeric' for number fields, 'boolean' for boolean fields,
            otherwise 'text'
        """
        if isinstance(self.model_field, ModelFieldColumn.NUMBER_FIELD_TYPES):
            return "numeric"
        elif isinstance(self.model_field, ModelFieldColumn.BOOLEAN_FIELD_TYPES):
            return "boolean"
        return "text"

    def orderby(self) -> str:
        """
        Get the field name to use for ordering.

        Returns:
            The attribute name of this column
        """
        return self.attr_name

    def format_value(self, obj: models.Model, value: Any) -> str:
        """
        Format a field value for display, handling choices and boolean fields specially.

        Args:
            obj: The model instance
            value: The field value to format

        Returns:
            The formatted value as a string
        """
        if getattr(self.model_field, "flatchoices", None):
            return dict(self.model_field.flatchoices).get(value, "")
        elif isinstance(self.model_field, ModelFieldColumn.BOOLEAN_FIELD_TYPES):
            if value is None:
                return ""  # Icon("remove")
            elif value is True:
                return str(Icon("check"))
            else:
                return str(Icon("close"))
        else:
            return super().format_value(obj, value)


class DataSourceColumn(BaseColumn):
    """
    Column that retrieves its value from an external data source.

    Data source attribute could be a property or callable.
    For a callable, to get the value it would be called with the model instance.
    """

    def __init__(self, data_source: Any, attr_name: str, verbose_name: str | None = None) -> None:
        """
        Initialize a column with a data source.

        Args:
            data_source: The object to get values from
            attr_name: The name of the attribute to use
            verbose_name: Optional override for the column header
        """
        super().__init__(attr_name)
        self.verbose_name = verbose_name
        self.data_source = data_source

    def _get_attr_boolean(self) -> bool:
        """
        Check if the attribute is marked as a boolean.

        Returns:
            True if the attribute is boolean, False otherwise
        """
        return _get_method_attr(self.data_source, self.attr_name, "boolean", False)

    def _get_attr_empty_value(self) -> Any:
        """
        Get the empty value for the attribute.

        Returns:
            The empty value or None if not specified
        """
        return _get_method_attr(self.data_source, self.attr_name, "empty_value")

    def get_value(self, obj: Any) -> Any:
        """
        Get the value from the data source.

        Args:
            obj: The object to get the value for

        Returns:
            The value from the data source
        """
        attr = getattr(self.data_source, self.attr_name)
        if callable(attr):
            attr = attr(obj)
        if attr is None:
            attr = self._get_attr_empty_value()
        return attr

    def header(self) -> str:
        """
        Get the header text for the column.

        Returns:
            The header text determined from verbose_name, short_description,
            or pretty-formatted attribute name
        """
        if self.verbose_name is not None:
            return self.verbose_name
        attr = getattr(self.data_source, self.attr_name)

        # Direct attribute short_description
        if hasattr(attr, "short_description"):
            return attr.short_description

        # Property getter short_description
        elif (
            isinstance(attr, property)
            and hasattr(attr, "fget")
            and hasattr(attr.fget, "short_description")
        ):
            return attr.fget.short_description

        # Callable name
        elif callable(attr):
            return "--" if attr.__name__ == "<lambda>" else pretty_name(attr.__name__)

        # Default to pretty attribute name
        else:
            return pretty_name(self.attr_name)

    def column_type(self) -> str:
        """
        Get the column type based on attribute metadata.

        Returns:
            'boolean' if the attribute is marked as boolean,
            otherwise the type from column_type attribute or 'text'
        """
        is_boolean = _get_method_attr(self.data_source, self.attr_name, "boolean", None)
        if is_boolean:
            return "boolean"
        return _get_method_attr(self.data_source, self.attr_name, "column_type", "text")

    def orderby(self) -> str | None:
        """
        Get the field to use for ordering by this column.

        Returns:
            The field name or None if not orderable
        """
        return _get_method_attr(self.data_source, self.attr_name, "orderby_column", None)

    def format_value(self, obj: Any, value: Any) -> str:
        """
        Format a value for display, handling boolean attributes specially.

        Args:
            obj: The object being displayed
            value: The value to format

        Returns:
            The formatted value as a string
        """
        if self._get_attr_boolean():
            if value is None:
                return " "  # Icon("indeterminate_check_box")
            elif value is True:
                return str(Icon("check"))
            else:
                return str(Icon("close"))
        else:
            return super().format_value(obj, value)


class ObjectAttrColumn(DataSourceColumn):
    """
    Column that retrieves its value from a model instance attribute.

    If the object attribute is a callable, to get the value it will be
    called without any arguments.
    """

    def get_value(self, obj: Any) -> Any:
        """
        Get the value of an attribute from an object.

        Args:
            obj: The object to get the attribute from

        Returns:
            The attribute value or result of calling the attribute
        """
        attr = getattr(obj, self.attr_name)
        if callable(attr):
            return attr()
        return attr


class FilterableViewMixin:
    """Mixin for adding filtering capabilities to a list view."""

    pass


class OrderableListViewMixin:
    """Mixin for adding ordering capabilities to a list view."""

    ordering: str | list[str] | tuple[str, ...] | None = None
    ordering_kwarg: str = "_orderby"

    def get_ordering(self) -> list[str]:
        """
        Return the field or fields to use for ordering the queryset.

        Returns:
            List of field names to order by
        """
        ordering: list[str] = []

        # url query parameter
        if self.ordering_kwarg in self.request.GET:
            params = self.request.GET[self.ordering_kwarg].split(",")
            for param in params:
                _, prefix, param_name = param.rpartition("-")
                column_def = self.list_columns.get(param_name)  # type: ignore
                if column_def:
                    column_ordering = column_def.orderby()
                    if column_ordering:
                        if hasattr(column_ordering, "as_sql"):
                            ordering.append(
                                column_ordering.desc() if prefix == "-" else column_ordering.asc()
                            )
                        elif (
                            isinstance(column_ordering, str)
                            and column_ordering.startswith("-")
                            and prefix == "-"
                        ):
                            ordering.append(column_ordering[1:])
                        else:
                            ordering.append(prefix + str(column_ordering))
        else:
            # default view ordering
            if isinstance(self.ordering, (list, tuple)):
                ordering.extend(self.ordering)
            elif isinstance(self.ordering, str):
                ordering.append(self.ordering)

            # default queryset order
            if hasattr(self, "queryset") and self.queryset is not None:
                ordering.extend(self.queryset.query.order_by)

        return ordering

    @cached_property
    def columns_order(self) -> dict[BaseColumn, str]:
        """
        Return mapping of columns to their ordering direction.

        Returns:
            Dictionary mapping column objects to 'asc' or 'desc'
        """
        ordering: dict[BaseColumn, str] = {}

        # ordered by the url query
        if self.ordering_kwarg in self.request.GET:
            params = self.request.GET[self.ordering_kwarg].split(",")
            for param in params:
                _, param_prefix, param_name = param.rpartition("-")
                column_def = self.list_columns.get(param_name)  # type: ignore
                if column_def:
                    column_ordering = column_def.orderby()
                    if column_ordering is not None and isinstance(column_ordering, str):
                        # TODO support custom OrderBy expressions
                        (
                            _,
                            column_order_prefix,
                            column_orderby,
                        ) = column_ordering.rpartition("-")
                        ordering[column_def] = (
                            "asc" if column_order_prefix == param_prefix else "desc"
                        )
        else:
            # ordered by explicit self.ordering definition or by queryset.order_by
            raw_ordering: list[str] = []
            if isinstance(self.ordering, (list, tuple)):
                raw_ordering.extend(self.ordering)
            elif isinstance(self.ordering, str):
                raw_ordering.append(self.ordering)
            if hasattr(self, "queryset") and self.queryset is not None:
                raw_ordering.extend(self.queryset.query.order_by)

            for param in raw_ordering:
                _, param_prefix, param_name = param.rpartition("-")
                for column_def in self.list_columns.values():  # type: ignore
                    if column_def in ordering:  # column order already found
                        continue
                    column_ordering = column_def.orderby()
                    if column_ordering is not None and isinstance(column_ordering, str):
                        # TODO support custom OrderBy expressions
                        (
                            _,
                            column_order_prefix,
                            column_orderby,
                        ) = column_ordering.rpartition("-")
                        if param_name == column_orderby:
                            ordering[column_def] = (
                                "asc" if column_order_prefix == param_prefix else "desc"
                            )

        return ordering


class BulkActionsMixin:
    """Mixin for adding bulk action capabilities to a list view."""

    bulk_actions: Sequence[dict[str, Any]] | None = None
    viewset: Any = None

    def get_bulk_actions(self, *actions: Any) -> Sequence[dict[str, Any]]:
        """
        Get the bulk actions for the view.

        Args:
            *actions: Additional actions to include

        Returns:
            List of action dictionaries
        """
        result = list(actions)
        if self.viewset is not None and hasattr(self.viewset, "get_list_bulk_actions"):
            viewset_actions = self.viewset.get_list_bulk_actions(self.request)
            result = list(viewset_actions) + result
        if self.bulk_actions:
            result = list(self.bulk_actions) + result
        return result


class BaseListModelView(generic.ListView):
    """Base class for list views of model objects."""

    viewset: Any = None
    columns: Sequence[str] | None = None
    object_link_columns: str | Sequence[str] | None = None
    paginate_by: int = 25
    page_actions: Sequence[dict[str, Any]] | None = None
    empty_value_display: str = ""
    request: HttpRequest
    model: type[models.Model]

    def has_view_permission(self, user: Any, obj: models.Model | None = None) -> bool:
        """
        Check if the user has permission to view this model.

        Args:
            user: The user to check permissions for
            obj: Optional model instance to check permissions for

        Returns:
            True if the user has permission, False otherwise
        """
        if self.viewset is not None and hasattr(self.viewset, "has_view_permission"):
            return self.viewset.has_view_permission(user, obj=obj)
        else:
            return has_object_perm(user, "view", self.model, obj=obj) or has_object_perm(
                user, "change", self.model, obj=obj
            )

    def get_columns(self) -> list[str]:
        """
        Get the list of column names to display.

        Returns:
            List of column attribute names
        """
        if self.columns is None:
            return ["__str__"]
        return list(self.columns)

    @cache
    def get_object_link_columns(self) -> str | list[str]:
        """
        Get the list of column names that should link to the object detail view.

        Returns:
            Column name or list of column names
        """
        if self.object_link_columns is None:
            return self.get_columns()[0]
        return self.object_link_columns

    def get_column_def(self, attr_name: str) -> BaseColumn:
        """
        Get the column definition for an attribute name.

        Args:
            attr_name: The name of the attribute to get a column for

        Returns:
            Column definition object

        Raises:
            ValueError: If no column definition can be found for the attribute
        """
        opts = self.model._meta

        # object printable string representation
        if attr_name == "__str__":
            return ObjectAttrColumn(self.model, attr_name, opts.verbose_name.capitalize())

        # a method from view or viewset
        data_sources = [self, self.viewset] if self.viewset is not None else [self]
        for data_source in data_sources:
            if hasattr(data_source, attr_name):
                return DataSourceColumn(data_source, attr_name)

        # an object field
        try:
            model_field = opts.get_field(attr_name)
        except FieldDoesNotExist:
            pass
        else:
            return ModelFieldColumn(model_field)

        # a method from object
        if hasattr(self.model, attr_name):
            return ObjectAttrColumn(self.model, attr_name)

        raise ValueError(f"Can't find datasource for {attr_name} column")

    def get_object_url(self, obj: models.Model) -> str | None:
        """
        Get the URL for viewing an object.

        Args:
            obj: The model instance to get a URL for

        Returns:
            URL string or None if not available
        """
        if self.viewset is not None and hasattr(self.viewset, "get_object_url"):
            return self.viewset.get_object_url(self.request, obj)
        else:
            if hasattr(obj, "get_absolute_url") and self.has_view_permission(
                self.request.user, obj
            ):
                return obj.get_absolute_url()
        return None

    @cached_property
    def list_columns(self) -> dict[str, BaseColumn]:
        """
        Get the dictionary of column definitions.

        Returns:
            Dictionary mapping column names to column definition objects
        """
        return {column_name: self.get_column_def(column_name) for column_name in self.get_columns()}

    def format_value(self, obj: models.Model, column: BaseColumn, value: Any) -> str:
        """
        Format a value for display in the table.

        Args:
            obj: The model instance being displayed
            column: The column definition
            value: The value to format

        Returns:
            Formatted value as HTML string
        """
        result = column.format_value(obj, value)

        # Check if this column should be a link
        link_columns = self.get_object_link_columns()
        is_link_column = False

        if isinstance(link_columns, str):
            is_link_column = column.attr_name == link_columns
        else:
            is_link_column = column.attr_name in link_columns

        if is_link_column:
            url = self.get_object_url(obj)
            if url:
                result = format_html('<a href="{}">{}</a>', url, result)

        return result

    def get_page_data(
        self, page: Sequence[models.Model]
    ) -> Iterator[tuple[models.Model, list[tuple[BaseColumn, str]]]]:
        """
        Get formatted page data for a table.

        Returned data is a list of tuples of (object, [(column, value), (column, value), ...]).

        Args:
            page: The page of objects to format

        Yields:
            Tuples of (object, list of (column, formatted value) pairs)
        """
        for obj in page:
            yield obj, [
                (
                    column_def,
                    self.format_value(obj, column_def, column_def.get_value(obj)),
                )
                for column_def in self.list_columns.values()
            ]

    def get_page_actions(self, *actions: Any) -> Sequence[dict[str, Any]]:
        """
        Get the actions to display on the page.

        Args:
            *actions: Additional actions to include

        Returns:
            List of action dictionaries
        """
        result = list(actions)
        if self.viewset is not None and hasattr(self.viewset, "get_list_page_actions"):
            viewset_actions = self.viewset.get_list_page_actions(self.request)
            result = list(viewset_actions) + result
        if self.page_actions:
            result = list(self.page_actions) + result
        return result

    @viewprop
    def queryset(self) -> models.QuerySet[Any] | None:
        """
        Get the queryset for this view.

        Returns:
            QuerySet instance or None if not available
        """
        if self.viewset is not None and hasattr(self.viewset, "get_queryset"):
            return self.viewset.get_queryset(self.request)
        return None

    def get_template_names(self) -> list[str]:
        """
        Return a list of template names to be used for the view.

        If `self.template_name` undefined, uses::
             [<app_label>/<model_label>_list.html,
              'material/views/list.html']

        Returns:
            List of template names to try
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                f"{opts.app_label}/{opts.model_name}{self.template_name_suffix}.html",
                "material/views/list.html",
            ]
        return [self.template_name]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Main entry point for handling requests.

        Checks permissions before processing.

        Args:
            request: The current request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response

        Raises:
            PermissionDenied: If user doesn't have permission
        """
        if not self.has_view_permission(self.request.user):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class ListModelView(
    BulkActionsMixin,
    FilterableViewMixin,
    OrderableListViewMixin,
    BaseListModelView,
):
    """
    Render a list of model objects with sorting, filtering, and bulk actions.

    This view combines several mixins to create a powerful list view with
    filtering, ordering, and bulk action capabilities.
    """

    from .search import SearchableViewMixin  # Import here to avoid circular imports
