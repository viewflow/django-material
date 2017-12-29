from django.contrib import auth, messages
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied, ValidationError
from django.forms.models import modelform_factory
from django.http import Http404
from django.utils.html import format_html
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from material.viewset import viewprop

from .base import FormLayoutMixin


class UpdateModelView(FormLayoutMixin, generic.UpdateView):
    viewset = None
    layout = None
    form_widgets = None

    def has_change_permission(self, request, obj=None):
        if self.viewset is not None:
            return self.viewset.has_change_permission(request, obj=obj)
        else:
            change_perm = auth.get_permission_codename('change', self.model._meta)

            if request.user.has_perm(change_perm):
                return True
            else:
                return request.user.has_perm(change_perm, obj=obj)

    def get_object_url(self, obj):
        if self.viewset is not None and hasattr(self.viewset, 'get_object_link'):
            return self.viewset.get_object_link(self.request, obj)
        elif hasattr(obj, 'get_absolute_url'):
            if self.has_change_permission(self.request, obj):
                return obj.get_absolute_url()

    def message_user(self):
        url = self.get_object_url(self.object)
        link = ''
        if url:
            link = format_html('<a href="{}">{}</a>', urlquote(url), _('View'))

        message = format_html(
            _("The {obj} was changed successfully. {link}"),
            obj=str(self.object),
            link=link
        )
        messages.add_message(self.request, messages.SUCCESS, message, fail_silently=True)

    @viewprop
    def queryset(self):
        if self.viewset is not None and hasattr(self.viewset, 'get_queryset'):
            return self.viewset.get_queryset(self.request)
        return None

    def get_form_class(self):
        if self.form_class is None:
            return modelform_factory(self.model, fields=self.fields, widgets=self.form_widgets)
        return self.form_class

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            pk = unquote(pk)
            try:
                self.kwargs[self.pk_url_kwarg] = self.model._meta.pk.to_python(pk)
            except (ValidationError, ValueError):
                raise Http404
        obj = super().get_object()

        if not self.has_change_permission(self.request, obj):
            raise PermissionDenied

        return obj

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
        response = super(UpdateModelView, self).form_valid(*args, **kwargs)
        self.message_user()
        return response

    def get_success_url(self):
        return '/'  # TODO
