from django.contrib.auth import get_permission_codename
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.forms.models import modelform_factory
from django.views import generic

from .mixins import _collect_elements


class DetailModelView(generic.DetailView):
    """Thin wrapper for `generic.DetailView`."""

    viewset = None
    form_class = None
    form_widgets = None
    layout = None
    fields = None

    def __init__(self, *args, **kwargs):  # noqa D102
        super(DetailModelView, self).__init__(*args, **kwargs)
        if self.form_class is None and self.fields is None:
            if self.layout is not None:
                self.fields = _collect_elements(self.layout)
            else:
                self.fields = '__all__'

    def get_queryset(self):
        """Return the list of items for this view.

        If view have no explicit `self.queryset`, tries too lookup to
        `viewflow.get_queryset`
        """
        if self.queryset is None and self.viewset is not None:
            if hasattr(self.viewset, 'get_queryset'):
                return self.viewset.get_queryset(self.request)
        return super(DetailModelView, self).get_queryset()

    def get_form_kwargs(self):
        return {
            'instance': self.object
        }

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_class(self):
        if self.form_class is None:
            if self.model is not None:
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                model = self.object.__class__
            else:
                model = self.get_queryset().model
            return modelform_factory(model, fields=self.fields, widgets=self.form_widgets)
        return super(DetailModelView, self).get_form_class()

    def has_view_permission(self, request, obj):
        """Object view permission check.

        If view had a `viewset`, the `viewset.has_view_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_view_permission(request, obj)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('view', opts)
        view_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(view_perm):
            return True
        elif request.user.has_perm(view_perm, obj=obj):
            return True
        return self.has_change_permission(request, obj=obj)

    def has_change_permission(self, request, obj):
        """Object chane permission check.

        If view had a `viewset`, the `viewset.has_change_permission` used.

        If true, view will show `Change` link to the Change view.
        """
        if self.viewset is not None:
            return self.viewset.has_change_permission(request, obj)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('change', opts)
        change_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(change_perm):
            return True
        return request.user.has_perm(change_perm, obj=obj)

    def has_delete_permission(self, request, obj):
        """Object delete permission check.

        If true, view will show `Delete` link to the Delete view.
        """
        if self.viewset is not None:
            return self.viewset.has_delete_permission(request, obj)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('delete', opts)
        delete_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(delete_perm):
            return True
        return request.user.has_perm(delete_perm, obj=obj)

    def get_object(self):
        """Retrieve the object.

        Check object view permission at the same time.
        """
        obj = super(DetailModelView, self).get_object()
        if not self.has_view_permission(self.request, obj):
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        """Additional context data for detail view.

        :keyword object_data: List of fields and values of the object
        :keyword change_url: Link to the change view
        :keyword delete_url: Link to the delete view
        """
        opts = self.model._meta

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        if self.has_change_permission(self.request, self.object):
            kwargs['change_url'] = reverse(
                '{}:{}_change'.format(opts.app_label, opts.model_name),
                args=[self.object.pk])
        if self.has_delete_permission(self.request, self.object):
            kwargs['delete_url'] = reverse(
                '{}:{}_delete'.format(opts.app_label, opts.model_name),
                args=[self.object.pk])

        return super(DetailModelView, self).get_context_data(**kwargs)

    def get_template_names(self):
        """
        List of templates for the view.

        If no `self.template_name` defined, returns::

             [<app_label>/<model_label>_detail.html
              'material/frontend/views/detail.html']
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(
                    opts.app_label,
                    opts.model_name,
                    self.template_name_suffix),
                'material/frontend/views/detail.html',
            ]

        return [self.template_name]
