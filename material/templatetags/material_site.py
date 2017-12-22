import re

from django import template
from django.db import models
from django.urls import NoReverseMatch
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from material import Viewset


register = template.Library()


KWARG_RE = re.compile(r"(?:(\w+)=)?(.+)")


@register.tag('viewset_url')
class ViewsetURLNode(template.Node):
    """
    Revers url for a view from viewset

    Example::
        {% viewset_url viewset viewname args kwargs %}
    """

    def __init__(self, parser, token):
        bits = token.split_contents()
        if len(bits) < 2:
            raise template.TemplateSyntaxError(
                "viewset_url takes at least two arguments, a "
                "viewset and the name of a url.")

        self.viewset = parser.compile_filter(bits[1])
        self.view_name = parser.compile_filter(bits[2])

        self.args = []
        self.kwargs = {}
        self.variable_name = None
        bits = bits[3:]
        if len(bits) >= 2 and bits[-2] == 'as':
            self.variable_name = bits[-1]
            bits = bits[:-2]

        if len(bits):
            for bit in bits:
                match = KWARG_RE.match(bit)
                if not match:
                    raise template.TemplateSyntaxError("Malformed arguments to viewset_url tag")
                name, value = match.groups()
                if name:
                    self.kwargs[name] = parser.compile_filter(value)
                else:
                    self.args.append(parser.compile_filter(value))

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = {
            force_text(key, 'ascii'): value.resolve(context)
            for key, value in self.kwargs.items()
        }

        viewset = self.viewset.resolve(context)
        if not isinstance(viewset, Viewset):
            raise template.TemplateSyntaxError("viewset_url first argument must be a viewset instance")

        view_name = self.view_name.resolve(context)

        try:
            current_app = context.request.current_app
        except AttributeError:
            try:
                current_app = context.request.resolver_match.namespace
            except AttributeError:
                current_app = None

        url = ''
        try:
            url = viewset.reverse(view_name, args=args, kwargs=kwargs, current_app=current_app)
        except NoReverseMatch:
            if self.variable_name is None:
                raise

        if self.variable_name:
            context[self.variable_name] = url
            return ''
        else:
            if context.autoescape:
                url = conditional_escape(url)
            return url


@register.filter
def has_perm(app, user):
    """
    Check a user access rights for an application

    Example:

        {% if request.resolver_match.app|has_perm:request.user %}
            {% include app.menu_template_name app=request.resolver_match.app only %}
        {% endif %}
    """
    return app.has_perm(user)


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
def list_page_data(page, list_view):
    """Formated page data for a table.

       Returned data is a list of list of cell values zipped with column definitions.
       [[(column, value), (column, value), ...], ...]
    """
    return list_view.get_page_data(page)
