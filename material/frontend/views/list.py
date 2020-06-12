from __future__ import unicode_literals

import datetime
import decimal
import six

from collections import OrderedDict
from copy import deepcopy

from django.contrib.auth import get_permission_codename
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldDoesNotExist
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models.query import QuerySet
from django.forms.utils import pretty_name
from django.http import JsonResponse
from django.urls import reverse
from django.utils import formats, timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, format_html
from django.views.generic import View
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from .. import forms


def _get_attr_label(owner, attr_name):
    attr = getattr(owner, attr_name)
    if hasattr(attr, "short_description"):
        return attr.short_description
    elif isinstance(attr, property) and hasattr(attr, "fget"):
        if hasattr(attr.fget, "short_description"):
            return attr.fget.short_description
        else:
            return pretty_name(attr.fget.__name__)
    elif callable(attr):
        return "--" if attr.__name__ == "<lambda>" else pretty_name(attr.__name__)
    else:
        return attr_name


class ModelField(object):
    """Retrieve a field value from the model.

    Field verbose name would be use as a label.
    """

    def __init__(self, field):  # noqa D102
        self.field = field

    def get_value(self, obj):  # noqa D102
        return getattr(obj, self.field.name)

    @property
    def label(self):  # noqa D102
        try:
            return self.field.verbose_name
        except AttributeError:
            # field is likely a ForeignObjectRel
            return self.field.related_model._meta.verbose_name

    @property
    def orderable(self):  # noqa D102
        return True


class ModelAttr(object):
    """Retrieve attribute value from the model instance.

    If model attribute is a callable, to get the value it would be
    called without any arguments.
    """

    def __init__(self, model, name, label=None):  # noqa D102
        self.model = model
        self.name = name
        self._label = label

    def get_value(self, obj):  # noqa D102
        attr = getattr(obj, self.name)
        if callable(attr):
            return attr()
        return attr

    @property
    def label(self):  # noqa D102
        if self._label:
            return self._label
        return _get_attr_label(self.model, self.name)

    @property
    def orderable(self):  # noqa D102
        return False


class DataSourceAttr(object):
    """Retrieve attribute value from external data source.

    Data source attribute could be a property or callable.

    For a callable, to get the value it would be called with model
    instance.
    """

    def __init__(self, data_source, name):  # noqa D102
        self.data_source = data_source
        self.name = name

    def get_value(self, obj):  # noqa D102
        attr = getattr(self.data_source, self.name)
        if callable(attr):
            return attr(obj)
        return attr

    @property
    def label(self):
        """Retrieve the label for the data source attribute.

        Label could be specified in `.short_description` or the
        attribute name would be used.

        Example::

        class SampleDataSource(object):
            def description(self, model):
                return "Sample for {}".format(model)
            description.short_description = "Model Description"

        """
        return _get_attr_label(self.data_source, self.name)

    @property
    def orderable(self):  # noqa D102
        return False


class DataTableMixin(ContextMixin):
    """Mixing for list views with DataTable."""

    datatable_config = None
    datatable_default_config = {
        'processing': False,
        'serverSide': True,
        'ajax': {
            'url': '.',
        },
        'order': [],
        'ordering': True,
        'orderMulti': True,
        'info': False,
        'bFilter': False,
        'bAutoWidth': True,
        'bLengthChange': False,
        'oLanguage': {
            'oPaginate': {
                'sFirst': "",
                'sLast': "",
                'sNext': "&rang;",
                'sPrevious': "&lang;",
            }
        },
        'responsive': {
            'details': False
        }
    }
    list_display = ('__str__', )
    empty_value_display = ""
    ordering = None
    viewset = None
    paginate_by = 15

    def get_context_data(self, **kwargs):
        """Update view context.

        Include `datatable_config`, 'headers' and initial `data` to
        first page render.
        """
        context = super(DataTableMixin, self).get_context_data(**kwargs)
        context.update({
            'datatable_config': self.get_datatable_config(),
            'headers': self.get_headers_data(),
            'data': self.get_table_data(0, self.paginate_by),
        })

        return context

    def get_list_display(self):
        """Return list of columns to display."""
        return self.list_display

    def get_datatable_config(self):
        """Prepare datatable config."""
        config = deepcopy(self.datatable_default_config)
        config['pageLength'] = self.paginate_by
        config['ajax']['url'] = self.request.path
        config['columns'] = self.get_columns_def()

        if self.ordering:
            datatable_ordering = []
            columns = self.get_list_display()

            for column in self.ordering:
                idx = columns.index(column.strip('-'))
                datatable_ordering.append([idx, 'asc' if column.startswith('-') else 'desc'])
            config['order'] = datatable_ordering

        if self.datatable_config is not None:
            config.update(self.datatable_config)
        return config

    def get_data_attr(self, attr_name):
        """Data getter for an attribute.

        Data could comes from the model field or external `data_source`
        method call.
        """
        opts = self.object_list.model._meta
        try:
            return ModelField(opts.get_field(attr_name))
        except FieldDoesNotExist:
            if attr_name == "__str__":
                return ModelAttr(self.object_list.model, attr_name, opts.verbose_name)
            else:
                data_sources = [self, self.viewset] if self.viewset is not None else [self]
                for data_source in data_sources:
                    if hasattr(data_source, attr_name):
                        return DataSourceAttr(data_source, attr_name)
            if hasattr(self.object_list.model, attr_name):
                return ModelAttr(self.object_list.model, attr_name)
        raise AttributeError("Unable to lookup '{}' on {}" .format(
            attr_name, self.object_list.model._meta.object_name)
        )

    def get_columns_def(self):
        """Return columns definition for the datables js config."""
        return [
            {'data': field_name, 'orderable': self.get_data_attr(field_name).orderable}
            for field_name in self.get_list_display()
        ]

    def get_headers_data(self):
        """Readable column titles."""
        for field_name in self.get_list_display():
            attr = self.get_data_attr(field_name)
            yield field_name, attr.label

    def format_column(self, item, field_name, value):
        if value is None:
            return self.empty_value_display
        elif isinstance(value, datetime.datetime):
            return formats.localize(timezone.template_localtime(value))
        elif isinstance(value, (datetime.date, datetime.time)):
            return formats.localize(value)
        elif isinstance(value, six.integer_types + (decimal.Decimal, float)):
            return formats.number_format(value)
        elif isinstance(value, (list, tuple)):
            return ', '.join(force_text(v) for v in value)
        else:
            return force_text(value)

    def get_table_data(self, start, length):
        """Get a page for datatable."""
        for item in self.object_list[start:start + length]:
            columns = OrderedDict()
            for n, field_name in enumerate(self.get_list_display()):
                attr = self.get_data_attr(field_name)
                value = self.format_column(item, field_name, attr.get_value(item))
                columns[field_name] = value
            yield item, columns

    def total(self):
        """Total dataset size."""
        return self.object_list.count()

    def total_filtered(self):
        """Dataset size with filter applied."""
        return self.object_list.count()

    def get_ordering(self):
        """Return the field or fields to use for ordering the queryset."""
        if self.request_form.is_valid():
            ordering = []
            requested_order = self.request_form.cleaned_data['ordering']
            for spec in requested_order:
                column_num, column_dir = spec.get('column', 0), spec.get('dir', 'asc')

                try:
                    order = self.get_list_display()[int(column_num)]
                    if column_dir == 'asc':
                        order = '-' + order
                except (IndexError, TypeError):
                    """ Skip """
                else:
                    ordering.append(order)
            return ordering
        else:
            return self.ordering

    def get(self, request, *args, **kwargs):
        """Response with rendered html template."""
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_json_data(self, request, *args, **kwargs):
        """Return `JSONResponse` with data for datatable."""
        if not self.request_form.is_valid():
            return JsonResponse({'error': self.request_form.errors})

        draw = self.request_form.cleaned_data['draw']
        start = self.request_form.cleaned_data['start']
        length = self.request_form.cleaned_data['length']

        result = []
        for item, columns_data in self.get_table_data(start, length):
            for header, data in columns_data.items():
                columns_data[header] = conditional_escape(data)
            result.append(columns_data)

        data = {
            "draw": draw,
            "recordsTotal": self.total(),
            "recordsFiltered": self.total_filtered(),
            "data": result
        }

        return JsonResponse(data)

    def get_object_list(self):
        """Create prepared queryset for datatables view."""
        return self.get_queryset()

    def dispatch(self, request, *args, **kwargs):
        """Handle for browser HTTP and AJAX requests from datatables."""
        self.request_form = forms.DatatableRequestForm(request.GET, prefix='datatable')
        self.object_list = self.get_object_list()
        if 'HTTP_DATATABLE' in request.META:
            handler = self.get_json_data
        elif request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class ListModelView(TemplateResponseMixin, DataTableMixin, View):
    """List view suitable to work with jQuery Datatables.

    The view responsive for handling GET/POST requests from the browser
    and AJAX from the datatable.

    :keyword model: Model class views

    :keyword queryset: Base views queryset

    :keyword paginate_by: Page size

    :keyword ordering: Default list order

    :keyword datatable_config: Datatable default config overrides

    :keyword list_display: List of fields to display

    :keyword list_display_links: List of fields form `list_display`
                                 linked to change view

    """

    model = None
    queryset = None
    template_name_suffix = '_list'
    list_display_links = ()

    def has_view_permission(self, request, obj=None):
        """Object view permission check.

        If view had a `viewset`, the `viewset.has_view_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_view_permission(request, obj)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('view', opts)
        view_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(view_perm):
            return True
        elif request.user.has_perm(view_perm, obj=obj):
            return True
        return self.has_change_permission(request, obj=obj)

    def has_change_permission(self, request, obj=None):
        """Object change permission check.

        If view had a `viewset`, the `viewset.has_change_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_change_permission(request, obj)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('change', opts)
        change_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(change_perm):
            return True
        return request.user.has_perm(change_perm, obj=obj)

    def has_add_permission(self, request):
        """Object add permission check.

        If view had a `viewset`, the `viewset.has_add_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_add_permission(request)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('add', opts)
        return request.user.has_perm('{}.{}'.format(opts.app_label, codename))

    def get_template_names(self):
        """
        List of templates for the view.

        If no `self.template_name` defined, uses::

             [<app_label>/<model_label>_list.html,
              'material/frontend/views/list.html']
        """
        if self.template_name is None:
            opts = self.object_list.model._meta
            return [
                '{}/{}{}.html'.format(
                    opts.app_label,
                    opts.model_name,
                    self.template_name_suffix),
                'material/frontend/views/list.html',
            ]
        return [self.template_name]

    def get_list_display_links(self, list_display):
        """Return columns list that would be linked to the object details.

        If `self.list_display_links` is not set, the first column would be used.
        """
        if (self.list_display_links or
                self.list_display_links is None or
                not list_display):
            return self.list_display_links
        else:
            # Use only the first item in list_display as link
            return list(list_display)[:1]

    def get_queryset(self):
        """Retrieve the view queryset."""
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.viewset is not None and hasattr(self.viewset, 'get_queryset'):
            queryset = self.viewset.get_queryset(self.request)
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                })
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

    def format_column(self, item, field_name, value):
        if isinstance(value, bool):
            return format_html('<i class="material-icons">{}</i>'.format(
                'check' if value else 'close'
            ))
        else:
            formatted = super(ListModelView, self).format_column(item, field_name, value)
            if field_name in self.get_list_display_links(self.get_list_display()):
                formatted = format_html('<a href="{}">{}</a>', self.get_item_url(item), formatted)
            return formatted

    def get_item_url(self, item):
        """Link to object detail to `list_display_links` columns."""
        opts = self.model._meta
        return reverse(
            '{}:{}_detail'.format(opts.app_label, opts.model_name),
            args=[item.pk])

    def get_context_data(self, **kwargs):
        """Additional context data for list view.

        :keyword add_url: Link to the add view
        """
        opts = self.model._meta

        if self.has_add_permission(self.request):
            kwargs['add_url'] = reverse('{}:{}_add'.format(opts.app_label, opts.model_name))

        return super(ListModelView, self).get_context_data(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Handle for browser HTTP and AJAX requests from datatables."""
        if not self.has_view_permission(self.request):
            raise PermissionDenied

        return super(ListModelView, self).dispatch(request, *args, **kwargs)
