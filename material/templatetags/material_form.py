from django import forms, template

from material.layout import Layout
from material.settings import material_settings

register = template.Library()


@register.tag('material')
class MaterialFormNode(template.Node):
    """
    Render a django form using google material-components-web library.

    Example:

        {% material form [layout] %}
    """
    def __init__(self, parser, token):
        bits = token.split_contents()

        layout_expr = None
        if len(bits) == 2:
            tag, form_expr = bits
        elif len(bits) == 3:
            tag, form_expr, layout_expr = bits
        else:
            raise template.TemplateSyntaxError(
                "Invalid syntax in material tag, expects only form and optional layout arguments.")

        self.form_expr = parser.compile_filter(form_expr)
        self.layout_expr = parser.compile_filter(layout_expr) if layout_expr else None

    def render(self, context):
        form = self.form_expr.resolve(context)
        if not isinstance(form, forms.BaseForm):
            raise template.TemplateSyntaxError("material tag first argument must be a form")

        layout = None
        if self.layout_expr:
            layout = self.layout_expr.resolve(context)
        if layout and not isinstance(layout, Layout):
            raise template.TemplateSyntaxError("material tag second argument must be a layout")

        renderer = material_settings.FORM_RENDERER(form, layout)
        return str(renderer)
