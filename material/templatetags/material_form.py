from django.template.base import (TemplateSyntaxError, Library, Node, token_kwargs)

register = Library()


@register.tag(register, 'form')
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

        kwargs = token_kwargs(remaining_bits, parser)

        if remaining_bits:
            raise TemplateSyntaxError("%r received an invalid token: %r" %
                                      (bits[0], remaining_bits[0]))

        for key in kwargs:
            if key not in ('form', 'layout'):
                raise TemplateSyntaxError("%r received an invalid key: %r" %
                                          (bits[0], key))

        self.nodelist = parser.parse(('end{}'.format(bits[0]),))
        parser.delete_first_token()

    def render(self, context):
        pass


@register.tag(register, 'part')
class FormPartNode(Node):
    pass
