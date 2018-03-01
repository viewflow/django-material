import datetime
import decimal
from functools import lru_cache

from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.db import models
from django.forms.forms import pretty_name
from django.utils import formats, timezone
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.views import generic

from material.ptml import Icon
from material.viewset import viewprop

from .base import has_object_perm


def _get_method_attr(data_source, method_name, attr_name, default=None):
    attr = getattr(data_source, method_name)
    try:
        return getattr(attr, attr_name)
    except AttributeError:
        if isinstance(attr, property) and hasattr(attr, "fget"):
            return getattr(attr.fget, attr_name, default)
    return default


class BaseColumn(object):
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def get_value(self, obj):
        raise NotImplementedError('subclasses must implement this method.')

    def header(self):
        raise NotImplementedError('subclasses must implement this method')

    def column_type(self):
        raise NotImplementedError('subclasses must implement this method')

    def format_value(self, obj, value):
        if value is None:
            return ''
        elif isinstance(value, datetime.datetime):
            return formats.localize(timezone.template_localtime(value))
        elif isinstance(value, (datetime.date, datetime.time)):
            return formats.localize(value)
        elif isinstance(value, (int, float, decimal.Decimal)):
            return formats.number_format(value)
        elif isinstance(value, (list, tuple)):
            return ', '.join(force_text(v) for v in value)
        else:
            return force_text(value)


class ModelFieldColumn(BaseColumn):
    """
    Retrieve a field value from a model.

    Field verbose name would be use as a label.
    """
    def __init__(self, model_field):
        super().__init__(model_field.name)
        self.model_field = model_field

    def get_value(self, obj):
        return getattr(obj, self.model_field.name)

    def header(self):
        try:
            return self.model_field.verbose_name.capitalize()
        except AttributeError:
            # field is likely a ForeignObjectRel
            return self.model_field.related_model._meta.verbose_name.capitalize()

    def column_type(self):
        number_field_types = (
            models.IntegerField,
            models.DecimalField,
            models.FloatField,
        )
        if isinstance(self.model_field, number_field_types):
            return 'numeric'
        return 'text'

    def format_value(self, obj, value):
        boolean_field_types = (models.BooleanField, models.NullBooleanField)

        if getattr(self.model_field, 'flatchoices', None):
            return dict(self.model_field.flatchoices).get(value, '')
        elif isinstance(self.model_field, boolean_field_types):
            if value is None:
                return Icon('indeterminate_check_box')
            elif value is True:
                return Icon('check_box')
            else:
                return Icon('check_box_outline_blank')
        else:
            return super().format_value(obj, value)


class DataSourceColumn(BaseColumn):
    """
    Retrieve attribute value from external data source.

    Data source attribute could be a property or callable.
    For a callable, to get the value it would be called with model
    instance.
    """
    def __init__(self, data_source, attr_name):
        super().__init__(attr_name)
        self.data_source = data_source

    def _get_attr_boolean(self):
        return _get_method_attr(self.data_source, self.attr_name, 'boolean', False)

    def _get_attr_empty_value(self):
        return _get_method_attr(self.data_source, self.attr_name, 'empty_value')

    def get_value(self, obj):
        attr = getattr(self.data_source, self.attr_name)
        if callable(attr):
            attr = attr(obj)
        if attr is None:
            attr = self._get_attr_empty_value()
        return attr

    def header(self):
        attr = getattr(self.data_source, self.attr_name)
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
            return pretty_name(self.attr_name)

    def column_type(self):
        return _get_method_attr(self.data_source, self.attr_name, 'column_type', 'text')

    def format_value(self, obj, value):
        if self._get_attr_boolean():
            if value is None:
                return Icon('indeterminate_check_box')
            elif value is True:
                return Icon('check_box')
            else:
                return Icon('check_box_outline_blank')
        else:
            return super().format_value(obj, value)


class ObjectAttrColumn(DataSourceColumn):
    """
    Retrieve attribute value from a model instance.

    If object attribute is a callable, to get the value it would be
    called without any arguments.
    """
    def get_value(self, obj):
        attr = getattr(obj, self.attr_name)
        if callable(attr):
            return attr()
        return attr


class BaseListModelView(generic.ListView):
    viewset = None
    columns = None
    object_link_columns = None
    paginate_by = 25

    page_actions = None

    empty_value_display = ""

    def has_view_permission(self, request, obj=None):
        if self.viewset is not None:
            return self.viewset.has_view_permission(request, obj=obj)
        else:
            return (
                has_object_perm(request.user, 'view', self.model, obj=obj) or
                has_object_perm(request.user, 'change', self.model, obj=obj)
            )

    def get_columns(self):
        if self.columns is None:
            return ['__str__']
        return self.columns

    @lru_cache(maxsize=None)
    def get_object_link_columns(self):
        if self.object_link_columns is None:
            return self.columns[0]
        return self.object_link_columns

    def get_column_def(self, attr_name):
        opts = self.model._meta

        # an object field
        try:
            model_field = opts.get_field(attr_name)
        except FieldDoesNotExist:
            pass
        else:
            return ModelFieldColumn(model_field)

        # object printable string representation
        if attr_name == "__str__":
            return ObjectAttrColumn(self.model, attr_name, opts.verbose_name.capitalize())

        # a method from view or viewset
        data_sources = [self, self.viewset] if self.viewset is not None else [self]
        for data_source in data_sources:
            if hasattr(data_source, attr_name):
                return DataSourceColumn(data_source, attr_name)

        # a method from object
        if hasattr(self.model, attr_name):
            return ObjectAttrColumn(self.model, attr_name)

    def get_object_url(self, obj):
        if self.viewset is not None and hasattr(self.viewset, 'get_object_url'):
            return self.viewset.get_object_url(self.request, obj)
        else:
            if hasattr(obj, 'get_absolute_url') and self.has_view_perm(self.request, obj):
                return obj.get_absolute_url()

    @cached_property
    def list_columns_defs(self):
        return [self.get_column_def(column_name) for column_name in self.get_columns()]

    def get_column_data(self, column_def):
        return {
            'column_def': column_def,
            'column_type': column_def.column_type,
            'header': column_def.header
        }

    def get_columns_data(self):
        return [
            self.get_column_data(column_def)
            for column_def in self.list_columns_defs
        ]

    def format_value(self, obj, column, value):
        result = column.format_value(obj, value)
        if column.attr_name in self.get_object_link_columns():
            url = self.get_object_url(obj)
            if url:
                result = format_html('<a href="{}">{}</a>', url, result)
        return result
    def get_page_data(self, page):
        """"Formated page data for a table.

       Returned data is a list of list of cell values zipped with column definitions.
       [[(column, value), (column, value), ...], ...]
        """
        for obj in page:
            yield [
                (column_def, self.format_value(obj, column_def, column_def.get_value(obj)))
                for column_def in self.list_columns_defs
            ]

    def get_page_actions(self, *actions):
        if self.viewset is not None and hasattr(self.viewset, 'get_list_page_actions'):
            actions = self.viewset.get_list_page_actions(self.request) + actions
        if self.page_actions:
            actions = self.page_actions + actions
        return actions

    @viewprop
    def queryset(self):
        if self.viewset is not None and hasattr(self.viewset, 'get_queryset'):
            return self.viewset.get_queryset(self.request)
        return None

    def get_template_names(self):
        """
        Return a list of template names to be used for the view.

        If `self.template_name` undefined, uses::
             [<app_label>/<model_label>_list.html,
              'material/views/list.html']
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                'material/views/list.html',
            ]
        return [self.template_name]

    def dispatch(self, request, *args, **kwargs):
        if not self.has_view_permission(self.request):
            raise PermissionDenied

        return super(BaseListModelView, self).dispatch(request, *args, **kwargs)


class ListModelView(BaseListModelView):
    """
    Render some list of objects.
    """
