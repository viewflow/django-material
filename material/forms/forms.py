# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

import copy
from collections import OrderedDict
from functools import reduce

from django import forms
from django.forms.forms import DeclarativeFieldsMetaclass, ErrorList
from django.forms.utils import ErrorDict
from django.forms.models import ModelFormMetaclass as BaseModelFormMetaclass

from .fields import CompositeField


class DeclarativeCompositeFieldsMetaclass(DeclarativeFieldsMetaclass):
    """
    Metaclass that converts FormField and FormSetField attributes to a
    dictionary called `composite_fields`. It will also include all composite
    fields from parent classes.
    """

    def __new__(mcs, name, bases, attrs):
        # Collect composite fields from current class.
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, CompositeField):
                current_fields.append((key, value))
                attrs.pop(key)
        current_fields.sort(key=lambda x: x[1].creation_counter)
        attrs["declared_composite_fields"] = OrderedDict(current_fields)

        new_class = super().__new__(mcs, name, bases, attrs)

        # Walk through the MRO.
        declared_fields = OrderedDict()
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, "declared_composite_fields"):
                declared_fields.update(base.declared_composite_fields)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        # field overriding
        for field_name in declared_fields:
            if field_name in new_class.base_fields:
                del new_class.base_fields[field_name]

        new_class.base_composite_fields = declared_fields
        new_class.declared_composite_fields = declared_fields

        return new_class


class FormMetaclass(DeclarativeCompositeFieldsMetaclass):
    """
    Metaclass for :class:`~material.forms.Form`.
    """


class ModelFormMetaclass(DeclarativeCompositeFieldsMetaclass, BaseModelFormMetaclass):
    """
    Metaclass for :class:`~material.forms.ModelForm`.
    """


class FormMixin(object):
    """
    The base class for all material forms. It does not inherit from any other
    classes, so you are free to mix it into any custom form class you have. You
    need to use it together with ``FormMetaclass``, like this::

        from material.forms import FormMixin
        from material.forms import FormMetaclass
        import six
        class MyForm(six.with_metaclass(
                FormMetaclass,
                FormMixin,
                MyCustomForm)):
            pass
    The goal of a material form is to behave just like a normal django form but is
    able to take composite fields, like
    :class:`~material.form.fields.FormField` and
    :class:`~material.form.fields.FormSetField`.
    Cleaning, validation, etc. should work totally transparent. See the
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_composite_fields()

    def __iter__(self):
        for name in self.fields:
            yield self[name]
        for name in self.composite_fields:
            yield self[name]

    def __getitem__(self, name):
        """
        Returns a ``django.forms.BoundField`` for the given field name. It also
        returns :class:`~material.forms.boundfield.CompositeBoundField`
        instances for composite fields.
        """
        if name not in self.fields and name in self.composite_fields:
            field = self.composite_fields[name]
            return field.get_bound_field(self, name)
        return super().__getitem__(name)

    def add_composite_field(self, name, field):
        """
        Add a dynamic composite field to the already existing ones and
        initialize it appropriately.
        """
        self.composite_fields[name] = field
        self._init_composite_field(name, field)

    def get_composite_field_value(self, name):
        """
        Return the form/formset instance for the given field name.
        """
        field = self.composite_fields[name]
        if hasattr(field, "get_form"):
            return self.forms[name]
        if hasattr(field, "get_formset"):
            return self.formsets[name]

    def _init_composite_field(self, name, field):
        if hasattr(field, "get_form"):
            form = field.get_form(self, name)
            self.forms[name] = form
        if hasattr(field, "get_formset"):
            formset = field.get_formset(self, name)
            self.formsets[name] = formset

    def _init_composite_fields(self):
        """
        Setup the forms and formsets.
        """
        # The base_composite_fields class attribute is the *class-wide*
        # definition of fields. Because a particular *instance* of the class
        # might want to alter self.composite_fields, we create
        # self.composite_fields here by copying base_composite_fields.
        # Instances should always modify self.composite_fields; they should not
        # modify base_composite_fields.
        self.composite_fields = copy.deepcopy(self.base_composite_fields)
        self.forms = OrderedDict()
        self.formsets = OrderedDict()
        for name, field in self.composite_fields.items():
            self._init_composite_field(name, field)

    def full_clean(self):
        """
        Clean the form, including all formsets and add formset errors to the
        errors dict. Errors of nested forms and formsets are only included if
        they actually contain errors.
        """
        super().full_clean()
        for field_name, composite in self.forms.items():
            composite.full_clean()
            if not composite.is_valid() and composite._errors:
                self._errors[field_name] = ErrorDict(composite._errors)
        for field_name, composite in self.formsets.items():
            composite.full_clean()
            if not composite.is_valid() and composite._errors:
                self._errors[field_name] = ErrorList(composite._errors)

    @property
    def media(self):
        """
        Incorporate composite field's media.
        """
        media_list = []
        media_list.append(super().media)
        for composite_name in self.composite_fields.keys():
            form = self.get_composite_field_value(composite_name)
            media_list.append(form.media)
        return reduce(lambda a, b: a + b, media_list)

    def is_multipart(self):
        if super().is_multipart():
            return True

        if any(
            field.widget.needs_multipart_form
            for field in self.composite_fields.values()
        ):
            return True

        return any(formset.is_multipart() for formset in self.formsets.values())


class ModelFormMixin(FormMixin):
    """
    Can be used in with your custom form subclasses like this::

        from material.forms import ModelFormMixin
        from material.forms import ModelFormMetaclass
        import six
        class MyForm(six.with_metaclass(
                ModelFormMetaclass,
                ModelFormMixin,
                MyCustomModelForm)):
            pass
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # iterate over fields like Django's apply_limit_choices_to_to_formfield
        # to apply DependentModelSelect query
        for field in self.fields.values():
            if hasattr(field.widget, "depends_on") and hasattr(
                field.widget, "queryset"
            ):
                field_queryset = field.queryset
                field.queryset = field_queryset.none()

                parent = None
                parent_field = self.fields[field.widget.depends_on]  ## ttodo

                parent_field_name = field.widget.depends_on
                if self.prefix:
                    parent_field_name = f"{self.prefix}-{field.widget.depends_on}"
                if field.widget.depends_on in parent_field_name:
                    try:
                        parent_value = parent_field.widget.value_from_datadict(
                            self.data, self.files, parent_field_name
                        )
                        parent = parent_field.to_python(parent_value)
                    except (ValueError, TypeError):
                        pass  # invalid input from the client
                elif self.instance.pk:
                    # TODO allow usual choices fields here
                    parent = getattr(self.instance, field.widget.depends_on, None)

                if parent:
                    field.queryset = field.widget.queryset(parent.pk).filter(
                        pk__in=field_queryset.values("pk")
                    )

    def save(self, commit=True):
        """
        When saving a super model form, the nested forms and formsets will be
        saved as well.
        The implementation of ``.save()`` looks like this::

            saved_obj = self.save_form()
            self.save_forms()
            self.save_formsets()
            return saved_obj

        That makes it easy to override it in order to change the order in which
        things are saved.
        The ``.save()`` method will return only a single model instance even if
        nested forms are saved as well. That keeps the API similar to what
        Django's model forms are offering.
        If ``commit=False`` django's modelform implementation will attach a
        ``save_m2m`` method to the form instance, so that you can call it
        manually later. When you call ``save_m2m``, the ``save_forms`` and
        ``save_formsets`` methods will be executed as well so again all nested
        forms are taken care of transparently.
        """
        saved_obj = self.save_form(commit=False)
        self.save_forms(commit=commit)
        if commit:
            saved_obj.save()
            self._save_m2m()
        self.save_formsets(commit=commit)
        return saved_obj

    def _extend_save_m2m(self, name, composites):
        additional_save_m2m = []
        for composite in composites:
            if hasattr(composite, "save_m2m"):
                additional_save_m2m.append(composite.save_m2m)

        if not additional_save_m2m:
            return

        def additional_saves():
            for save_m2m in additional_save_m2m:
                save_m2m()

        # The save() method was called before save_forms()/save_formsets(), so
        # we will already have save_m2m() available.
        if hasattr(self, "save_m2m"):
            _original_save_m2m = self.save_m2m
        else:

            def _original_save_m2m():
                return None

        def augmented_save_m2m():
            _original_save_m2m()
            additional_saves()

        self.save_m2m = augmented_save_m2m
        setattr(self, name, additional_saves)

    def save_form(self, commit=True):
        """
        This calls Django's ``ModelForm.save()``. It only takes care of
        saving this actual form, and leaves the nested forms and formsets
        alone.
        We separate this out of the
        :meth:`~material.forms.ModelForm.save` method to make
        extensibility easier.
        """
        return super().save(commit=commit)

    def save_forms(self, commit=True):
        saved_composites = []
        for name, composite in self.forms.items():
            field = self.composite_fields[name]
            if hasattr(field, "save"):
                field.save(self, name, composite, commit=commit)
                saved_composites.append(composite)

        self._extend_save_m2m("save_forms_m2m", saved_composites)

    def save_formsets(self, commit=True):
        """
        Save all formsets. If ``commit=False``, it will modify the form's
        ``save_m2m()`` so that it also calls the formsets' ``save_m2m()``
        methods.
        """
        saved_composites = []
        for name, composite in self.formsets.items():
            field = self.composite_fields[name]
            if hasattr(field, "save"):
                field.save(self, name, composite, commit=commit)
                saved_composites.append(composite)

        self._extend_save_m2m("save_formsets_m2m", saved_composites)


class ModelForm(ModelFormMixin, forms.ModelForm, metaclass=ModelFormMetaclass):
    """
    The ``ModelForm`` works like a Django ``ModelForm`` but has the
    capabilities of nesting like :class:`~material.forms.Form`.
    Saving a ``ModelForm`` will also save all nested model forms as well.
    """


class Form(FormMixin, forms.Form, metaclass=FormMetaclass):
    """
    The base class for all material forms. The goal of a material form is to behave
    just like a normal django form but is able to take composite fields, like
    :class:`~material.forms.fields.FormField` and
    :class:`~material.forms.fields.FormSetField`.
    Cleaning, validation, etc. should work totally transparent.
    """
