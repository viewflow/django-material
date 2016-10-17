from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse


class ModelViewMixin(object):
    """Mixin for generic form views to play nice with `ModelViewSet`."""

    viewset = None
    layout = None

    def __init__(self, *args, **kwargs):  # noqa D102
        super(ModelViewMixin, self).__init__(*args, **kwargs)
        if self.form_class is None and self.fields is None:
            self.fields = '__all__'

    def has_object_permission(self, request, obj):
        """Check object access permission.

        Subclasses should override it
        """
        raise NotImplementedError

    def get_object(self):
        """Retrive an object and check user permissions."""
        obj = super(ModelViewMixin, self).get_object()
        if not self.has_object_permission(self.request, obj):
            raise PermissionDenied
        return obj

    def get_success_url(self):
        """Redirect back to the list view if no `success_url` is configured."""
        if self.success_url is None:
            opts = self.model._meta
            return reverse('{}:{}_list'.format(
                opts.app_label, opts.model_name)
            )
        return super(ModelViewMixin, self).get_success_url()

    def get_template_names(self):
        """
        List of templates for the view.

        If no `self.template_name` defined, uses::

             [<app_label>/<model_label>_<suffix>.html,
              <app_label>/<model_label>_form.html,
              'material/frontend/views/form.html']
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(
                    opts.app_label,
                    opts.model_name,
                    self.template_name_suffix),
                '{}/{}_form.html'.format(
                    opts.app_label,
                    opts.model_name),
                'material/frontend/views/form.html',
            ]

        return [self.template_name]
