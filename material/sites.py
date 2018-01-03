from django.urls import URLResolver, NoReverseMatch
from django.urls.resolvers import RoutePattern
from django.utils.functional import cached_property

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


class AppViewset(NamedViewsetMixin, Viewset):
    """
    A top level application viewset.
    """
    title = None
    icon = Icon("view_carousel")

    def __init__(self, *, title=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        if self.title is None:
            self.title = self.app_name.replace('_', '').title()


class Application(IndexViewMixin, NamedViewsetMixin, Viewset):
    """
    Top-level group of viewsets.
    """

    title = None
    icon = Icon("view_module")
    menu_template_name = 'material/includes/app_menu.html'
    base_template_name = 'material/base_site.html'

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

    def menu_items(self):
        result = []
        for attr_name in self._viewset_items:
            attr = getattr(self, attr_name, None)
            if isinstance(attr, AppViewset):
                result.append(attr)
        return result


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

    @cached_property
    def _viewset_models(self):
        result = {}

        queue = list(self.apps)
        while queue:
            viewset = queue.pop(0)
            if hasattr(viewset, 'model') and viewset.model not in result:
                result[viewset.model] = viewset
            for attr_name in viewset._viewset_items:
                attr = getattr(viewset, attr_name)
                if attr is None:
                    continue
                if attr_name.endswith('_viewset') and isinstance(attr, Viewset):
                    queue.append(attr)
        return result

    def get_object_url(self, request, obj):
        model = type(obj)
        if model in self._viewset_models:
            return self._viewset_models[model].get_object_url(request, obj)
        else:
            raise NoReverseMatch('Viewset for {} not found'.format(model.__name__))


# This global object represents the default material site, for the common case.
site = Site()
