from django.contrib import auth
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.forms.models import modelform_factory
from django.views import generic

from material.viewset import viewprop

from .base import FormLayoutMixin


class CreateModelView(FormLayoutMixin, generic.CreateView):
    viewset = None
    layout = None  # todo samples
    form_widgets = None

    template_name_suffix = '_create'

    def has_add_permission(self, request):
        if self.viewset is not None:
            return self.viewset.has_add_permission(request)
        else:
            return request.user.has_perm(
                auth.get_permission_codename('add', self.model._meta)
            )

    def message_user(self):
        pass

    @viewprop
    def queryset(self):
        if self.viewset is not None and hasattr(self.viewset, 'get_queryset'):
            return self.viewset.get_queryset(self.request)
        return None

    def get_form_class(self):
        if self.form_class is None:
            return modelform_factory(self.model, fields=self.fields, widgets=self.form_widgets)
        return self.form_class

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

    def form_valid(self, *args, **kwargs):
        response = super(CreateModelView, self).form_valid(*args, **kwargs)
        self.message_user()
        return response

    def get_success_url(self):
        return '/'  # TODO

    def dispatch(self, request, *args, **kwargs):
        if not self.has_add_permission(self.request):
            raise PermissionDenied

        return super(CreateModelView, self).dispatch(request, *args, **kwargs)
