from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth import get_permission_codename

from .create import CreateModelView
from .delete import DeleteModelView
from .detail import DetailModelView
from .list import ListModelView
from .update import UpdateModelView


DEFAULT = object()


class BaseViewset(object):
    """Base router-like class for frontend viewset."""

    @property
    def urls(self):
        """Collect url specs from the instance attributes.

        Assumes that each attribute with name ending with `_view`
        contains triple (regexp, view, url_name)
        """
        result = []

        format_kwargs = {
            'model_name': self.model._meta.model_name
        }

        url_entries = (
            getattr(self, attr)
            for attr in dir(self)
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
    """Model Create/Read/Update/Delete/List viewset.

    Lightweight alternative for django admin. CRUD interface based in
    the django generic views. Viewset provides a simple place to
    configure the views and share the common configuration parameters.

    :keyword model: Model class views

    :keyword queryset: Base views queryset

    :keyword list_display: List of fields for ListView

    :keyword list_display_links: List of fields form `list_display`
                                 linked to change view

    :keyword ordering: Defaul ListView ordering

    :keyword create_view_class: CBV for create an object

    :keyword list_view_class:  CBV for create to list objects

    :keyword detail_view_class:  CBV to show an object detail

    :keyword update_view_class: CBV to update an object

    :keyword delete_view_class: CBV to delete an object

    :keyword layout: Layout for django-material forms

    :keyword form_class: Form Class for Create and Update views

    :keyword form_widgets: Custom widgets for the model form
                           in the Create and Update views, if
                           no custom form_class provided.

    There is no specifically requirements to CBV, by overriding
    corresponding `get_<op>_view` method you can even use function
    based views with this viewset.

    Example::

        class CityViewSet(ModelViewSet):
            model = models.Sea
            list_display = ('name', 'parent', 'ocean', 'sea_area', )
            layout = Layout(
                Row('name', 'parent'),
                'ocean',
                Row('area', 'avg_depth', 'max_depth'),
                'basin_countries'
            )

            def sea_area(self, sea):
                return None if sea.area == 0 else sea.area

    """

    model = None
    queryset = DEFAULT
    list_display = DEFAULT
    list_display_links = DEFAULT
    ordering = DEFAULT

    layout = DEFAULT
    form_class = DEFAULT
    form_widgets = DEFAULT

    def filter_kwargs(self, view_class, **kwargs):
        """Add defaults and filter kwargs to only those that view can accept.

        Viewset pass to the view only kwargs that have non DEFAULT values,
        and if the view have a corresponding attribute.

        In addition, if view has `viewset` attribute, it will receive
        the `self` instance

        """
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
        """Function view for create an object."""
        return self.create_view_class.as_view(**self.get_create_view_kwargs())

    def get_create_view_kwargs(self, **kwargs):
        """Configuration arguments for create view.

        May not be called if `get_create_view` is overridden.
        """
        result = {
            'layout': self.layout,
            'form_class': self.form_class,
            'form_widgets': self.form_widgets,
        }
        result.update(kwargs)
        return self.filter_kwargs(self.create_view_class, **result)

    @property
    def create_view(self):
        """Triple (regexp, view, name) for create view url config."""
        return [
            r'^add/$',
            self.get_create_view(),
            '{model_name}_add',
        ]

    def has_add_permission(self, request):
        """Default add permission check for a detail and list views.

        May not be called if views have own implementation.
        """
        opts = self.model._meta
        codename = get_permission_codename('add', opts)
        return request.user.has_perm('{}.{}'.format(opts.app_label, codename))

    """
    Detail
    """
    detail_view_class = DetailModelView

    def get_detail_view(self):
        """Function view for object detail."""
        return self.detail_view_class.as_view(**self.get_detail_view_kwargs())

    def get_detail_view_kwargs(self, **kwargs):
        """Configuration arguments for detail view.

        May not be called if `get_detail_view` is overridden.
        """
        return self.filter_kwargs(self.detail_view_class, **kwargs)

    def has_view_permission(self, request, obj=None):
        """Default view permission check for a detail and list views.

        May not be called if views have own implementation.
        """
        opts = self.model._meta
        codename = get_permission_codename('view', opts)
        view_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(view_perm):
            return True
        elif request.user.has_perm(view_perm, obj=obj):
            return True
        return self.has_change_permission(request, obj=obj)

    @property
    def detail_view(self):
        """Triple (regexp, view, name) for detail view url config."""
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
        """Function view for objects list."""
        return self.list_view_class.as_view(**self.get_list_view_kwargs())

    def get_list_view_kwargs(self, **kwargs):
        """Configuration arguments for list view.

        May not be called if `get_list_view` is overridden.
        """
        result = {
            'list_display': self.list_display,
            'list_display_links': self.list_display_links,
            'ordering': self.ordering
        }
        result.update(kwargs)
        return self.filter_kwargs(self.list_view_class, **result)

    @property
    def list_view(self):
        """Triple (regexp, view, name) for list view url config."""
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
        """Function view for update an object."""
        return self.update_view_class.as_view(**self.get_update_view_kwargs())

    def get_update_view_kwargs(self, **kwargs):
        """Configuration arguments for update view.

        May not be called if `get_update_view` is overridden.
        """
        result = {
            'layout': self.layout,
            'form_class': self.form_class,
            'form_widgets': self.form_widgets,
        }
        result.update(kwargs)
        return self.filter_kwargs(self.update_view_class, **result)

    def has_change_permission(self, request, obj=None):
        """Default change permission check for a update view.

        May not be called if update view have own implementation.
        """
        opts = self.model._meta
        codename = get_permission_codename('change', opts)
        change_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(change_perm):
            return True
        return request.user.has_perm(change_perm, obj=obj)

    @property
    def update_view(self):
        """Triple (regexp, view, name) for update view url config."""
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
        delete_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(delete_perm):
            return True
        return request.user.has_perm(delete_perm, obj=obj)

    def get_delete_view_kwargs(self, **kwargs):
        """Configuration arguments for delete view.

        May not be called if `get_delete_view` is overridden.
        """
        return self.filter_kwargs(self.delete_view_class, **kwargs)

    @property
    def delete_view(self):
        """Triple (regexp, view, name) for delete view url config."""
        return [
            r'^(?P<pk>.+)/delete/$',
            self.get_delete_view(),
            '{model_name}_delete'
        ]
