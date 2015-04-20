import re
from django.forms.forms import BoundField
from django.template.base import Library, Node, TemplateSyntaxError, Variable, token_kwargs
from django.utils import formats
from django.utils.encoding import force_text

from ..base import Field
from .material_form import FormPartNode, _render_parts


register = Library()


@register.tag('render')
class FormRenderNode(Node):
    def __init__(self, parser, token):
        bits = token.split_contents()

        if len(bits) == 0:
            raise TemplateSyntaxError(
                "%r received invalid args, expected one element for render. Got: %r" %
                (bits[0], bits[1:]))

        remaining_bits = bits[2:]

        self.kwargs = token_kwargs(remaining_bits, parser)

        if remaining_bits:
            raise TemplateSyntaxError("%r received an invalid token: %r" %
                                      (bits[0], remaining_bits[0]))

        for key in self.kwargs:
            if key not in ('template', 'widget'):
                raise TemplateSyntaxError("%r received an invalid key: %r" %
                                          (bits[0], key))

            self.kwargs[key] = self.kwargs[key]

        self.nodelist = parser.parse(('end{}'.format(bits[0]),))
        parser.delete_first_token()

        self.element = Variable(bits[1])

    def render(self, context):
        element = self.element.resolve(context)

        options = {}
        for key, value in self.kwargs.items():
            options[key] = value.resolve(context)

        # render inner parts
        children = (node for node in self.nodelist if isinstance(node, FormPartNode))
        _render_parts(context, children)

        # render element
        if isinstance(element, BoundField):
            return Field(element.name).render(context, **options)
        elif hasattr(element, 'render'):
            with context.push(parent=element):
                return element.render(context, **options)
        else:
            raise TemplateSyntaxError("form_render can't render %r" % (element, ))


@register.tag('tagattrs')
class TagAttrsNode(Node):
    def __init__(self, parser, token):
        bits = token.split_contents()
        self.nodelist = parser.parse(('end{}'.format(bits[0]),))
        parser.delete_first_token()

    def render(self, context):
        """
        Remove empty attributes and newlines
        """
        value = self.nodelist.render(context)
        value = re.sub('\w+=\"\s*\"', '', value)
        return re.sub('[\n ]+', ' ', value).strip()


@register.filter
def multiwidget_value(bound_field, pos):
    value = bound_field.value()
    if not isinstance(value, (list, tuple)):
        value = bound_field.field.widget.decompress(value)
    return value[pos]


@register.filter
def jquery_datepicker_format(field):
    input_format = field.input_formats[0]

    # %a, %A, %z, %f %Z %j %U %W %c %x %X unsupported

    subst = {
        '%d': 'd',    # Day of the month as a zero-padded decimal number
        '%b': 'M',    # Month as locale's abbreviated name
        '%B': 'F',    # Month as locale's full name
        '%m': 'm',    # Month as a zero-padded decimal number
        '%y': 'y',    # Year without century as a zero-padded decimal number
        '%Y': 'Y',    # Year with century as a decimal number
        '%H': 'H',    # Hour (24-hour clock) as a zero-padded decimal number
        '%I': 'h',    # Hour (12-hour clock) as a zero-padded decimal number
        '%p': 'a',    # Locale's equivalent of either AM or PM
        '%M': 'i',    # Minute as a zero-padded decimal number
        '%S': 's',    # Second as a zero-padded decimal number
        '%%': '%'     # A literal '%' character
    }

    return re.sub('|'.join(re.escape(key) for key in subst.keys()),
                  lambda k: subst[k.group(0)], input_format)


@register.filter
def datepicker_value(value, date_format):
    return formats.localize_input(value, date_format)


@register.filter('force_text')
def force_text_impl(value):
    return force_text(value)
