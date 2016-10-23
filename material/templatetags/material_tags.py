import itertools
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db.models import ForeignKey
from django.template.defaulttags import NowNode
from django.utils.safestring import mark_safe
from material.config import get_config

register = template.Library()

@register.filter(name='material_conf')
def material_conf(name):
    value = get_config(name)
    return mark_safe(value) if isinstance(value, str) else value
