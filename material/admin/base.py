from ..base import LayoutNode


class AdminReadonlyField(LayoutNode):
    template_name = 'fields/django_adminreadonlyfield.html'

    def __init__(self, fieldset_field):
        self.fieldset_field = fieldset_field

    def get_context_data(self, context):
        return {'fieldset_field': self.fieldset_field}


class TabularInline(LayoutNode):
    template_name = 'inlines/tabular.html'

    def __init__(self, inline, **kwargs):
        self.inline = inline
        self.span_columns = kwargs.pop('span_columns', 1)
