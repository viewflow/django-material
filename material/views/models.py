from django.contrib import auth
from django.urls import path

from material import AppViewset, viewprop

from .create import CreateModelView


class CRUDViewset(AppViewset):
    model = None

    """
    Create
    """
    create_view_klass = CreateModelView

    def has_add_permission(self, request):
        return request.user.has_perm(
            auth.get_permission_codename('add', self.model._meta)
        )

    def get_create_view_kwargs(self, **kwargs):
        result = {
            'viewset': self,
            **self.create_view_kwargs,
            **kwargs
        }
        # TODO filter
        return result

    @viewprop
    def create_view_kwargs(self):
        return {}

    @viewprop
    def create_view(self):
        return self.create_view_klass.as_view(**self.get_create_view_kwargs())

    @property
    def create_url_(self):
        return path('add/', self.create_view, name='login')
