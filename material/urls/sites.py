# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

from django.urls import NoReverseMatch
from django.utils.functional import cached_property

from material.utils import camel_case_to_title, strip_suffixes

from .base import IndexViewMixin, Viewset

T = TypeVar("T")


class AppMenuMixin:
    """A route that can be listed in an Application menu."""

    title: str | None = None
    icon: str = "view_carousel"

    def __getattribute__(self, name: str) -> Any:
        attr = super().__getattribute__(name)

        if name == "title" and attr is None:
            class_title = camel_case_to_title(
                strip_suffixes(self.__class__.__name__, ["Viewset", "Admin", "App", "Flow"])
            )
            if not class_title:
                raise ValueError("Application item needs a title")
            return class_title + "s"

        return attr

    def has_view_permission(self, user: Any, obj: Any | None = None) -> bool:
        parent_class = super()
        if hasattr(parent_class, "has_view_permission"):
            # Use type ignore because the parent might not be correctly typed
            return parent_class.has_view_permission(user, obj=obj)  # type: ignore
        return True


class Application(IndexViewMixin, Viewset):
    title: str = ""
    icon: str = "view_module"
    menu_template_name: str = "material/includes/app_menu.html"
    base_template_name: str = "material/base_page.html"
    permission: str | Callable[[Any], bool] | None = None

    def __getattribute__(self, name: str) -> Any:
        attr = super().__getattribute__(name)

        if name == "title" and attr is not None and not attr:
            title = camel_case_to_title(
                strip_suffixes(
                    self.__class__.__name__,
                    ["Application", "Viewset", "Admin", "App", "Flow"],
                )
            )
            if not title:
                raise ValueError("Application needs a title")
            return title

        return attr

    def _get_resolver_extra(self) -> dict[str, Any]:
        return {"viewset": self, "app": self}

    def get_context_data(self, request: Any) -> dict[str, Any]:
        return {}

    def has_view_permission(self, user: Any, obj: Any | None = None) -> bool:
        if self.permission is not None:
            if callable(self.permission):
                return self.permission(user)
            return user.is_authenticated and user.has_perm(self.permission)
        return True

    def menu_items(self) -> Iterator[AppMenuMixin]:
        for viewset in self._children:
            if isinstance(viewset, AppMenuMixin):
                yield viewset


class Site(IndexViewMixin, Viewset):
    title: str | None = None
    icon: str = "view_comfy"
    menu_template_name: str = "material/includes/site_menu.html"
    primary_color: str | None = None
    secondary_color: str | None = None
    permission: str | None = None

    def __init__(self, *, title: str | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if title is not None:
            self.title = title

        if self.title is None:
            # pluralize class name
            self.title = camel_case_to_title(strip_suffixes(self.__class__.__name__, ["Site"]))
            if not self.title:
                self.title = "Django Viewflow"

    def __getattribute__(self, name: str) -> Any:
        attr = super().__getattribute__(name)

        if name == "title" and attr is None:
            title = camel_case_to_title(strip_suffixes(self.__class__.__name__, ["Site"]))
            if not title:
                title = "Django Viewflow"
            return title

        return attr

    def _get_resolver_extra(self) -> dict[str, Any]:
        return {"viewset": self, "site": self}

    def menu_items(self) -> Iterator[Site | Application]:
        for viewset in self._children:
            if isinstance(viewset, Site | Application):
                yield viewset

    def has_view_permission(self, user: Any, obj: Any | None = None) -> bool:
        if self.permission is not None:
            return user.has_perm(self.permission)
        return True

    def register(self, app_class: type[T]) -> type[T]:
        app = app_class()
        app._parent = self  # type: ignore

        # Initialize viewsets if not already done
        if getattr(self, "viewsets", None) is None:
            self.viewsets = []

        self.viewsets.append(app)  # type: ignore
        return app_class

    @cached_property
    def _viewset_models(self) -> dict[Any, Any]:
        result: dict[Any, Any] = {}

        queue = list(self._children)
        while queue:
            viewset = queue.pop(0)
            if (
                hasattr(viewset, "model")
                and hasattr(viewset, "get_object_url")
                and viewset.model not in result
            ):
                result[viewset.model] = viewset

            # Use getattr to access _children since some types might not have it defined
            children = getattr(viewset, "_children", [])
            for child_viewset in children:
                if isinstance(child_viewset, Viewset):
                    queue.append(child_viewset)
        return result

    def get_absolute_url(self, request: Any, obj: Any) -> str:
        model = type(obj)
        if model in self._viewset_models:
            viewset = self._viewset_models[model]
            # We know get_object_url exists because we checked in _viewset_models
            return viewset.get_object_url(request, obj)  # type: ignore
        else:
            raise NoReverseMatch(f"Viewset for {model.__name__} not found")
