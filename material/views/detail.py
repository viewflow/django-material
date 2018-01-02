from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.http import Http404
from django.views import generic

from .base import has_object_perm


class DetailModelView(generic.DetailView):
    viewset = None
    page_actions = None

    def has_view_permission(self, request, obj=None):
        if self.viewset is not None and hasattr(self.viewset, 'has_view_permission'):
            return self.viewset.has_view_permission(request, obj=obj)
        else:
            return (
                has_object_perm(request.user, 'view', self.model, obj=obj) or
                has_object_perm(request.user, 'change', self.model, obj=obj)
            )

    def get_object_data(self):
        """List of object fields to display.
        Choice fields values are expanded to readable choice label.
        """
        for field in self.object._meta.fields:
            if isinstance(field, models.AutoField):
                continue
            elif field.auto_created:
                continue
            else:
                choice_display_attr = "get_{}_display".format(field.name)
            if hasattr(self.object, choice_display_attr):
                value = getattr(self.object, choice_display_attr)()
            else:
                value = getattr(self.object, field.name)

            if value is not None:
                yield (field, field.verbose_name.capitalize(), value)

    def get_page_actions(self, *actions):
        if self.viewset:
            actions = self.viewset.get_detail_page_actions(self.request, self.object) + actions
        if self.page_actions:
            actions = self.page_actions + actions
        return actions

    def get_object_change_link(self):
        if self.viewset and hasattr(self.viewset, 'has_change_permission'):
            if self.viewset.has_change_permission(self.request, self.object):
                return self.viewset.reverse('change', args=[self.object.pk])

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            pk = unquote(pk)
            try:
                self.kwargs[self.pk_url_kwarg] = self.model._meta.pk.to_python(pk)
            except (ValidationError, ValueError):
                raise Http404
        obj = super().get_object()

        if not self.has_view_permission(self.request, obj):
            raise PermissionDenied

        return obj

    def get_template_names(self):
        """
        List of templates for the view.
        If no `self.template_name` defined, uses::
             [<app_label>/<model_label>_detail.html,
              'material/views/confirm_delete.html']
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                'material/views/detail.html',
            ]
        return [self.template_name]
