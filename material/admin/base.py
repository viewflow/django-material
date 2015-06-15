from ..base import LayoutNode


class AdminReadonlyField(LayoutNode):
    template_name = 'fields/django_adminreadonlyfield.html'

    def __init__(self, fieldset_field):
        self.fieldset_field = fieldset_field

    def get_context_data(self, context):
        return {'fieldset_field': self.fieldset_field}
