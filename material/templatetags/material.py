"""
Template tags for rendering forms, templates, and handling viewset URLs.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

from django import template
from django.urls import NoReverseMatch
from django.utils.html import conditional_escape
from django.template.loader import get_template
from django.template.context import Context
from django.http import HttpRequest
from django.forms import Form

from material.urls.base import Viewset
from material.forms import MaterialFormRenderer

register = template.Library()


@register.simple_tag
def render(form: Form, layout: Optional[Any] = None) -> str:
    """
    Render a form using a specified layout.

    Usage:
      {% render form form.layout %}
      {% render form %}
    """
    if layout:
        return layout.render(form)

    # If no layout is specified, render the form normally
    return form.render(
        renderer=MaterialFormRenderer(),
        template_name="material/django/forms/div.html",
    )


@register.simple_tag(takes_context=True)
def reverse(context: Context, viewset: Viewset, view_name: str, *args: Any, **kwargs: Any) -> str:
    """
    Reverse a URL from a viewset.

    Example:
        {% reverse viewset 'view_name' arg1 arg2 name1=val1 name2=val2 as var %}
    """
    if viewset == "":
        return ""

    if not isinstance(viewset, Viewset):
        raise template.TemplateSyntaxError(
            f"reverse '{view_name}' first argument must be a viewset instance, got '{viewset}'"
        )

    try:
        current_app = context.request.current_app  # type: ignore
    except AttributeError:
        try:
            current_app = context.request.resolver_match.namespace  # type: ignore
        except AttributeError:
            current_app = None

    try:
        url = viewset.reverse(view_name, args=args, kwargs=kwargs, current_app=current_app)
        return url
    except NoReverseMatch:
        return ""


@register.filter
def has_perm(obj: Any, user: Any) -> bool:
    """
    Check if a user has permission to view an object.

    Example:
        {% if app|has_perm:request.user %}
    """
    if hasattr(obj, "has_view_permission"):
        return obj.has_view_permission(user)
    return True
