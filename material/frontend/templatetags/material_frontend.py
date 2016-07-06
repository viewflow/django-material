from django.db import models
from django.template import Library


register = Library()


@register.filter
def frontend_urlname(model, url_type):
    return '{}:{}_{}'.format(model._meta.app_label, model._meta.model_name, url_type)


@register.filter
def verbose_name(obj):
    if isinstance(obj, models.Model):
        type(obj)._meta.verbose_name
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    if isinstance(obj, models.Model):
        type(obj)._meta.verbose_name_plural
    return obj._meta.verbose_name_plural
