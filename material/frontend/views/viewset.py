from django.conf.urls import url
from django.contrib.auth import get_permission_codename

from .create import CreateModelView
from .delete import DeleteModelView
from .detail import DetailModelView
from .list import ListModelView
from .update import UpdateModelView


DEFAULT = object()


class ModelViewSet(object):
    model = None

    create_view_class = CreateModelView
    detail_view_class = DetailModelView
    list_view_class = ListModelView
    update_view_class = UpdateModelView
    delete_view_class = DeleteModelView

    queryset = DEFAULT
    list_display = DEFAULT
    list_display_links = DEFAULT

    layout = DEFAULT
    form_class = DEFAULT

    def _filter_options(self, view_class, options):
        return {name: value for name, value in options.items()
                if hasattr(view_class, name)
                if value is not DEFAULT}

    def has_add_permission(self, request):
        opts = self.model._meta
        codename = get_permission_codename('add', opts)
        return request.user.has_perm('{}.{}'.format(opts.app_label, codename))

    def has_view_permission(self, request, obj=None):
        opts = self.model._meta
        codename = get_permission_codename('view', opts)
        if request.user.has_perm('{}.{}'.format(opts.app_label, codename), obj=obj):
            return True
        return self.has_change_permission(request, obj=obj)

    def has_change_permission(self, request, obj=None):
        opts = self.model._meta
        codename = get_permission_codename('change', opts)
        return request.user.has_perm('{}.{}'.format(opts.app_label, codename), obj=obj)

    def has_delete_permission(self, request, obj=None):
        opts = self.model._meta
        codename = get_permission_codename('delete', opts)
        return request.user.has_perm('{}.{}'.format(opts.app_label, codename), obj=obj)

    def get_common_kwargs(self, **kwargs):
        result = {
            'model': self.model,
            'viewset': self,
            'queryset': self.queryset,
        }
        result.update(kwargs)
        return result

    def get_create_view_kwargs(self, **kwargs):
        result = {
            'layout': self.layout,
            'form_Class': self.form_class,
        }
        result.update(kwargs)

        return self._filter_options(
            self.create_view_class,
            self.get_common_kwargs(**result))

    def get_list_view_kwargs(self, **kwargs):
        result = {
            'list_display': self.list_display,
            'list_display_links': self.list_display_links
        }
        result.update(kwargs)

        return self._filter_options(
            self.list_view_class,
            self.get_common_kwargs(**result))

    def get_detail_view_kwargs(self, **kwargs):
        return self._filter_options(
            self.detail_view_class,
            self.get_common_kwargs(**kwargs))

    def get_update_view_kwargs(self, **kwargs):
        result = {
            'layout': self.layout,
            'form_Class': self.form_class,
        }
        result.update(kwargs)

        return self._filter_options(
            self.update_view_class,
            self.get_common_kwargs(**result))

    def get_delete_view_kwargs(self, **kwargs):
        return self._filter_options(
            self.delete_view_class,
            self.get_common_kwargs(**kwargs))

    def get_queryset(self, request):
        return self.queryset

    @property
    def create_view(self):
        return self.create_view_class.as_view(**self.get_create_view_kwargs())

    @property
    def detail_view(self):
        return self.detail_view_class.as_view(**self.get_detail_view_kwargs())

    @property
    def list_view(self):
        return self.list_view_class.as_view(**self.get_list_view_kwargs())

    @property
    def update_view(self):
        return self.update_view_class.as_view(**self.get_update_view_kwargs())

    @property
    def delete_view(self):
        return self.delete_view_class.as_view(**self.get_delete_view_kwargs())

    @property
    def urls(self):
        model_name = self.model._meta.model_name

        return [
            url('^$', self.list_view, name='{}_list'.format(model_name)),
            url('^add/$', self.create_view, name='{}_add'.format(model_name)),
            url(r'^(?P<pk>.+)/detail/$', self.detail_view, name='{}_detail'.format(model_name)),
            url(r'^(?P<pk>.+)/change/$', self.update_view, name='{}_change'.format(model_name)),
            url(r'^(?P<pk>.+)/delete/$', self.delete_view, name='{}_delete'.format(model_name)),
        ]
