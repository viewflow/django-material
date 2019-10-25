from __future__ import unicode_literals

from django.contrib.auth import get_permission_codename
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from ...compat import _
from .mixins import MessageUserMixin, ModelViewMixin


class UpdateModelView(MessageUserMixin, ModelViewMixin, generic.UpdateView):
    """Thin `generic.UpdateView` wrapper plays nice with `ModelViewSet`."""

    template_name_suffix = '_update'

    def has_object_permission(self, request, obj):
        """Object change permission check.

        If view had a `viewset`, the `viewset.has_change_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_change_permission(request, obj)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('change', opts)
        return request.user.has_perm(
            '{}.{}'.format(opts.app_label, codename), obj=obj)

    def get_success_url(self):
        """Redirect back to the detail view if no `success_url` is configured."""
        if self.success_url is None:
            opts = self.model._meta
            return reverse('{}:{}_detail'.format(
                opts.app_label, opts.model_name), args=[self.object.pk]
            )
        return super(ModelViewMixin, self).get_success_url()

    def message_user(self):
        self.success(_('The {name} "{link}" was changed successfully.'))
