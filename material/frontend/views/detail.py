from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.db import models
from django.views import generic


class DetailModelView(generic.DetailView):
    viewset = None

    def get_object_data(self):
        for field in self.object._meta.fields:
            if isinstance(field, models.AutoField):
                continue
            elif field.auto_created:
                continue
            else:
                choice_display_attr = "get_{}_display".format(field.get_attname())
            if hasattr(self.object, choice_display_attr):
                value = getattr(self.object, choice_display_attr)()
            else:
                value = getattr(self.object, field.get_attname())

                if value is not None:
                    yield (field.verbose_name.title(), value)

    def has_view_permission(self, request, obj):
        if self.viewset is not None:
            return self.viewset.has_view_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')

    def has_change_permission(self, request, obj):
        if self.viewset is not None:
            return self.viewset.has_change_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')

    def has_delete_permission(self, request, obj):
        if self.viewset is not None:
            return self.viewset.has_delete_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')

    def get_object(self):
        obj = super(DetailModelView, self).get_object()
        if not self.has_view_permission(self.request, obj):
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        opts = self.model._meta

        kwargs['object_data'] = self.get_object_data()
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
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                'material/frontend/views/detail.html',
            ]

        return [self.template_name]
