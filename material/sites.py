from django.urls import URLResolver, NoReverseMatch
from django.urls.resolvers import RoutePattern

from material.ptml import Icon
from material.viewset import Viewset, IndexViewMixin, NamedViewsetMixin


class _UrlName(str):
    """
    Dump str wrapper.

    Just to keep a reference over django url resolve calling
    hierarchy.
    """
    def __init__(self, value):
        str.__init__(value)
        self.extra = {}


class _URLResolver(URLResolver):
    def __init__(self, *args, **kwargs):
        self.extra = kwargs.pop('extra', {})
        super(_URLResolver, self).__init__(*args, **kwargs)

    def resolve(self, *args, **kwargs):
        result = super(_URLResolver, self).resolve(*args, **kwargs)
        if not isinstance(result.url_name, _UrlName):
            result.url_name = _UrlName(result.url_name)

        extra = {}
        extra.update(self.extra)
        extra.update(result.url_name.extra)
        result.url_name.extra = extra
        return result


class Application(IndexViewMixin, NamedViewsetMixin, Viewset):
    """
    Top-level group of viewsets.
    """

    title = None
    icon = Icon("view_module")

    def __init__(self, *, title=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        if self.title is None:
            self.title = self.app_name.replace('_', '').title()

    def has_perm(self, user):
        return True

    @property
    def urls(self):
        pattern = RoutePattern('', is_endpoint=False)
        url_patterns, app_name, namespace = super().urls
        resolver = _URLResolver(pattern, url_patterns, extra={'app': self})
        return [resolver], app_name, namespace


class Site(IndexViewMixin, Viewset):
    """Object combines set of module under in a single place."""
    title = None
    icon = Icon('view_comfy')
    menu_template_name = 'material/includes/site_menu.html'

    def __init__(self, *, title=None, apps=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.apps = apps or []
        self._menu_template = None

    def has_perm(self, user):
        return True

    def register(self, app_class):
        self.apps.append(app_class())

    def get_urls(self):
        urlpatterns = super().get_urls()
        for app in self.apps:
            if app.app_name is None:
                raise ValueError(
                    "Site application {} should have an app_name".format(app.title or app))
            urlpatterns.append(self._mount(app.app_name, app))
        return urlpatterns

    @property
    def urls(self):
        pattern = RoutePattern('', is_endpoint=False)
        url_patterns, app_name, namespace = super().urls
        resolver = _URLResolver(pattern, url_patterns, extra={'site': self})
        return [resolver], app_name, namespace

    def parent_index(self):
        if self._parent:
            try:
                return self._parent.reverse('index')
            except NoReverseMatch:
                pass


# This global object represents the default material site, for the common case.
site = Site()
