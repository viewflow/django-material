from django.contrib import auth
from django.urls import path

from material import AppViewset, viewprop

from .create import CreateModelView
from .list import ListModelView


DEFAULT = object()


class BaseModelViewSet(AppViewset):
    model = DEFAULT
    queryset = DEFAULT

    def filter_kwargs(self, view_class, **kwargs):
        result = {
            'model': self.model,
            'viewset': self,
            'queryset': self.queryset,
            **kwargs
        }
        return {
            name: value for name, value in result.items()
            if hasattr(view_class, name)
            if value is not DEFAULT
        }

    @property
    def index_url(self):
        return path('', self.list_view, name='index')

    """
    List
    """
    list_view_class = ListModelView

    def has_view_permission(self, request, obj=None):
        view_perm = auth.get_permission_codename('view', self.model._meta)

        if request.user.has_perm(view_perm):
            return True
        elif request.user.has_perm(view_perm, obj=obj):
            return True
        return self.has_change_permission(request, obj=obj)

    def get_list_view_kwargs(self, **kwargs):
        view_kwargs = {
            **self.list_view_kwargs,
            **kwargs
        }
        return self.filter_kwargs(self.list_view_class, **view_kwargs)

    @viewprop
    def list_view_kwargs(self):
        return {}

    @viewprop
    def list_view(self):
        return self.list_view_class.as_view(**self.get_list_view_kwargs())

    @property
    def list_url(self):
        return path('', self.list_view, name='list')

    """
    Create
    """
    create_view_class = CreateModelView

    def has_add_permission(self, request):
        return request.user.has_perm(
            auth.get_permission_codename('add', self.model._meta)
        )

    def get_create_view_kwargs(self, **kwargs):
        view_kwargs = {
            **self.create_view_kwargs,
            **kwargs
        }
        return self.filter_kwargs(self.create_view_class, view_kwargs)

    @viewprop
    def create_view_kwargs(self):
        return {}

    @viewprop
    def create_view(self):
        return self.create_view_class.as_view(**self.get_create_view_kwargs())

    @property
    def create_url_(self):
        return path('add/', self.create_view, name='login')

    """
    Update
    """
    def has_change_permission(self, request, obj=None):
        change_perm = auth.get_permission_codename('change', self.model._meta)

        if request.user.has_perm(change_perm):
            return True
        return request.user.has_perm(change_perm, obj=obj)


class ModelViewSet(BaseModelViewSet):
    list_columns = DEFAULT

    def get_list_view_kwargs(self, **kwargs):
        view_kwargs = {
            'columns': self.list_columns,
            **kwargs
        }
        return super().get_list_view_kwargs(**view_kwargs)
