from django.conf.urls import url
from django.contrib.auth import get_permission_codename

from .create import CreateModelView
from .delete import DeleteModelView
from .detail import DetailModelView
from .list import ListModelView
from .update import UpdateModelView


DEFAULT = object()


class BaseViewset(object):
    """
    Base router-like class for frontend viewset
    """

    @property
    def urls(self):
        result = []

        format_kwargs = {
            'model_name': self.model._meta.model_name
        }

        url_entries = (
            getattr(self, attr)
            for attr in self.__dir__()
            if attr.endswith('_view')
            if isinstance(getattr(self, attr), (list, tuple))
        )
        for url_entry in url_entries:
            regexp, view, name = url_entry
            result.append(
                url(regexp.format(**format_kwargs),
                    view,
                    name=name.format(**format_kwargs))
            )

        return result


class ModelViewSet(BaseViewset):
    model = None
    queryset = DEFAULT
    list_display = DEFAULT
    list_display_links = DEFAULT

    layout = DEFAULT
    form_class = DEFAULT

    def get_queryset(self, request):
        return self.queryset

    def filter_kwargs(self, view_class, **kwargs):
        result = {
            'model': self.model,
            'viewset': self,
            'queryset': self.queryset,
        }
        result.update(kwargs)
        return {name: value for name, value in result.items()
                if hasattr(view_class, name)
                if value is not DEFAULT}

    """
    Create
    """
    create_view_class = CreateModelView

    def get_create_view(self):
        return self.create_view_class.as_view(**self.get_create_view_kwargs())

    def get_create_view_kwargs(self, **kwargs):
        result = {
            'layout': self.layout,
            'form_class': self.form_class,
        }
        result.update(kwargs)
        return self.filter_kwargs(self.create_view_class, **result)

    @property
    def create_view(self):
        return [
            r'^add/$',
            self.get_create_view(),
            '{model_name}_add',
        ]

    def has_add_permission(self, request):
        opts = self.model._meta
        codename = get_permission_codename('add', opts)
        return request.user.has_perm('{}.{}'.format(opts.app_label, codename))

    """
    Detail
    """
    detail_view_class = DetailModelView

    def get_detail_view(self):
        return self.detail_view_class.as_view(**self.get_detail_view_kwargs())

    def get_detail_view_kwargs(self, **kwargs):
        return self.filter_kwargs(self.detail_view_class, **kwargs)

    def has_view_permission(self, request, obj=None):
        opts = self.model._meta
        codename = get_permission_codename('view', opts)
        view_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(view_perm, obj=obj):
            return True
        return self.has_change_permission(request, obj=obj)

    @property
    def detail_view(self):
        return [
            r'^(?P<pk>.+)/detail/$',
            self.get_detail_view(),
            '{model_name}_detail'
        ]

    """
    List
    """
    list_view_class = ListModelView

    def get_list_view(self):
        return self.list_view_class.as_view(**self.get_list_view_kwargs())

    def get_list_view_kwargs(self, **kwargs):
        result = {
            'list_display': self.list_display,
            'list_display_links': self.list_display_links
        }
        result.update(kwargs)
        return self.filter_kwargs(self.list_view_class, **result)

    @property
    def list_view(self):
        return [
            '^$',
            self.get_list_view(),
            '{model_name}_list'
        ]

    """
    Update
    """
    update_view_class = UpdateModelView

    def get_update_view(self):
        return self.update_view_class.as_view(**self.get_update_view_kwargs())

    def get_update_view_kwargs(self, **kwargs):
        result = {
            'layout': self.layout,
            'form_Class': self.form_class,
        }
        result.update(kwargs)
        return self.filter_kwargs(self.update_view_class, **result)

    def has_change_permission(self, request, obj=None):
        opts = self.model._meta
        codename = get_permission_codename('change', opts)
        return request.user.has_perm(
            '{}.{}'.format(opts.app_label, codename), obj=obj)

    @property
    def update_view(self):
        return [
            r'^(?P<pk>.+)/change/$',
            self.get_update_view(),
            '{model_name}_change',
        ]

    """
    Delete
    """
    delete_view_class = DeleteModelView

    def get_delete_view(self):
        """Function view for delete an object."""
        return self.delete_view_class.as_view(**self.get_delete_view_kwargs())

    def has_delete_permission(self, request, obj=None):
        """Default delete permission check for a delete view.

        May not be called if delete view have own implementation.
        """
        opts = self.model._meta
        codename = get_permission_codename('delete', opts)
        return request.user.has_perm(
            '{}.{}'.format(opts.app_label, codename), obj=obj)

    def get_delete_view_kwargs(self, **kwargs):
        """Configuration arguments for delete view.

        May not be called if `get_delete_view` is overriden.
        """
        return self.filter_kwargs(self.delete_view_class, **kwargs)

    @property
    def delete_view(self):
        """Tripple (regexp, view, name) for delete view url config."""
        return [
            r'^(?P<pk>.+)/delete/$',
            self.get_delete_view(),
            '{model_name}_delete'
        ]
