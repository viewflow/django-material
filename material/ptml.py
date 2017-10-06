"""
Python Template Markup Language.

It's like JSX but for Python.
"""
from django.utils.html import mark_safe, conditional_escape


class HtmlElement(object):
    tag = 'div'
    void = False

    def __init__(self, **attrs):
        self.attrs = attrs
        self.body = None

    def __truediv__(self, obj):
        if self.void:
            raise ValueError("{} can't have a value".format(self.tag))
        if not isinstance(obj, (list, tuple)):
            raise ValueError('Element content should be a list')
        self.body = obj
        return self

    def __str__(self):
        attrs = ' '.join(
            filter(None, (self._format_attr(name, value) for name, value in self.attrs.items()))
        )

        if self.void:
            return mark_safe('<{}{}{}/>'.format(self.tag, ' ' if attrs else '', attrs))
        else:
            body = ''
            if self.body:
                body = ''.join(conditional_escape(str(child)) for child in self.body if child is not None)
            return mark_safe('<{}{}{}>{}</{}>'.format(self.tag, ' ' if attrs else '', attrs, body, self.tag))

    def _format_attr(self, name, value):
        cleaned_name = self._clean_name(name)
        cleaned_value = self._clean_value(name, value)

        if cleaned_value is None:
            return ''
        elif isinstance(cleaned_value, bool):
            return cleaned_name if value else ''
        else:
            return '{}="{}"'.format(cleaned_name, cleaned_value)

    def _clean_name(self, name):
        return name.rstrip('_').replace('_', '-')

    def _clean_value(self, name, value):
        if value is None:
            return None
        elif isinstance(value, bool):
            return value
        elif isinstance(value, dict):
            value = ' '.join(key for key, enabled in value.items() if enabled)
            if value == '':
                return None

        return conditional_escape(value)


class Div(HtmlElement):
    pass


class H1(HtmlElement):
    tag = 'h1'


class H2(HtmlElement):
    tag = 'h2'


class H3(HtmlElement):
    tag = 'h3'


class H4(HtmlElement):
    tag = 'h5'


class Span(HtmlElement):
    tag = 'span'


class I(HtmlElement):
    tag = 'i'


class P(HtmlElement):
    tag = 'p'


class Label(HtmlElement):
    tag = 'label'


class Ul(HtmlElement):
    tag = 'ul'


class Li(HtmlElement):
    tag = 'li'


class Input(HtmlElement):
    tag = 'input'
    void = True


class Svg(HtmlElement):
    tag = 'svg'


class Path(HtmlElement):
    tag = 'path'
    void = True
