from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.db.models import Model, QuerySet
    from django.http import HttpRequest

from django_filters.filterset import filterset_factory


class FilterableViewMixin:
    """
    A mixin that provides a way to show and handle a FilterSet in a request.
    """

    filterset_class: Any = None
    filterset_initial: dict[str, Any] | None = None
    filter_fields: list[str] | None = None
    strict_filter: bool = False
    model: type[Model]  # Provided by concrete view class
    viewset: Any = None  # Provided by concrete view class
    request: HttpRequest  # Provided by concrete view class

    def get_filterset_class(self) -> type[Any] | None:
        """
        Returns the filterset class to use in this view
        """
        if self.filterset_class:
            return self.filterset_class
        elif self.filter_fields:
            return filterset_factory(model=self.model, fields=self.filter_fields)  # type: ignore
        return None

    def get_filterset_kwargs(self, filterset_class: type[Any]) -> dict[str, Any]:
        """
        Returns the keyword arguments for instantiating the filterset.
        """
        kwargs: dict[str, Any] = {}

        if self.viewset is not None and hasattr(self.viewset, "get_filterset_kwargs"):  # type: ignore
            kwargs = self.viewset.get_filterset_kwargs(self.request)  # type: ignore

        # filterset initial
        data = self.request.GET or None  # type: ignore
        if self.filterset_initial:
            if data is None:
                data = self.filterset_initial
            else:
                data = data.copy()
                for key, value in (self.filterset_initial or {}).items():
                    if key not in data:
                        if isinstance(value, (list, tuple, set)):
                            data.setlist(key, value)
                        else:
                            data[key] = value

        return {
            **kwargs,
            "data": data,
            "request": self.request,  # type: ignore
        }

    def get_filterset(self, filterset_class: type[Any], queryset: QuerySet[Any]) -> Any:
        """
        Returns an instance of the filterset to be used in this view.
        """
        kwargs = self.get_filterset_kwargs(filterset_class)
        return filterset_class(queryset=queryset, **kwargs)

    def is_strict_filter(self) -> bool:
        return self.strict_filter

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()  # type: ignore
        self.filterset, filterset_class = None, self.get_filterset_class()
        if filterset_class is not None:
            self.filterset = self.get_filterset(filterset_class, queryset=queryset)
            if self.filterset.is_valid() or not self.is_strict_filter():
                queryset = self.filterset.qs
            else:
                queryset = self.filterset.queryset.none()
        return queryset
