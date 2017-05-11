from __future__ import division

import math
import re
from collections import OrderedDict

from django.db.models.query import QuerySet
from django.forms.forms import BoundField
from django.template import Library
from django.template.base import (
    Node, TemplateSyntaxError, Variable, token_kwargs
)
from django.utils import formats
from django.utils.encoding import force_text

from ..base import Field
from ..widgets import SelectDateWidget
from .material_form import FormPartNode, WidgetAttrNode, _render_parts


register = Library()


@register.tag('render')
class FormRenderNode(Node):
    """Sugar for element in template rendering."""

    def __init__(self, parser, token):  # noqa D102
        bits = token.split_contents()

        if len(bits) == 0:
            raise TemplateSyntaxError(
                "%r received invalid args, expected one element for render."
                " Got: %r".format(bits[0], bits[1:])
            )

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

    def render(self, context):  # noqa D102
        element = self.element.resolve(context)

        options = {}
        for key, value in self.kwargs.items():
            options[key] = value.resolve(context)

        # render inner parts
        children = (
            node for node in self.nodelist
            if isinstance(node, FormPartNode)
        )
        _render_parts(context, children)

        attrs = (
            node for node in self.nodelist
            if isinstance(node, WidgetAttrNode)
        )
        for attr in attrs:
            attr.render(context)

        # render element
        if isinstance(element, BoundField):
            return Field(element.name).render(context, **options)
        elif hasattr(element, 'render'):
            with context.push(parent=element):
                return element.render(context, **options)
        else:
            raise TemplateSyntaxError(
                "form_render can't render %r".format(element)
            )


@register.filter
def multiwidget_value(bound_field, pos):
    """Subwidget value for MultiWidget."""
    value = bound_field.value()
    if not isinstance(value, (list, tuple)):
        value = bound_field.field.widget.decompress(value)
    return value[pos]


@register.filter
def have_default_choice(field):
    """Handle special case for SelectMultiple widget."""
    return [
        choice
        for choice, _ in field.widget.choices
        if choice is None or choice == ""
    ]


@register.filter
def jquery_datepicker_format(field):
    """Convert django input format to jquery datepicket format."""
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
    """Return localized date value."""
    return formats.localize_input(value, date_format)


@register.filter('force_text')
def force_text_impl(value):
    """Coerce widget value to text."""
    return force_text(value)


@register.filter
def split_choices_by_columns(choices, columns):
    """Split CheckboxSelectMultiple values into columns."""
    columns = int(columns)
    col_span = 12 // columns
    per_column = int(math.ceil(len(choices) / columns))
    choices = [tuple(choice) + (i,) for i, choice in enumerate(choices)]
    return [
        (col_span, choices[i:i + per_column])
        for i in range(0, len(choices), per_column)
    ]


@register.filter
def select_date_widget_wrapper(bound_field):
    """Wrap SelectDateWidget into django-material internal wrapper."""
    class Wrapper(object):
        def __init__(self, bound_field):
            self.bound_field = bound_field

        @property
        def selects(self):
            widget = SelectDateWidget(self.bound_field.field.widget)
            for data in widget.selects_data(self.bound_field.value()):
                yield data

    return Wrapper(bound_field)


@register.filter
def is_initial_file(value):
    """Check for initial value of FileFile."""
    return bool(value and getattr(value, 'url', False))


@register.filter
def is_null_boolean_selected(bound_field, value):
    """Return NullBooleanField state."""
    BOOL_VALUES = {True: '2', False: '3', '2': '2', '3': '3'}
    try:
        current_value = BOOL_VALUES[bound_field.value()]
    except KeyError:
        current_value = '1'
    return value == current_value


@register.filter
def select_options(bound_field):
    """
    Return list of (group_name, option_label, option_value, selected).

    If group_name is None - option is not belongs to group
    """
    selected = bound_field.value()
    if not isinstance(selected, (list, tuple, QuerySet)):
        selected = [selected]
    selected = set(force_text(v) for v in selected)

    groups = OrderedDict()
    for option in bound_field.field.widget.choices:
        option_value, option_label = option[0], option[1]
        if isinstance(option_label, (list, tuple)):
            if option_value not in groups:
                groups[option_value] = []
            for value, label in option_label:
                if value is None:
                    value = ''
                value = force_text(value)
                groups[option_value].append((label, value, value in selected))
        else:
            if None not in groups:
                groups[None] = []
            if option_value is None:
                option_value = ''
            value = force_text(option_value)
            groups[None].append(
                (option_label, option_value, value in selected)
            )

    return groups.items()
