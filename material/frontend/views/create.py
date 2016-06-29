from django.core.urlresolvers import reverse
from django.views.generic import CreateView


class CreateModelView(CreateView):
    def __init__(self, *args, **kwargs):
        super(CreateModelView, self).__init__(*args, **kwargs)
        if self.form_class is None and self.fields is None:
            self.fields = '__all__'

    @classmethod
    def has_perm(cls, user):
        return True

    def get_success_url(self):
        if self.success_url is None:
            opts = self.model._meta
            return reverse('{}:{}_list'.format(opts.app_label, opts.model_name))

        return super(CreateModelView, self).get_success_url()

    def get_template_names(self):
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                '{}/{}_form.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                'material/frontend/views/create.html',
            ]
        return [self.template_name]
