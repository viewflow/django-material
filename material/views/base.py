from material.layout import Span
from material.viewset import viewprop


def _collect_elements(parent, container=None):
    if container is None:
        container = []

    if hasattr(parent, 'elements'):
        for element in parent.elements:
            _collect_elements(element, container=container)

    if isinstance(parent, Span):
        container.append(parent.field_name)

    return container


class FormLayoutMixin(object):
    """
    Mixin for FormView to infer View.fields definition from form Layout.
    """
    form_class = None
    layout = None

    @viewprop
    def fields(self):
        if self.form_class is None:
            if self.layout is not None:
                self.fields = _collect_elements(self.layout)
            else:
                self.fields = '__all__'


class Action(object):
    def __init__(self, name, url=None, icon=None):
        self.name = name
        self.url = url
        self.icon = icon
