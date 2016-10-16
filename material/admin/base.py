from ..base import LayoutNode


class AdminReadonlyField(LayoutNode):
    """Layout wrapper node for admin read-only field."""

    template_name = 'fields/django_adminreadonlyfield.html'

    def __init__(self, fieldset_field):  # noqa D102
        self.fieldset_field = fieldset_field

    def get_context_data(self, context):  # noqa D102
        return {'fieldset_field': self.fieldset_field}


class Inline(LayoutNode):
    """Leayout wrapper node for admin inline."""

    def __init__(self, inline, **kwargs):  # noqa D102
        self.inline = inline
        self.span_columns = kwargs.pop('span_columns', 1)

    @property
    def template_name(self):  # noqa D102
        return self.inline.opts.template
