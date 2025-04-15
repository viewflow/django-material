# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.
from __future__ import annotations

import copy
import types
import warnings
from collections import OrderedDict, namedtuple
from typing import Any

from django.urls import ResolverMatch, URLPattern, URLResolver, include, path, reverse
from django.urls.resolvers import RoutePattern
from django.views.generic import RedirectView

from material.utils import (
    DEFAULT,
    camel_case_to_underscore,
    list_path_components,
    strip_suffixes,
)


class _UrlName(str):
    """
    A string wrapper that maintains additional metadata.

    Used to keep a reference over django URL resolve calling
    hierarchy by attaching extra context data.
    """

    def __new__(cls, value: str) -> _UrlName:
        instance = super().__new__(cls, value)
        instance.extra: dict[str, Any] = {}
        return instance


class _URLResolver(URLResolver):
    """
    Custom URL resolver that maintains extra metadata in the resolution process.

    This extends Django's URLResolver to track and propagate additional context
    information during the URL resolution process.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.extra: dict[str, Any] = kwargs.pop("extra", {})
        super().__init__(*args, **kwargs)

    def resolve(self, *args: Any, **kwargs: Any) -> ResolverMatch:
        result = super().resolve(*args, **kwargs)

        # Convert url_name to our wrapper class if needed
        if not isinstance(result.url_name, _UrlName):
            result.url_name = _UrlName(str(result.url_name) if result.url_name else "")

        # Merge extras from resolver and result
        merged_extra: dict[str, Any] = {}
        merged_extra.update(self.extra)
        merged_extra.update(result.url_name.extra)
        result.url_name.extra = merged_extra

        return result


class Route(namedtuple("Route", ["prefix", "viewset"])):
    """
    Represents a URL route with a prefix and a viewset.

    Attributes:
        prefix (str): The URL prefix for the route
        viewset (BaseViewset): The viewset instance that handles this route
    """

    pass


def route(prefix: str, viewset: BaseViewset) -> Route:
    """
    Create a route mapping a URL prefix to a viewset.

    Args:
        prefix (str): The URL prefix for the route
        viewset (BaseViewset): The viewset to attach to the route

    Returns:
        Route: A new Route instance

    Raises:
        ValueError: If viewset is not a BaseViewset instance
    """
    if not isinstance(viewset, BaseViewset):
        raise ValueError(
            f"route(...) second argument should be a viewset instance, got {type(viewset)} instead"
        )
    return Route(prefix, viewset)


class BaseViewset:
    """
    Base class for defining a class-based Django routing configuration.

    This provides the core functionality for defining URL routing in a class-based
    manner. It manages parent-child relationships between viewsets and provides
    utilities for resolving and generating URLs with proper namespacing.

    Attributes:
        app_name (Optional[str]): The name of the application associated with this viewset.
        namespace (Optional[str]): The namespace for the URLs of this viewset.
        parent_namespace (Optional[str]): The namespace of the parent viewset.
        extra_kwargs (Optional[Dict[str, Any]]): Additional keyword arguments for URL configuration.
    """

    app_name: str | None = None
    namespace: str | None = None
    parent_namespace: str | None = None
    extra_kwargs: dict[str, Any] | None = None

    def __init__(self) -> None:
        super().__init__()
        self._parent: BaseViewset | None = None

    @property
    def parent(self) -> BaseViewset | None:
        """
        Get the parent viewset.

        Returns:
            Optional[BaseViewset]: The parent viewset, if any.
        """
        return self._parent

    @parent.setter
    def parent(self, value: BaseViewset) -> None:
        """
        Set the parent viewset. This can only be set once.

        Args:
            value (BaseViewset): The viewset to set as the parent.

        Raises:
            Warning: If the parent is being set more than once or if the viewset
                     already has an explicit parent namespace.
        """
        if self._parent is not None:
            warnings.warn(
                f"Viewset {self.__class__.__name__} parent could be set only once",
                Warning,
                stacklevel=2,
            )
        if self.parent_namespace is not None:
            warnings.warn(
                f"Viewset {self.__class__.__name__} already has explicit parent namespace",
                Warning,
                stacklevel=2,
            )
        self._parent = value

    @property
    def urls(self) -> tuple[list[URLResolver], str | None, str | None]:
        """
        Get the URL patterns, app name, and namespace for this viewset.

        This method must be implemented by subclasses.

        Returns:
            tuple: A tuple containing:
                - list[URLResolver]: The URL resolvers for this viewset
                - Optional[str]: The app name
                - Optional[str]: The namespace

        Raises:
            NotImplementedError: If not implemented by a subclass
        """
        raise NotImplementedError("Subclass must override this")

    def reverse(
        self,
        viewname: str,
        args: list[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
        current_app: str | None = None,
    ) -> str:
        """
        Get the URL for a given viewname, including the namespace.

        This method constructs a namespaced URL name by traversing up the viewset
        hierarchy and prepending the appropriate namespaces.

        Args:
            viewname (str): The name of the view.
            args (Optional[list[Any]]): Positional arguments for the view.
            kwargs (Optional[Dict[str, Any]]): Keyword arguments for the view.
            current_app (Optional[str]): The current application namespace.

        Returns:
            str: The URL for the view with the appropriate namespace
        """
        view_namespace = ""

        current_viewset: BaseViewset | None = self
        while current_viewset:
            namespace = current_viewset.namespace or current_viewset.app_name
            if namespace:
                view_namespace = f"{namespace}:{view_namespace}"
            if current_viewset.parent is None and current_viewset.parent_namespace:
                view_namespace = f"{current_viewset.parent_namespace}:{view_namespace}"
            current_viewset = current_viewset.parent

        if view_namespace:
            viewname = view_namespace + viewname

        return reverse(viewname, args=args, kwargs=kwargs, current_app=current_app)

    def has_view_permission(self, user: Any, obj: Any | None = None) -> bool:
        """
        Determine if the user has permission to view the viewset.

        This method can be overridden by subclasses to implement custom
        permission checks.

        Args:
            user (Any): The user to check permissions for.
            obj (Optional[Any]): The object being viewed, if applicable.

        Returns:
            bool: True if the user has view permission, False otherwise.
        """
        return True


class ViewsetMeta(type):
    """
    Metaclass that collects URL patterns declared on viewset classes.

    This metaclass collects all attributes ending with '_path' (excluding those
    starting with 'get_') from the class and its base classes, handling inheritance
    correctly. It enforces the proper override behavior where subclass paths
    take precedence over parent class paths.
    """

    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> type:
        # Collect URL patterns from current class
        current_patterns: list[tuple[str, Any]] = []
        for key, value in list(attrs.items()):
            if not key.endswith("_path") or key.startswith("get_"):
                continue
            current_patterns.append((key, value))

        # Initialize with empty dict - will be populated after class creation
        attrs["declared_patterns"] = OrderedDict()

        new_class = super().__new__(mcs, name, bases, attrs)

        # Walk through the MRO to collect patterns from base classes
        declared_patterns = OrderedDict()
        for base in reversed(new_class.__mro__):
            # Collect patterns from base class
            if hasattr(base, "declared_patterns"):
                declared_patterns.update(base.declared_patterns)

            # Handle attribute shadowing (None value removes inherited pattern)
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_patterns:
                    declared_patterns.pop(attr)

        # Give precedence to current class patterns over inherited patterns
        new_class.declared_patterns = OrderedDict(current_patterns)
        new_class.declared_patterns.update(
            {
                key: value
                for key, value in declared_patterns.items()
                if key not in dict(current_patterns)
            }
        )

        return new_class


class Viewset(BaseViewset, metaclass=ViewsetMeta):
    """
    Declarative, class-based Django routing configuration.

    A Viewset class automatically collects URL patterns from class attributes
    with names ending in '_path' and includes nested Viewset classes from
    attributes with names specified in the viewsets list.

    Viewset classes can be inherited, extended, and have overridden attributes.
    Subclass patterns take precedence over parent class patterns.

    Attributes:
        viewsets (Optional[list[BaseViewset]]): Additional viewsets to include
        turbo_disabled (bool): Flag to disable turbo features
        urlpatterns (Optional[list]): Additional URL patterns to include
        declared_patterns (OrderedDict): Collected URL patterns (set by metaclass)
    """

    viewsets: list[BaseViewset] | None = None
    turbo_disabled: bool = False
    urlpatterns: list[URLPattern | URLResolver | Route] | None = None

    def __init__(self, **initkwargs: Any) -> None:
        """
        Initialize a viewset instance with optional configuration.

        Args:
            **initkwargs: Keyword arguments to override class attributes

        Raises:
            TypeError: If an invalid keyword argument is provided
        """
        super().__init__()
        self._urls_cache: list[URLPattern | URLResolver] | None = None
        self._children: list[BaseViewset] = []

        # Customize instance attributes
        for key, value in initkwargs.items():
            if key.startswith("_"):
                raise TypeError(
                    f"You tried to pass the private {key} name as a "
                    f"keyword argument to {self.__class__.__name__}(). Don't do that."
                )
            if not hasattr(self.__class__, key):
                raise TypeError(
                    f"{self.__class__.__name__}() received an invalid keyword {key}. "
                    f"Viewset constructor only accepts arguments that are already "
                    f"attributes of the class."
                )
            setattr(self, key, value)

        # Clone additional routes from viewsets
        if self.viewsets:
            self.viewsets = [copy.copy(viewset) for viewset in self.viewsets]
            self._children.extend(self.viewsets)

        # Clone route instances from declared patterns
        for attr_name in self.declared_patterns:
            attr_value = getattr(self.__class__, attr_name)
            if isinstance(attr_value, Route):
                viewset = copy.copy(attr_value.viewset)
                viewset.extra_kwargs = list_path_components(attr_value.prefix)
                setattr(self, attr_name, Route(attr_value.prefix, viewset))
                self._children.append(viewset)

    def _create_url_pattern(self, value: Any) -> URLPattern | URLResolver:
        """
        Convert a value to a URLPattern or URLResolver.

        Args:
            value: The value to convert (URLPattern, URLResolver, or Route)

        Returns:
            Union[URLPattern, URLResolver]: The resulting URL pattern

        Raises:
            ValueError: If the value is not a valid URL entry
        """
        if isinstance(value, URLPattern | URLResolver):
            return value
        elif isinstance(value, Route):
            value.viewset.parent = self
            patterns, app_name, namespace = value.viewset.urls
            pattern = path(
                value.prefix if value.prefix else "",
                include((patterns, app_name), namespace=namespace),
            )
            return pattern
        else:
            raise ValueError(
                f"{self.__class__.__name__} got unknown url entry: {value} (type: {type(value)})"
            )

    def _get_urls(self) -> list[URLPattern | URLResolver]:
        """
        Collect URLs from the instance attributes.

        Returns:
            list[Union[URLPattern, URLResolver]]: List of URL patterns
        """
        urlpatterns: list[URLPattern | URLResolver] = []

        # URL overrides from urlpatterns attribute
        for url_entry in self.urlpatterns or []:
            urlpatterns.append(self._create_url_pattern(url_entry))

        # Class attributes (declared_patterns)
        for attr_name in self.declared_patterns:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, types.FunctionType) or attr_value is None:
                continue
            urlpatterns.append(self._create_url_pattern(attr_value))

        # Additional routes from viewsets list
        for viewset in self.viewsets or []:
            if viewset.app_name is None:
                # Generate app_name from class name if not provided
                viewset.app_name = camel_case_to_underscore(
                    strip_suffixes(
                        viewset.__class__.__name__,
                        ["App", "Application", "Viewset", "Admin", "Flow"],
                    )
                )
                assert viewset.app_name, f"Can't provide auto name for {viewset.__class__.__name__}"
            urlpatterns.append(self._create_url_pattern(route(f"{viewset.app_name}/", viewset)))

        return urlpatterns

    def _get_resolver_extra(self) -> dict[str, Any]:
        """
        Get extra data to be attached to the URL resolver.

        Returns:
            Dict[str, Any]: Extra data for the resolver
        """
        return {"viewset": self}

    def filter_kwargs(self, view_class: type, **kwargs: Any) -> dict[str, Any]:
        """
        Filter keyword arguments to only those applicable to the view class.

        Args:
            view_class: The view class to filter kwargs for
            **kwargs: Keyword arguments to filter

        Returns:
            Dict[str, Any]: Filtered keyword arguments
        """
        return {
            name: value
            for name, value in kwargs.items()
            if hasattr(view_class, name) and value is not DEFAULT
        }

    @property
    def urls(self) -> tuple[list[URLResolver], str | None, str | None]:
        """
        Get the URL patterns, app name, and namespace for this viewset.

        Returns:
            tuple: A tuple containing:
                - list[URLResolver]: The URL resolvers for this viewset
                - Optional[str]: The app name
                - Optional[str]: The namespace
        """
        namespace = self.namespace
        if namespace is None:
            namespace = self.app_name

        if self._urls_cache is None:
            self._urls_cache = self._get_urls()

        pattern = RoutePattern("", is_endpoint=False)
        resolver = _URLResolver(pattern, self._urls_cache, extra=self._get_resolver_extra())
        return [resolver], self.app_name, namespace


def _get_index_redirect_url(viewset: BaseViewset) -> str | None:
    """
    Return the first non-parameterized viewset URL.

    Args:
        viewset (BaseViewset): The viewset to find an index URL for

    Returns:
        Optional[str]: The URL path for redirection, or None if no suitable URL found
    """

    def _get_index_url(url_patterns: list[Any], prefix: str = "./") -> str | None:
        """
        Recursively search for a suitable index URL in the URL patterns.

        Args:
            url_patterns: List of URL patterns to search
            prefix: Current URL prefix

        Returns:
            Optional[str]: The URL path for redirection, or None if no suitable URL found
        """
        # Sort to prioritize patterns with name != "index"
        index_first_patterns = sorted(
            url_patterns, key=lambda pat: getattr(pat, "name", "") != "index"
        )

        for url_pattern in index_first_patterns:
            if isinstance(url_pattern, URLPattern):
                # Check if this pattern could be a suitable index view
                is_suitable_index = (
                    isinstance(url_pattern.pattern, RoutePattern)
                    and url_pattern.pattern.converters == {}  # No URL parameters
                    and not (
                        hasattr(url_pattern.callback, "view_class")
                        and url_pattern.callback.view_class == _IndexRedirectView
                    )  # Not a redirect view itself
                )

                if is_suitable_index:
                    return prefix + url_pattern.pattern._route

            elif isinstance(url_pattern, URLResolver) and isinstance(
                url_pattern.pattern, RoutePattern
            ):
                # Recursively check patterns in nested resolvers
                nested_index = _get_index_url(
                    url_pattern.url_patterns, prefix + url_pattern.pattern._route
                )
                if nested_index:
                    return nested_index

        return None

    return _get_index_url(viewset.urls[0], "./")


class _IndexRedirectView(RedirectView):
    """
    A view that redirects to the first suitable URL pattern in a viewset.

    This is used to implement automatic redirects from the root URL of a viewset
    to a suitable default view within that viewset.
    """

    viewset: BaseViewset | None = None

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        """
        Get the URL to redirect to.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Optional[str]: The URL to redirect to

        Raises:
            ValueError: If no suitable redirect URL can be found
        """
        if self.viewset:
            redirect = _get_index_redirect_url(self.viewset)
            if redirect is None:
                raise ValueError(
                    "Can't determine index URL. Please add an explicit "
                    "`index_path = path('', RedirectView(url='...'), name='index')` "
                    "declaration for the viewset."
                )
            return redirect
        return super().get_redirect_url(*args, **kwargs)


class IndexViewMixin(metaclass=ViewsetMeta):
    """
    A mixin that adds automatic redirection from the root URL to the first suitable view.

    When a viewset uses this mixin, accessing the root URL of the viewset will
    automatically redirect to the first non-parameterized view defined in the viewset.
    """

    @property
    def index_path(self) -> URLPattern:
        """
        Create a URL pattern that redirects from the root URL to a suitable default view.

        Returns:
            URLPattern: A URL pattern for the root URL that redirects to a suitable view
        """
        return path("", _IndexRedirectView.as_view(viewset=self), name="index")
