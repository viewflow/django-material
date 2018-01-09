import re
from datetime import datetime
from urllib.parse import urljoin

from django import template
from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.files.storage import default_storage
from django.db import models
from django.urls import NoReverseMatch
from django.utils.encoding import force_text
from django.utils.html import conditional_escape

from material.sites import Site
from material.viewset import Viewset


register = template.Library()


KWARG_RE = re.compile(r"(?:(\w+)=)?(.+)")


def _parse_var_and_args(tagname, parser, bits):
    variable_name, args, kwargs = None, [], {}
    if len(bits) >= 2 and bits[-2] == 'as':
        variable_name = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = KWARG_RE.match(bit)
            if not match:
                raise template.TemplateSyntaxError("Malformed arguments for {} tag".format(tagname))
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return variable_name, args, kwargs


def _resolve_args(context, args, kwargs):
    args = [arg.resolve(context) for arg in args]
    kwargs = {
        force_text(key, 'ascii'): value.resolve(context)
        for key, value in kwargs.items()
    }
    return args, kwargs


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
        self.variable_name, self.args, self.kwargs = _parse_var_and_args(
            'viewset_url', parser, bits[3:]
        )

    def render(self, context):
        args, kwargs = _resolve_args(context, self.args, self.kwargs)

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


@register.tag('site_object_url')
class SiteObjectURLNode(template.Node):
    """
    Call viewset.get_object_url for an object from site

    Example::
        {% site_object_url site view.object %}
    """

    def __init__(self, parser, token):
        bits = token.split_contents()
        if len(bits) < 3:
            raise template.TemplateSyntaxError(
                "viewset_url takes at least two arguments, a "
                "site and an object.")

        self.site = parser.compile_filter(bits[1])
        self.object = parser.compile_filter(bits[2])
        if len(bits) >= 2 and bits[-2] == 'as':
            self.variable_name = bits[-1]

    def render(self, context):
        site = self.site.resolve(context)
        if not isinstance(site, Site):
            raise template.TemplateSyntaxError("site_url first argument must be a site instance")

        obj = self.object.resolve(context)
        if not isinstance(obj, models.Model):
            raise template.TemplateSyntaxError("site_url third argument must be a model instance")

        url = ''
        try:
            url = site.get_object_url(context.request, obj)
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


@register.filter
def _user_avatar_url(user):
    key = make_template_fragment_key('django-material-avatar', [user.pk])
    url = cache.get(key)
    if url is not None:
        return url

    file_name = 'avatars/{}.png'.format(user.pk)
    if default_storage.exists(file_name):
        try:
            modified = default_storage.get_modified_time(file_name)
        except NotImplementedError:
            modified = datetime.now()
        url = default_storage.url(file_name)+"?timestamp={}".format(modified.timestamp())
    else:
        if apps.is_installed('django.contrib.staticfiles'):
            from django.contrib.staticfiles.storage import staticfiles_storage
            url = staticfiles_storage.url('material/img/user.png')
        else:
            url = urljoin(settings.STATIC_URL, 'material/img/user.png')

    cache.set(key, url)
    return url
