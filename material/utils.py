# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

import re
from collections.abc import Iterator
from typing import Any

from django.contrib import auth
from django.db import models

__all__ = ("has_object_perm", "viewprop", "DEFAULT", "first_not_default", "DEFAULT")


class MARKER:
    def __init__(self, marker: str):
        self.marker = marker

    def __iter__(self):
        return iter(())

    def __repr__(self):
        return self.marker

    def __lt__(self, other) -> bool:
        return self.marker < str(other)


DEFAULT = MARKER("DEFAULT")


def first_not_default(*args):
    """
    Return the first argument that is not the `DEFAULT` marker. If all arguments
    are `DEFAULT`, return the last one.
    """
    if not args:
        return None

    for arg in args:
        if arg is not DEFAULT:
            return arg
    return arg


def camel_case_to_underscore(name):
    """
    Convert a camel-cased string to an underscore-separated string.
    For example, 'SomeString' becomes 'some_string'.
    """

    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)).lower()


def camel_case_to_title(name):
    """
    Convert a camel-cased string to a title-cased string.
    For example, 'SomeString' becomes 'Some String'.
    """

    return re.sub(
        "([a-z0-9])([A-Z])", r"\1 \2", re.sub("(.)([A-Z][a-z]+)", r"\1 \2", name)
    ).capitalize()


def has_object_perm(user, short_perm_name, model, obj=None):
    """
    Check if the user has the specified permission for the given model. If an
    object is provided, and user has no model-wide permission, check if the user
    has the permission for that specific object instance.
    """
    perm_name = (
        f"{model._meta.app_label}.{auth.get_permission_codename(short_perm_name, model._meta)}"
    )
    has_perm = user.has_perm(perm_name)
    if not has_perm and obj is not None:
        has_perm = user.has_perm(perm_name, obj=obj)
    return has_perm


def strip_suffixes(word, suffixes):
    """
    Strip the specified suffixes from the given word.
    Never strip the whole word to an empty string.
    """

    for suffix in suffixes:
        if word != suffix and word.endswith(suffix):
            word = word[: -len(suffix)]
    return word


class viewprop:  # noqa: N801
    """
    A property that can be overridden.

    The viewprop class is a descriptor that works similarly to the built-in
    `property` decorator but allows its value to be overridden on instances
    of the class it is used in.
    """

    def __init__(self, func: Any):
        self.__doc__ = func.__doc__
        self.fget = func

    def __get__(self, obj: Any | None, objtype: type[Any] | None = None) -> Any:
        if obj is None:
            return self
        if self.fget.__name__ not in obj.__dict__:
            obj.__dict__[self.fget.__name__] = self.fget(obj)
        return obj.__dict__[self.fget.__name__]

    def __set__(self, obj: Any, value: Any) -> None:
        obj.__dict__[self.fget.__name__] = value

    def __repr__(self) -> str:
        return f"<view_property func={self.fget}>"


def get_object_data(obj: models.Model) -> Iterator[tuple[models.Field, str, Any]]:
    """
    List of object fields to display. Choice fields values are expanded to
    readable choice label.

    Returns a list of (field, label, value) tuples for the fields of the given
    object.

    """
    for field in obj._meta.fields:
        if isinstance(field, models.AutoField) or field.auto_created:
            continue
        else:
            choice_display_attr = f"get_{field.name}_display"
        if hasattr(obj, choice_display_attr):
            value = getattr(obj, choice_display_attr)()
        else:
            value = getattr(obj, field.name)

        if value is not None:
            yield (field, field.verbose_name.capitalize(), value)


PATH_PARAMETER_COMPONENT_RE = re.compile(r"<(?:(?P<converter>[^>:]+):)?(?P<parameter>[^>]+)>")


def list_path_components(route: str) -> list[str]:
    """
    Extract keyword arguments from a Django path expression, which are used as
    input parameters for a view function.

    Example Usage:

     >>> list_path_components('/prefix/<str:pk>')
     ['pk']
     >>> list_path_components('<str:pk>/<int:id>')
     ['pk', 'id']
    """
    return [match["parameter"] for match in PATH_PARAMETER_COMPONENT_RE.finditer(route)]
