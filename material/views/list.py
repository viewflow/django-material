import collections.abc
from typing import TYPE_CHECKING, Any, Literal, Optional, Sequence
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.paginator import Page
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic

from material.utils import DEFAULT, MARKER

if TYPE_CHECKING:
    from material.urls import BaseModelViewset
    from cursor_pagination import CursorPage


class BaseColumn:
    title: str

    def __init__(self, name: str, title: Optional[str]) -> None:
        self.name = name
        self.title = title if title else self.name.replace("_", " ").capitalize()

    def get_data(self, obj: object, viewset: Optional["BaseModelViewset"] = None) -> Any:
        raise NotImplementedError("Subclasses should override this")

    def __str__(self):
        return self.title

    def orderby(self) -> Optional[str]:
        """None if column can't be ordered"""
        return None


class Column(BaseColumn):
    """Get data from object field"""

    def __init__(
        self,
        lookup: str,
        title: Optional[str] = None,
        orderby: str = DEFAULT,  # type: ignore
    ) -> None:
        self.lookup = lookup
        self.order_by_column: str = self.lookup if orderby is DEFAULT else orderby

        name = lookup.split("__", 1)[0]
        super().__init__(name, title)

    def get_data(self, obj: object, viewset: Optional["BaseModelViewset"] = None) -> Any:
        value = obj
        for part in self.lookup.split("__"):
            value = getattr(value, part, None)
            if value is None:
                break
        return value

    def orderby(self) -> Optional[str]:
        return self.order_by_column


class RowWrapper:
    """Wrapper for a single row object that iterates over columns"""
    
    def __init__(self, obj: object, columns: Sequence[BaseColumn], viewset: Optional["BaseModelViewset"] = None):
        self.obj = obj
        self.columns = columns
        self.viewset = viewset
    
    def __iter__(self):
        """Iterate over columns and return values from column.get_data"""
        for column in self.columns:
            yield column.get_data(self.obj, self.viewset)
    
    def __getattr__(self, name):
        """Delegate attribute access to the wrapped object"""
        return getattr(self.obj, name)


class List(collections.abc.Sequence):
    """Wrap page to provide object list with desired columns"""

    def __init__(
        self,
        columns: Sequence[BaseColumn],
        page: "Page | CursorPage",
        viewset: Optional["BaseModelViewset"] = None,
    ):
        self.page = page
        self.columns = columns
        self.viewset = viewset

    def __len__(self):
        return len(self.page)

    def __getitem__(self, key):
        obj = self.page[key]
        return RowWrapper(obj, self.columns, self.viewset)


def get_ordering(columns: Sequence[BaseColumn], order_spec: Optional[str]) -> list[str]:
    """
    Builds a list of database ordering expressions based on the given order specification.

    Args:
        columns (list[BaseColumn]): A list of column objects, each with a `name` attribute and an `orderby()` method.
        order_spec (str): A comma-separated string specifying the sort order, with optional '-' for descending.
                          Example: "-created_at,name"

    Returns:
        list[str]: A list of database order expressions (e.g., ["-created_at", "name"]).
                   Only includes columns present in `columns` with a valid `orderby()` result.
    """
    if not order_spec:
        return []

    result = []
    for order in order_spec.split(","):
        field_name = order.lstrip("-")
        order_direction = "-" if order.startswith("-") else ""
        for col in columns:
            if col.name == field_name:
                db_order_column = col.orderby()
                if db_order_column is not None:
                    result.append(f"{order_direction}{db_order_column}")
                    break
    return result


class OrderableListViewMixin:
    pass


class BulkActionsMixin:
    pass


class BaseListModelView(generic.ListView):
    """Base class for list views of model objects."""

    request: HttpRequest
    viewset: Optional["BaseModelViewset"]
    model: type[models.Model]
    paginate_by: int = 50

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


@method_decorator(login_required, name="dispatch")
class ListModelView(BaseListModelView):
    """
    Render a list of model objects with sorting, filtering, and bulk actions.
    """
