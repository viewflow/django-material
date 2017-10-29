from django.views import generic
from django.urls import URLPattern, URLResolver, path, include
from django.urls.resolvers import RegexPattern

from material.utils import strip_suffixes, camel_case_to_underscore


class viewset_items(dict):
    """Track the order of declared views and child viewsets."""
    def __init__(self):
        self.items = []

    def __setitem__(self, key, value):
        if key not in self:
            if key.endswith('_view') or key.endswith('_viewset'):
                self.items.append(key)
        # Call superclass
        dict.__setitem__(self, key, value)


class ViewsetMetaClass(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return viewset_items()

    def __new__(cls, name, bases, classdict):
        result = type.__new__(cls, name, bases, dict(classdict))

        items = []

        metabases = (
            base for base in bases
            if hasattr(base, '_viewset_items')
        )
        for metabase in metabases:
            items += metabase._viewset_items

        for item in classdict.items:
            if item not in items:
                items.append(item)

        result._viewset_items = items

        return result


class Viewset(metaclass=ViewsetMetaClass):
    """
    Set of views ready to include into the django url config.

    Automatically collect URL patterns from `_view` and `_viewset` class attributes.

    For sub-viewsets attribute name used as the default value for url prefix and
    url namepace.

    Example::

        class SiteViewset(Viewset):
            stats_view = path('stats/', DeptStatView.as_view(), name="stats")
            employees_viewset = EmployeesViewset(prefix='emp')

        urlpatters = [
            SiteViewset(app_name="site").urls,
        ]

        reverse('site:employees:index')

    .. seealso::
        `Django URL namespaces
        https://docs.djangoproject.com/en/1.11/topics/http/urls/#url-namespaces>`_
    """

    namespace = None
    prefix = None

    def __init__(self, *, prefix=None, app_name=None, namespace=None):
        """
        Instantiate a viewset instance.

        :param prefix: an URL prefix. Could be used by parent viewset.
        :param app_name: application URL namespace
        :param namespace: instance URL namespace
        """
        self._urls = None
        self.prefix = prefix
        self.app_name = app_name
        self.namespace = namespace
        super().__init__()

    def get_viewset_pattern(self, attr_name, viewset):
        prefix = viewset.prefix
        patterns, app_name, namespace = viewset.urls
        default = strip_suffixes(attr_name, ["_viewset"])

        if prefix is None:
            prefix = default

        if app_name is None:
            name = default

        if namespace is None:
            namespace = default

        return path('{}/'.format(prefix), include((patterns, name), namespace=namespace))

    def get_urls(self):
        """
        Collect URLs from the instance attributes.

        Assumes that each attribute with name ending on `_view`
        contains url pattern declaration.

        Attributes ends on `_viewset` is the Viewset class instance
        """
        urlpatterns = []

        for attr_name in self._viewset_items:
            attr = getattr(self, attr_name)
            if isinstance(attr, URLPattern):
                urlpatterns.append(attr)
            elif isinstance(attr, Viewset):
                urlpatterns.append(self.get_viewset_pattern(attr_name, attr))

        return urlpatterns

    @property
    def urls(self):
        namespace = self.namespace
        if namespace is None:
            namespace = self.app_name
        if self._urls is None:
            self._urls = self.get_urls()
        return self._urls, self.app_name, namespace


def _get_viewset_index_url(viewset):
    """
    Return first non-parameterized viewset url.
    """
    pattern, app_name, namespace = viewset.urls
    resolver = URLResolver(RegexPattern(r'^/'), pattern, app_name=app_name, namespace=namespace)

    for url_pattern in viewset.urls[0]:
        if isinstance(url_pattern, URLPattern):
            couldbe_index_view = (
                url_pattern.pattern.converters == {} and
                not (hasattr(url_pattern.callback, 'view_class') and
                     url_pattern.callback.view_class == IndexRedirectView)
            )
            if couldbe_index_view:
                match = resolver.reverse_dict.get(url_pattern.callback, None)
                if match:
                    matches, _, _, _ = match
                    return '{}'.format(matches[0][0])


class IndexRedirectView(generic.RedirectView):
    viewset = None

    def get_redirect_url(self, *args, **kwargs):
        if self.viewset:
            return _get_viewset_index_url(self.viewset)
        return super().get_redirect_url(*args, **kwargs)


class IndexViewMixin(metaclass=ViewsetMetaClass):
    """
    Redirect from / to the first non-parameterized view of the viewset.
    """
    @property
    def index_view(self):
        return path('', IndexRedirectView.as_view(viewset=self), name="index")


class NamedViewsetMixin:
    """
    Auto-derive viewset namespace from the viewset class name.
    """
    name = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        viewset_name = camel_case_to_underscore(
            strip_suffixes(
                self.__class__.__name__,
                ['Viewset', 'Admin']))

        if self.name is None:
            self.app_name = viewset_name
