import datetime
import decimal

from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.forms.forms import pretty_name
from django.utils import formats, timezone
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.views import generic

from material.ptml import Icon


def _get_attr_header(obj_class, attr_name):
    attr = getattr(obj_class, attr_name)
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
        return pretty_name(attr_name)


def _get_attr_type(obj_class, attr_name):
    attr = getattr(obj_class, attr_name)
    if hasattr(attr, "column_type"):
        return attr.align
    elif isinstance(attr, property) and hasattr(attr, "fget"):
        if hasattr(attr.fget, "column_type"):
            return attr.fget.align
    return 'text'


def _get_attr_empty_value(obj_class, attr_name):
    attr = getattr(obj_class, attr_name)
    if hasattr(attr, "empty_value"):
        return attr.align
    elif isinstance(attr, property) and hasattr(attr, "fget"):
        if hasattr(attr.fget, "empty_value"):
            return attr.fget.empty_value
    return None


def _get_attr_boolean(obj_class, attr_name):
    attr = getattr(obj_class, attr_name)
    if hasattr(attr, "boolean"):
        return attr.boolean
    elif isinstance(attr, property) and hasattr(attr, "fget"):
        if hasattr(attr.fget, "boolean"):
            return attr.fget.boolean
    return False


class BaseColumn(object):
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def get_value(self, obj):
        raise NotImplementedError('subclasses must implement this method.')

    def header(self):
        raise NotImplementedError('subclasses must implement this method')

    def column_type(self):
        raise NotImplementedError('subclasses must implement this method')

    def format_value(self, value):
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

    def format_value(self, value):
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
            return super().format_value(value)


class ObjectAttrColumn(BaseColumn):
    """
    Retrieve attribute value from a model instance.

    If object attribute is a callable, to get the value it would be
    called without any arguments.
    """
    def __init__(self, obj_class, attr_name, header=None):
        super().__init__(attr_name)
        self.obj_class = obj_class
        self._header = header

    def get_value(self, obj):
        attr = getattr(obj, self.attr_name)
        if callable(attr):
            return attr()
        return attr

    def header(self):
        if self._header:
            return self._header
        return _get_attr_header(self.obj_class, self.attr_name)

    def column_type(self):
        return _get_attr_type(self.obj_class, self.attr_name)

    def format_value(self, value):
        if _get_attr_boolean(self.obj_class, self.attr_name):
            if value is None:
                return Icon('indeterminate_check_box')
            elif value is True:
                return Icon('check_box')
            else:
                return Icon('check_box_outline_blank')
        else:
            return super().format_value(value)


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

    def get_value(self, obj):
        attr = getattr(self.data_source, self.attr_name)
        if callable(attr):
            return attr(obj)
        return attr

    def header(self):
        return _get_attr_header(self.data_source, self.attr_name)

    def column_type(self):
        return _get_attr_type(self.data_source, self.attr_name)

    def format_value(self, value):
        if _get_attr_boolean(self.data_source, self.attr_name):
            if value is None:
                return Icon('indeterminate_check_box')
            elif value is True:
                return Icon('check_box')
            else:
                return Icon('check_box_outline_blank')
        else:
            return super().format_value(value)


class ListModelView(generic.ListView):
    viewset = None
    columns = None
    paginate_by = 25

    empty_value_display = ""

    def get_columns(self):
        if self.columns is None:
            return ['__str__']
        return self.columns

    def get_column(self, attr_name):
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
        if hasattr(self.object_list.model, attr_name):
            return ObjectAttrColumn(self.model, attr_name)

    @cached_property
    def list_columns(self):
        return [self.get_column(column_name) for column_name in self.get_columns()]

    def get_page_data(self, page):
        """"Formated page data for a table.

       Returned data is a list of list of cell values zipped with column definitions.
       [[(column, value), (column, value), ...], ...]
        """
        for obj in page:
            yield [
                (column, self.format_value(column, column.get_value(obj)))
                for column in self.list_columns
            ]

    def format_value(self, column, value):
        return column.format_value(value)

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
