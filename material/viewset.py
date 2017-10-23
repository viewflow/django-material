from django.views import generic
from django.urls import URLPattern, URLResolver, path
from django.urls.resolvers import RegexPattern


class viewset_items(dict):
    """Track the order of declared views."""
    def __init__(self):
        self.views = []

    def __setitem__(self, key, value):
        if key.endswith('_view') and key not in self:
            self.views.append(key)

        # Call superclass
        dict.__setitem__(self, key, value)


class ViewsetMetaClass(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return viewset_items()

    def __new__(cls, name, bases, classdict):
        result = type.__new__(cls, name, bases, dict(classdict))
        result._views = classdict.views
        return result


class Viewset(metaclass=ViewsetMetaClass):
    def __init__(self):
        self._urls = None

    def get_urls(self):
        """
        Collect url specs from the instance attributes.

        Assumes that each attribute with name ending with `_view`
        contains url pattern declaration.
        """
        url_entries = (
            getattr(self, attr)
            for attr in self._views
            if isinstance(getattr(self, attr), URLPattern)
        )

        return list(url_entries)

    @property
    def urls(self):
        if self._urls is None:
            self._urls = self.get_urls()
        return self._urls


def _get_viewset_index_url(viewset):
    """
    Return first non-parametrized viewset url
    """
    resolver = URLResolver(RegexPattern(r'^/'), viewset.urls)

    for url_pattern in viewset.urls:
        if isinstance(url_pattern, URLPattern):
            couldbe_index_view = (
                url_pattern.pattern.converters == {} and
                not isinstance(url_pattern.callback, IndexRedirectView)
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


class IndexViewMixin:
    """
    Redirect from / to the first non-parametrized view of the viewset.
    """
    @property
    def index_view(self):
        return path('', IndexRedirectView.as_view(viewset=self), name="index")
