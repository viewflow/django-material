from django.views import generic


class ListModelView(generic.ListView):
    viewset = None

    def get_template_names(self):
        """
        Return a list of template names to be used for the view.

        If `self.template_name` undefined, uses::
             [<app_label>/<model_label>_list.html,
              'material/views/list.html']
        """
        if self.template_name is None:
            if hasattr(self.object_list, 'model'):
                opts = self.object_list.model._meta
                return [
                    '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                    'material/views/list.html',
                ]
        return [self.template_name]
