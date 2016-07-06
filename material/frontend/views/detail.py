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

    def has_object_permission(self, request, obj):
        if self.viewset is not None:
            return self.viewset.has_view_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')

    def get_object(self):
        obj = super(DetailModelView, self).get_object()
        if not self.has_object_permission(self.request, obj):
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        if 'opts' not in kwargs:
            kwargs['opts'] = self.model._meta
        kwargs['object_data'] = self.get_object_data()
        return super(DetailModelView, self).get_context_data(**kwargs)

    def get_template_names(self):
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                'material/frontend/views/detail.html',
            ]

        return [self.template_name]
