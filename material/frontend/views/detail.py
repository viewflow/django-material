from django.views import generic


class DetailModelView(generic.DetailView):
    def get_template_names(self):
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                'material/frontend/views/detail.html',
            ]

        return [self.template_name]
