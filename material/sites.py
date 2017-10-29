from django.urls import path
from material.viewset import Viewset, IndexViewMixin, NamedViewsetMixin


class Application(IndexViewMixin, NamedViewsetMixin, Viewset):
    """
    Top-level group of viewsets.
    """

    title = None

    def __init__(self, *, title=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title


class Site(IndexViewMixin, Viewset):
    """Object combines set of module under in a single place."""

    def __init__(self, *, apps=None, **kwargs):
        super().__init__(**kwargs)
        self.apps = apps or []

    def register(self, app_class):
        self.apps.append(app_class())

    def get_urls(self):
        urls = super().get_urls()
        for app in self.apps:
            prefix = app.prefix
            if prefix is None:
                prefix = app.app_name
            urls += [
                path('{}/'.format(prefix), app.urls)
            ]
        return urls


# This global object represents the default material site, for the common case.
site = Site()
