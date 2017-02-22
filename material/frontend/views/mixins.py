from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.http import urlquote
from django.utils.translation import ugettext as _


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

    def get_queryset(self):
        """Return the list of items for this view.

        If view have no explicit `self.queryset`, tries too lookup to
        `viewflow.get_queryset`
        """
        if self.queryset is None and self.viewset is not None:
            if hasattr(self.viewset, 'get_queryset'):
                queryset = self.viewset.get_queryset(self.request)
                ordering = self.get_ordering()
                if ordering:
                    if isinstance(ordering, six.string_types):
                        ordering = (ordering,)
                    queryset = queryset.order_by(*ordering)
                return queryset
        return super(ModelViewMixin, self).get_queryset()

    def get_object(self):
        """Retreive an object and check user permissions."""
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

    def form_valid(self, *args, **kwargs):
        response = super(ModelViewMixin, self).form_valid(*args, **kwargs)
        self.message_user()
        return response

    def message_user(self):
        """Successful notification.

        Subclasses can override it.
        """


class MessageUserMixin(object):
    """User notification utilities django.messages framework.'"""

    def report(self, message, level=messages.INFO, fail_silently=True, **kwargs):
        """Construct message and notify the user."""
        opts = self.model._meta

        url = reverse('{}:{}_detail'.format(
            opts.app_label, opts.model_name), args=[self.object.pk])
        link = format_html('<a href="{}">{}</a>', urlquote(url), force_text(self.object))
        name = force_text(opts.verbose_name)

        options = {
            'link': link,
            'name': name
        }
        options.update(kwargs)
        message = format_html(_(message).format(**options))
        messages.add_message(self.request, messages.SUCCESS, message, fail_silently=True)

    def success(self, message, fail_silently=True, **kwargs):
        self.report(message, level=messages.SUCCESS, fail_silently=fail_silently, **kwargs)

    def error(self, message, fail_silently=True, **kwargs):
        self.report(message, level=messages.ERROR, fail_silently=fail_silently, **kwargs)
