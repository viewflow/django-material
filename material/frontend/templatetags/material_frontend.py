from django.db import models
from django.template import Library, TemplateSyntaxError

from ..urlconf import frontend_url


register = Library()


@register.filter
def frontend_urlname(model, url_type):
    """
    Retrieve URL for a model.

    Suitable for use with {% url %} template tag

    Example::

        {% url view.model|frontend_urlname:'list' %}
        {% url view.model|frontend_urlname:'detail' object.pk %}

    """
    return '{}:{}_{}'.format(model._meta.app_label, model._meta.model_name, url_type)


@register.filter
def verbose_name(obj):
    """Return model verbose name."""
    if isinstance(obj, models.Model):
        type(obj)._meta.verbose_name
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    """Return model verbose name in plural mode."""
    if isinstance(obj, models.Model):
        type(obj)._meta.verbose_name_plural
    return obj._meta.verbose_name_plural


@register.filter
def query_back(request, back_link=None):
    """
    Set the `back` url GET parameter.

    Usage::

        <a href="{{ url }}?{{ request|query_back:"here" }}>
        <a href="{{ url }}?{{ request|query_back:"here_if_none" }}>
    """
    if back_link is not None and back_link not in ['here', 'here_if_none']:
        raise TemplateSyntaxError(
            "query_back tag accepts `here`, or `here_if_none` as parameter. Got {}".format(back_link))

    return frontend_url(request, back_link=back_link)
