from django.contrib import auth

from material.layout import Span
from material.viewset import viewprop


def _collect_elements(parent, container=None):
    if container is None:
        container = []

    if hasattr(parent, 'children'):
        for element in parent.children:
            _collect_elements(element, container=container)

    if isinstance(parent, Span):
        container.append(parent.field_name)

    return container


def has_object_perm(user, short_perm_name, model, obj=None):
    perm_name = auth.get_permission_codename(short_perm_name, model._meta)
    has_perm = user.has_perm(perm_name)
    if not has_perm and obj is not None:
        has_perm = user.has_perm(perm_name, obj=obj)
    return has_perm


class FormLayoutMixin(object):
    """
    Mixin for FormView to infer View.fields definition from form Layout.
    """
    form_class = None

    @viewprop
    def layout(self):
        if self.form_class is None and hasattr(self.form_class, 'layout'):
            return self.form_class.layout

    @viewprop
    def fields(self):
        if self.form_class is None:
            if self.layout is not None:
                return _collect_elements(self.layout)
            else:
                return '__all__'


class Action(object):
    def __init__(self, name, url=None, icon=None):
        self.name = name
        self.url = url
        self.icon = icon
