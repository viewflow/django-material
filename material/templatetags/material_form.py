import os
from collections import defaultdict

from django.forms.forms import BoundField
from django.template.base import (
    TemplateSyntaxError, Library,
    Node, Variable, token_kwargs)
from django.template.loader import get_template
from django.template.loader_tags import IncludeNode


register = Library()


def _render_parts(context, parts_list):
    parts = context['form_parts']

    for partnode in parts_list:
        part = partnode.resolve_part(context)
        if partnode.section not in parts[part]:
            value = partnode.render(context)
            parts[part][partnode.section] = value


@register.tag('form')
class FormNode(Node):
    """
    Template based form rendering

    Example::

        {% form template='material/form.html' form=form layout=view.layout %}
            {% part form.email prepend %}<span class="input-group-addon" id="basic-addon1">@</span>{% endpart %}
        {% endform %}
    """

    def __init__(self, parser, token):
        bits = token.split_contents()
        remaining_bits = bits[1:]

        self.kwargs = token_kwargs(remaining_bits, parser)

        if remaining_bits:
            raise TemplateSyntaxError("%r received an invalid token: %r" %
                                      (bits[0], remaining_bits[0]))

        for key in self.kwargs:
            if key not in ('form', 'layout', 'template'):
                raise TemplateSyntaxError("%r received an invalid key: %r" %
                                          (bits[0], key))

            self.kwargs[key] = self.kwargs[key]

        self.nodelist = parser.parse(('end{}'.format(bits[0]),))
        parser.delete_first_token()

    def render(self, context):
        form = self.kwargs.get('form')
        form = form.resolve(context) if form else context.get('form')

        if form is None:
            return ''

        # Take one of view.layout or form.layout
        layout = self.kwargs.get('layout')
        if layout is not None:
            layout = layout.resolve(context)

        if layout is None:
            if 'view' in context:
                view = context['view']
                if hasattr(view, 'layout'):
                    layout = view.layout
        if layout is None:
            if hasattr(form, 'layout'):
                layout = form.layout

        template_name = self.kwargs.get('template', 'material/form.html')
        template = get_template(template_name)

        # Render form and parts
        parts = defaultdict(dict)  # part -> section -> value

        with context.push(
                form=form,
                layout=layout,
                form_template_pack=os.path.dirname(template_name),
                form_parts=parts):

            # direct children
            children = (node for node in self.nodelist if isinstance(node, FormPartNode))
            _render_parts(context, children)

            # include
            children = (node for node in self.nodelist if isinstance(node, IncludeNode))
            for included_list in children:
                included = included_list.template.resolve(context)
                children = (node for node in included.nodelist if isinstance(node, FormPartNode))
                _render_parts(context, children)

            return template.render(context)


@register.tag('part')
class FormPartNode(Node):
    def __init__(self, parser, token):
        bits = token.split_contents()

        if len(bits) > 5:
            raise TemplateSyntaxError(
                "%r accepts at most 4 arguments (part_id, section, asvar, varname), got: {}" %
                (bits[0], ','.join(bits[1:])))

        self.part_id = Variable(bits[1])
        self.section = bits[2] if len(bits) >= 3 else None

        self.varname = None
        if len(bits) > 3:
            if bits[3] != 'asvar':
                raise TemplateSyntaxError('Forth argument should be asvar, got {}', format(bits[3]))
            if len(bits) < 4:
                raise TemplateSyntaxError('Variable name not provided')
            else:
                self.varname = Variable(bits[4])

        self.nodelist = parser.parse(('end{}'.format(bits[0]),))
        parser.delete_first_token()

    def resolve_part(self, context):
        part = self.part_id.resolve(context)
        if isinstance(part, BoundField):
            part = part.field
        return part

    def render(self, context):
        part = self.resolve_part(context)
        parts = context['form_parts']

        if self.section in parts[part]:
            # already rendered
            if self.varname is not None:
                context[self.varname.resolve(context)] = parts[part][self.section]
                return ""
            else:
                return parts[part][self.section]

        # child parts
        children = (node for node in self.nodelist if isinstance(node, FormPartNode))
        _render_parts(context, children)

        # render own content
        value = self.nodelist.render(context).strip()
        if self.varname is not None:
            context[self.varname.resolve(context)] = value
            return ''
        else:
            if not value:
                return ''
            return value
