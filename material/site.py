from django.views import generic
from django.urls import path
from material.viewset import Viewset


class Application(Viewset):
    title = None

    def __init__(self, title=None):
        super().__init__()
        self.title = title

    @property
    def index_view(self):
        return path('', generic.RedirectView.as_view())


class Site(Viewset):
    """Object combines set of module under in a single place."""
    def __init__(self, apps=None):
        super().__init__()
        self.apps = apps or []

    @property
    def index_view(self):
        return path('', generic.RedirectView.as_view())


# This global object represents the default material site, for the common case.
site = Site()
