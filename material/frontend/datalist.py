from __future__ import unicode_literals

from collections import OrderedDict

from django.core.exceptions import FieldDoesNotExist
from django.utils.encoding import smart_text
from django.forms.forms import pretty_name


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
    def __init__(self, field):
        self.field = field

    def get_value(self, obj):
        return getattr(obj, self.field.name)

    @property
    def label(self):
        try:
            return self.field.verbose_name
        except AttributeError:
            # field is likely a ForeignObjectRel
            return self.field.related_model._meta.verbose_name


class ModelAttr(object):
    def __init__(self, model, name, label=None):
        self.model = model
        self.name = name
        self._label = label

    def get_value(self, obj):
        attr = getattr(obj, self.name)
        if callable(attr):
            return attr()
        return attr

    @property
    def label(self):
        if self._label:
            return self._label
        return _get_attr_label(self.model, self.name)


class DataSourceAttr(object):
    def __init__(self, data_source, name):
        self.data_source = data_source
        self.name = name

    def get_value(self, obj):
        attr = getattr(self.data_source, self.name)
        if callable(attr):
            return attr(obj)
        return attr

    @property
    def label(self):
        return _get_attr_label(self.data_source, self.name)


class DataList(object):
    def __init__(self, model, queryset, data_sources=None, list_display=None, list_display_links=None):
        self.model = model
        self.queryset = queryset
        self.data_sources = data_sources if data_sources else []

        self.list_display = list_display if list_display else ('__str__', )

        if list_display_links:
            self.list_display_links = list_display_links
        else:
            # Use only the first item in list_display as link
            list_display_links = list(self.list_display)[:1]

    def get_data_attr(self, attr_name):
        opts = self.model._meta
        try:
            return ModelField(opts.get_field(attr_name))
        except FieldDoesNotExist:
            if attr_name == "__str__":
                return ModelAttr(self.model, attr_name, opts.verbose_name)
            else:
                for data_source in self.data_sources:
                    if hasattr(data_source, attr_name):
                        return DataSourceAttr(data_source, attr_name)

        raise AttributeError("Unable to lookup '{}' on {}" .format(attr_name, self.model._meta.object_name))

    def total(self):
        return self.queryset.count()

    def total_filtered(self):
        return self.queryset.count()

    def set_filter(self):
        """
        TODO
        """

    def set_ordering(self):
        """
        TODO
        """

    def get_headers_data(self):
        for field_name in self.list_display:
            attr = self.get_data_attr(field_name)
            yield field_name, attr.label

    def get_data(self, start, length):
        for item in self.queryset[start:start+length]:
            columns = OrderedDict()
            for n, field_name in enumerate(self.list_display):
                attr = self.get_data_attr(field_name)
                columns[field_name] = smart_text(attr.get_value(item))
            yield item, columns
