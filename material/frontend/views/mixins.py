from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse


class ModelViewMixin(object):
    viewset = None
    layout = None

    def __init__(self, *args, **kwargs):
        super(ModelViewMixin, self).__init__(*args, **kwargs)
        if self.form_class is None and self.fields is None:
            self.fields = '__all__'

    def has_object_permission(self, request, obj):
        raise NotImplementedError

    def get_object(self):
        obj = super(ModelViewMixin, self).get_object()
        if not self.has_object_permission(self.request, obj):
            raise PermissionDenied
        return obj

    def get_success_url(self):
        if self.success_url is None:
            opts = self.model._meta
            return reverse('{}:{}_list'.format(opts.app_label, opts.model_name))
        return super(ModelViewMixin, self).get_success_url()

    def get_template_names(self):
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                '{}/{}_form.html'.format(opts.app_label, opts.model_name),
                'material/frontend/views/form.html',
            ]

        return [self.template_name]
