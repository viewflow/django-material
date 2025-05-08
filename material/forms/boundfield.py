# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial licence defined in file 'COMM_LICENSE',
# which is part of this source code package.

from django.forms.boundfield import BoundField


class CompositeBoundField(BoundField):
    """Adapter for bound composite fields.

    This is an emulation of the BoundField that is returned if you
    call ``form['field_name']`` for an ordinary django field. A
    ``CompositeBoundField`` will be used if you access a nested form
    or formset with ``form['nested_form']``.  The
    ``CompositeBoundField`` has the purpose of providing the same
    interface to other libraries that use a ``BoundField`` instance
    for rendering.
    """

    # __init__, no changes required
    # __str__, no changes required

    def __iter__(self):
        """Iterate over the composite field.

        For ``FormSetField`` this will return form instances. For
        ``FormField`` this will return bound form fields.
        """
        for item in self.form.get_composite_field_value(self.name):
            yield item

    # __len__, no changes required

    def __getitem__(self, item):
        """
        Access to field by name.

        Allow named access to the form fields and forms contained in the
        composite fields. For ``FormField``s you get a bound field, for
        ``FormSetField`` you can use and integer index lookup for a specific
        form.
        Examples:
        .. code:: python
            # Gives ``street`` field of nested ``address`` form.
            form['address']['street']
        .. code:: django
            {# That is useful in the template as well: #}
            {{ form.address.street }}
        """
        composite_item = self.form.get_composite_field_value(self.name)
        return composite_item[item]

    def __bool__(self):
        """Never evaluate the bound field as False.

        This is necessary since otherwise python will fallback to the
        __len__ implementation of the object. However this might
        return 0 for a ``CompositeBoundField`` since it might contain
        zero forms in the given formset.
        """
        return True

    # Python 2's __bool__ is called __nonzero__.
    __nonzero__ = __bool__

    @property
    def errors(self):
        """Return an ErrorList for this field.

        Either the errors of the contained formset or of the inlined
        form.
        """
        # TODO: We could make this work and return the forms/formsets errors.
        return self.form.error_class()

    # as_widget, no changes required

    def as_text(self, attrs=None, **kwargs):
        """Not supported.

        This does not make sense for a CompositeBoundField.  Will
        raise ``NotImplementedError``.

        """
        raise NotImplementedError

    def as_textarea(self, attrs=None, **kwargs):
        """Not supported.

        This does not make sense for a CompositeBoundField.
        Will raise ``NotImplementedError``.

        """
        raise NotImplementedError

    def as_hidden(self, attrs=None, **kwargs):
        """
        Raise ``NotImplementedError``.

        An implementation might be useful, which could return a string of HTML
        for representing the nested form or formsets as multiple <input
        type="hidden">.
        Pull request are welcome.
        """
        # TODO: This might make sense. But we don't support it yet.
        raise NotImplementedError

    @property
    def data(self):
        """
        Return ``None`` always.

        This doesn't make much sense for a ``CompositeField``.
        """
        return None

    def value(self):
        """Return the form/formset for this BoundField.

        This is passed into the call for ``self.widget.render`` in the
        ``as_widget`` method.
        """
        return self.form.get_composite_field_value(self.name)

    # label_tag, no changes required
    # auto_id, no changes required
    # id_for_label, no changes required
