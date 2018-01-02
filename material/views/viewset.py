from django.urls import path

from material.ptml import Icon
from material.sites import AppViewset
from material.viewset import ViewsetMetaClass, viewprop

from .base import Action, has_object_perm
from .create import CreateModelView
from .delete import DeleteModelView
from .detail import DetailModelView
from .list import ListModelView
from .update import UpdateModelView


DEFAULT = object()


def _first_not_default(*args):
    for arg in args:
        if arg is not DEFAULT:
            return arg
    return arg


class BaseModelViewset(AppViewset):
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


class ModelViewset(BaseModelViewset):
    """List/Create/Update/Delete for a model."""

    def get_object_url(self, request, obj):
        if self.has_change_permission(request, obj):
            return self.reverse('change', args=[obj.pk])

    def get_success_url(self, request, obj=None):
        return self.reverse('index')

    """
    List
    """
    list_view_class = ListModelView
    list_columns = DEFAULT
    list_object_link_columns = DEFAULT
    list_page_actions = DEFAULT

    def has_view_permission(self, request, obj=None):
        return (
            has_object_perm(request.user, 'view', self.model, obj=obj) or
            self.has_change_permission(request, obj=obj)
        )

    def get_list_view_kwargs(self, **kwargs):
        view_kwargs = {
            'columns': self.list_columns,
            'object_link_columns': self.list_object_link_columns,
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

    def get_list_page_actions(self, request, *actions):
        if self.has_add_permission(request):
            actions = (
                Action(name="Add new", url=self.reverse('add'), icon=Icon('add')),
                *actions
            )
        if self.list_page_actions is not DEFAULT:
            actions = (
                *self.list_page_actions,
                *actions
            )
        return actions

    """
    Update
    """
    update_view_class = UpdateModelView
    form_layout = DEFAULT
    form_class = DEFAULT
    form_widgets = DEFAULT

    def has_change_permission(self, request, obj=None):
        return has_object_perm(request.user, 'change', self.model, obj=obj)

    def get_update_view_kwargs(self, **kwargs):
        view_kwargs = {
            'form_class': self.form_class,
            'form_widgets': self.form_widgets,
            'layout': self.form_layout,
            **self.update_view_kwargs,
            **kwargs
        }
        return self.filter_kwargs(self.update_view_class, **view_kwargs)

    @viewprop
    def update_view_kwargs(self):
        return {}

    @viewprop
    def update_view(self):
        return self.update_view_class.as_view(**self.get_update_view_kwargs())

    @property
    def update_url(self):
        return path('<path:pk>/change/', self.update_view, name='change')

    """
    Create
    """
    create_view_class = CreateModelView
    create_form_layout = DEFAULT
    create_form_class = DEFAULT
    create_form_widgets = DEFAULT

    def has_add_permission(self, request):
        return has_object_perm(request.user, 'add', self.model)

    def get_create_view_kwargs(self, **kwargs):
        layout = self.create_form_layout
        if self.create_form_class is DEFAULT:
            layout = _first_not_default(self.create_form_layout, self.form_layout)

        view_kwargs = {
            'form_class': _first_not_default(self.create_form_class, self.form_class),
            'form_widgets': _first_not_default(self.create_form_widgets, self.form_widgets),
            'layout': layout,
            **self.create_view_kwargs,
            **kwargs
        }
        return self.filter_kwargs(self.create_view_class, **view_kwargs)

    @viewprop
    def create_view_kwargs(self):
        return {}

    @viewprop
    def create_view(self):
        return self.create_view_class.as_view(**self.get_create_view_kwargs())

    @property
    def create_url(self):
        return path('add/', self.create_view, name='add')

    """
    Delete
    """
    delete_view_class = DeleteModelView

    def has_delete_permission(self, request, obj=None):
        return has_object_perm(request.user, 'delete', self.model, obj=obj)

    def get_delete_view_kwargs(self, **kwargs):
        view_kwargs = {
            **self.delete_view_kwargs,
            **kwargs
        }
        return self.filter_kwargs(self.delete_view_class, **view_kwargs)

    @viewprop
    def delete_view_kwargs(self):
        return {}

    @viewprop
    def delete_view(self):
        return self.delete_view_class.as_view(**self.get_delete_view_kwargs())

    @property
    def delete_url(self):
        return path('<path:pk>/delete/', self.delete_view, name='delete')


class DetailViewsetMixin(metaclass=ViewsetMetaClass):
    def get_object_url(self, request, obj):
        if self.has_view_permission(request, obj):
            return self.reverse('detail', args=[obj.pk])

    def get_success_url(self, request, obj=None):
        if obj is not None:
            return self.reverse('detail', args=[obj.pk])
        return super().get_success_url(request, obj=obj)

    """
    Detail
    """
    detail_view_class = DetailModelView

    def get_detail_view_kwargs(self, **kwargs):
        view_kwargs = {
            **self.detail_view_kwargs,
            **kwargs
        }
        return self.filter_kwargs(self.detail_view_class, **view_kwargs)

    @viewprop
    def detail_view_kwargs(self):
        return {}

    @viewprop
    def detail_view(self):
        return self.detail_view_class.as_view(**self.get_detail_view_kwargs())

    @property
    def detail_url(self):
        return path('<path:pk>/detail/', self.detail_view, name='detail')

    def get_detail_page_actions(self, request, *actions):
        if self.has_delete_permission(request):
            actions = (
                Action(name="Delete", url=self.reverse('delete'), icon=Icon('remove')),
                *actions
            )

        return actions


class ReadonlyModelViewset(DetailViewsetMixin, BaseModelViewset):
    list_view_class = ListModelView
    list_columns = DEFAULT
    list_object_link_columns = DEFAULT
    list_page_actions = DEFAULT

    def has_view_permission(self, request, obj=None):
        for perm_name, _ in self.model._meta.permissions:
            if perm_name == 'view':
                return has_object_perm(request.user, 'view', self.model, obj=obj)
        if 'view' in self.model._meta.default_permissions:
            return has_object_perm(request.user, 'view', self.model, obj=obj)
        else:
            # No explicit `view` permission, assume all objects are available for every logged in user
            return request.user.is_authenticated

    def get_list_view_kwargs(self, **kwargs):
        view_kwargs = {
            'columns': self.list_columns,
            'object_link_columns': self.list_object_link_columns,
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

    def get_list_page_actions(self, request, *actions):
        return actions
