import re
import warnings
from functools import partial
from django.template import TemplateDoesNotExist
from django.template.loader import get_template, select_template
from django.utils import six
from django.utils.encoding import smart_text


class LayoutNode(object):
    """
    Base class for self-rendered nodes for {% include %} template tag,
    based on context defined template pack
    """
    span_columns = 1
    template_name = None

    def get_context_data(self, context):
        return {}

    def get_template(self, context):
        template_name = self.template_name
        if 'template' in context:
            template_name = context['template']
        return get_template("{}/{}".format(context['form_template_pack'], template_name))

    def render(self, context, **options):
        context.push()
        try:
            for key, value in self.get_context_data(context).items():
                context[key] = value

            template = self.get_template(context)
            return template.render(context)
        finally:
            context.pop()


def _convert_to_field(elements):
    result = []
    for element in elements:
        if isinstance(element, six.string_types):
            result.append(Field(element))
        else:
            result.append(element)
    return result


def _camel_case_to_underscore(name):
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2',
                  re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)).lower()


def _get_field_template(template_pack, field):
    widget_templates = [
        '{}_{}.html'.format(cls.__module__.split('.', 1)[0], cls.__name__.lower())
        for cls in type(field.widget).mro()[:-2]]

    field_templates = [
        '{}_{}/{}'.format(cls.__module__.split('.', 1)[0], cls.__name__.lower(), widget_template)
        for cls in type(field).mro()[:-2]
        for widget_template in widget_templates]

    template_names = ["{}/fields/{}".format(template_pack, template_name)
                      for template_name in widget_templates + field_templates]

    return select_template(template_names)


class Layout(LayoutNode):
    """
    Form layout specification
    """
    template_name = 'layout/layout.html'

    def __init__(self, *elements):
        self.elements = _convert_to_field(elements)


class Fieldset(LayoutNode):
    template_name = 'layout/fieldset.html'

    def __init__(self, label, *elements, **kwargs):
        self.label = label
        self.elements = _convert_to_field(elements)
        self.span_columns = kwargs.pop('span_columns', 1)


class Inline(LayoutNode):
    template_name = 'layout/inline_tabular.html'

    def __init__(self, label, inline, varname=None):
        self.label = label
        self.inline = inline
        self.varname = varname if varname else _camel_case_to_underscore(inline.__name__)

    def get_context_data(self, context):
        return {'inline': context[self.varname]}


class Row(LayoutNode):
    template_name = 'layout/row.html'

    def __init__(self, *elements, **kwargs):
        self.elements = _convert_to_field(elements)
        self.row_id = kwargs.pop('row_id', None)

    def __getattr__(self, name):
        _, container_size = name.split('_')
        container_size = int(container_size)

        def elements_iterator():
            elements_span = sum(element.span_columns for element in self.elements)
            if container_size % elements_span != 0:
                warnings.warn("Can't equally divide container {} for {} span elements"
                              .format(container_size, self.elements))

            span_multiplier = container_size // elements_span
            for element in self.elements:
                yield element, element.span_columns * span_multiplier

        return elements_iterator


class Column(LayoutNode):
    template_name = 'layout/column.html'

    def __init__(self, *elements, **kwargs):
        self.elements = _convert_to_field(elements)
        self.span_columns = kwargs.pop('span_columns', 1)
        self.column_id = kwargs.pop('column_id', None)


class Span(object):
    template_name = 'layout/field.html'

    def __init__(self, span_columns, field_name):
        self.span_columns = span_columns
        self.field_name = field_name

    def render(self, context, **options):
        template_pack = context['form_template_pack']
        form = context['form']
        bound_field = form[self.field_name]

        try:
            if 'template' in options:
                template = select_template(["{}/{}".format(template_pack, options['template'])])
            elif 'widget' in options:
                widget_templates = [
                    '{}/fields/{}_{}.html'.format(template_pack, cls.__module__.split('.', 1)[0], cls.__name__.lower())
                    for cls in type(options['widget']).mro()[:-2]]
                template = select_template(widget_templates)
            else:
                template = _get_field_template(template_pack, bound_field.field)
        except TemplateDoesNotExist:
            # fallback to default field render
            warnings.warn("Unknown field and widget {} {}".format(
                bound_field.field.__class__, bound_field.field.widget.__class__))
            return smart_text(bound_field)
        else:
            hidden_initial = ''

            if bound_field.field.show_hidden_initial:
                hidden_initial = bound_field.as_hidden(only_initial=True)

            context.push()
            try:
                context['bound_field'] = bound_field
                context['field'] = bound_field.field
                context['hidden_initial'] = hidden_initial
                return template.render(context)
            finally:
                context.pop()

    def __str__(self):
        return 'Span{}({})'.format(self.span_columns, self.field_name)


Field = partial(Span, 1)
Span2 = partial(Span, 2)
Span3 = partial(Span, 3)
Span4 = partial(Span, 4)
Span5 = partial(Span, 5)
Span6 = partial(Span, 6)
Span7 = partial(Span, 7)
Span8 = partial(Span, 8)
Span9 = partial(Span, 9)
Span10 = partial(Span, 10)
Span11 = partial(Span, 11)
Span12 = partial(Span, 12)


def _collect_elements(element_cls, parent, container=None):
    if container is None:
        container = []

    if hasattr(parent, 'elements'):
        for element in parent.elements:
            _collect_elements(element_cls, element, container=container)

    if isinstance(parent, element_cls):
        container.append(parent)

    return container


class LayoutMixin(object):
    """
    Extracts from layout `fields` for django FormView
    `inlines` and `inlines_names` for django-extra-views
    """
    @property
    def fields(self):
        return [field.field_name for field in _collect_elements(Span, self.layout)]

    @property
    def inlines(self):
        return [inline.inline for inline in _collect_elements(Inline, self.layout)]

    @property
    def inlines_names(self):
        return [inline.varname for inline in _collect_elements(Inline, self.layout)]
