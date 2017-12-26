from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.views import generic

from material.viewset import viewprop

from .base import FormLayoutMixin


class CreateModelView(FormLayoutMixin, generic.CreateView):
    viewset = None
    layout = None
    template_name_suffix = '_create'

    def has_add_permission(self, request):
        if self.viewset is not None:
            return self.viewset.has_add_permission(request)
        else:
            return request.user.has_perm(
                auth.get_permission_codename('add', self.model._meta)
            )

    @viewprop
    def queryset(self):
        if self.viewset is not None and hasattr(self.viewset, 'get_queryset'):
            return self.viewset.get_queryset(self.request)
        return None

    def get_template_names(self):
        """
        List of templates for the view.
        If no `self.template_name` defined, uses::
             [<app_label>/<model_label>_<suffix>.html,
              <app_label>/<model_label>_form.html,
              'material/views/form.html']
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                '{}/{}_form.html'.format(opts.app_label, opts.model_name),
                'material/views/form.html',
            ]

    def dispatch(self, request, *args, **kwargs):
        if not self.has_add_permission(self.request):
            raise PermissionDenied

        return super(CreateModelView, self).dispatch(request, *args, **kwargs)
