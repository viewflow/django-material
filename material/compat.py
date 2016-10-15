"""Django backport and compatibility utilities."""

import inspect
import functools

from django.utils import six
from django.utils.html import conditional_escape


__all__ = ('simple_tag', )


try:
    from django.template.library import Library  # NOQA
    simple_tag = Library.simple_tag
except ImportError:
    # django 1.8
    from django.template import Node
    from django.template.base import parse_bits

    class TagHelperNode(Node):
        """Base class for tag helper nodes such as SimpleNode and InclusionNode.

        Manages the positional and keyword arguments to be passed to
        the decorated function.
        """

        def __init__(self, func, takes_context, args, kwargs):  # noqa: D102
            self.func = func
            self.takes_context = takes_context
            self.args = args
            self.kwargs = kwargs

        def get_resolved_arguments(self, context):
            resolved_args = [var.resolve(context) for var in self.args]
            if self.takes_context:
                resolved_args = [context] + resolved_args
            resolved_kwargs = {
                k: v.resolve(context)
                for k, v in self.kwargs.items()
            }
            return resolved_args, resolved_kwargs

    class SimpleNode(TagHelperNode):
        def __init__(self, func, takes_context, args, kwargs, target_var):
            super(SimpleNode, self).__init__(func, takes_context, args, kwargs)
            self.target_var = target_var

        def render(self, context):
            resolved_args, resolved_kwargs = \
                self.get_resolved_arguments(context)
            output = self.func(*resolved_args, **resolved_kwargs)
            if self.target_var is not None:
                context[self.target_var] = output
                return ''
            if context.autoescape:
                output = conditional_escape(output)
            return output

    def getargspec(func):
        if six.PY2:
            return inspect.getargspec(func)

        sig = inspect.signature(func)
        args = [
            p.name for p in sig.parameters.values()
            if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        ]
        varargs = [
            p.name for p in sig.parameters.values()
            if p.kind == inspect.Parameter.VAR_POSITIONAL
        ]
        varargs = varargs[0] if varargs else None
        varkw = [
            p.name for p in sig.parameters.values()
            if p.kind == inspect.Parameter.VAR_KEYWORD
        ]
        varkw = varkw[0] if varkw else None
        defaults = [
            p.default for p in sig.parameters.values()
            if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            if p.default is not p.empty
        ] or None
        return args, varargs, varkw, defaults

    def simple_tag(library, func=None, takes_context=None, name=None):
        """
        Register a callable as a compiled template tag.

        Example:
            @register.simple_tag
            def hello(*args, **kwargs):
                return 'world'

        Backport from django 1.9
        """
        def dec(func):
            params, varargs, varkw, defaults = getargspec(func)
            function_name = (
                name or getattr(func, '_decorated_function', func).__name__
            )

            @functools.wraps(func)
            def compile_func(parser, token):
                bits = token.split_contents()[1:]
                target_var = None
                if len(bits) >= 2 and bits[-2] == 'as':
                    target_var = bits[-1]
                    bits = bits[:-2]
                    args, kwargs = parse_bits(
                        parser, bits, params, varargs, varkw,
                        defaults, takes_context, function_name)
                return SimpleNode(
                    func, takes_context, args, kwargs, target_var)
            library.tag(function_name, compile_func)
            return func

        if func is None:
            # @register.simple_tag(...)
            return dec
        elif callable(func):
            # @register.simple_tag
            return dec(func)
        else:
            raise ValueError("Invalid arguments provided to simple_tag")


def context_flatten(context):
    result = {}
    # https://code.djangoproject.com/ticket/24765
    for dict_ in context.dicts:
        if hasattr(dict_, 'flatten'):
            dict_ = context_flatten(dict_)
        result.update(dict_)
    return result
