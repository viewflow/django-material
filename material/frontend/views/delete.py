from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_permission_codename
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import router
from django.db.models.deletion import Collector
from django.http import Http404
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from ...compat import _


class DeleteModelView(generic.DeleteView):
    """View for deleting an object and all linked by foreign key data."""

    viewset = None

    def has_object_permission(self, request, obj):
        """Object delete permission check.

        If view had a `viewset`, the `viewset.has_delete_permission` used.
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

    def _get_deleted_objects(self):
        collector = Collector(using=router.db_for_write(self.object))
        collector.collect([self.object])
        return collector.data

    def get_context_data(self, **kwargs):
        """Extend view context data.

        `{{ deleted_objects }}` - list of related objects to delete
        """
        kwargs.setdefault('deleted_objects', self._get_deleted_objects())
        return super(DeleteModelView, self).get_context_data(**kwargs)

    def get_object(self):
        """Retrieve the object for delete.

        Check object delete permission at the same time.
        """
        queryset = self.get_queryset()
        model = queryset.model
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            try:
                self.kwargs[self.pk_url_kwarg] = model._meta.pk.to_python(pk)
            except (ValidationError, ValueError):
                raise Http404

        obj = super(DeleteModelView, self).get_object()
        if not self.has_object_permission(self.request, obj):
            raise PermissionDenied
        return obj

    def get_success_url(self):
        """Redirect back to the list view if no `success_url` is configured."""
        if self.success_url is None:
            opts = self.model._meta
            return reverse('{}:{}_list'.format(opts.app_label, opts.model_name))
        return super(DeleteModelView, self).get_success_url()

    def get_template_names(self):
        """
        List of templates for the view.

        If no `self.template_name` defined, uses::

             [<app_label>/<model_label>_delete.html,
              'material/frontend/views/confirm_delete.html']
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                'material/frontend/views/confirm_delete.html',
            ]

        return [self.template_name]

    def delete(self, request, *args, **kwargs):
        response = super(DeleteModelView, self).delete(request, *args, **kwargs)
        self.message_user()
        return response

    def message_user(self):
        message = _('The {name} "{link}"  was deleted successfully.'.format(
            name=force_text(self.model._meta.verbose_name),
            link=force_text(self.object)
        ))
        messages.add_message(self.request, messages.SUCCESS, message, fail_silently=True)
