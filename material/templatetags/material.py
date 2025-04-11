"""
Template tags for rendering form layouts.
"""

from django import template
from django.template.base import Node, TemplateSyntaxError

register = template.Library()


@register.tag
def render(parser, token):
    """
    Render a form using a specified layout.

    Usage: {% render form form.layout %}
    """
    bits = token.split_contents()
    if len(bits) != 3:
        raise TemplateSyntaxError(f"'{bits[0]}' tag requires two arguments")

    form_var = bits[1]
    layout_var = bits[2]

    return RenderNode(form_var, layout_var)


class RenderNode(Node):
    """Node for rendering a form with a specific layout."""

    def __init__(self, form_var, layout_var):
        self.form_var = template.Variable(form_var)
        self.layout_var = template.Variable(layout_var)

    def render(self, context):
        form = self.form_var.resolve(context)

        try:
            layout = self.layout_var.resolve(context)
        except template.VariableDoesNotExist:
            layout = None

        if layout is None:
            # If no layout is specified, render the form normally
            return form.render()

        return layout.render(form, context)
