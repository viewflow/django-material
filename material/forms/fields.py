# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.
from typing import Type

from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import inlineformset_factory

from .boundfield import CompositeBoundField
from .widgets import FormWidget, FormSetWidget


class BaseCompositeField(object):
    """
    The ``BaseCompositeField`` takes care of keeping some kind of compatibility
    with the ``django.forms.Field`` class.
    """

    widget: Type[FormWidget]
    show_hidden_initial = False

    # Tracks each time a FormSetField instance is created. Used to retain
    # order.
    creation_counter = 0

    def __init__(
        self,
        required=True,
        widget=None,
        label=None,
        help_text="",
        localize=False,
        disabled=False,
        initial=None,
    ):
        self.required = required
        self.label = label
        self.help_text = help_text
        self.disabled = disabled
        self.initial = None

        widget = widget or self.widget
        if isinstance(widget, type):
            widget = widget()

        # Trigger the localization machinery if needed.
        self.localize = localize
        if self.localize:
            widget.is_localized = True

        # Let the widget know whether it should display as required.
        widget.is_required = self.required

        # We do not call self.widget_attrs() here as the original field is
        # doing it.

        self.widget = widget

        # Increase the creation counter, and save our local copy.
        self.creation_counter = BaseCompositeField.creation_counter
        BaseCompositeField.creation_counter += 1


class CompositeField(BaseCompositeField):
    """
    Implements the base structure that is relevant for all composite fields.
    This field cannot be used directly, use a subclass of it.
    """

    prefix_name = "composite"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Let the widget know about the field for easier complex renderings in
        # the template.
        self.widget.field = self

    def get_bound_field(self, form, field_name):
        return CompositeBoundField(form, self, field_name)

    def get_prefix(self, form, name):
        """
        Return the prefix that is used for the formset.
        """
        return "{form_prefix}{prefix_name}-{field_name}".format(
            form_prefix=form.prefix + "-" if form.prefix else "",
            prefix_name=self.prefix_name,
            field_name=name,
        )

    def get_initial(self, form, name):
        """
        Get the initial data that got passed into the material form for this
        composite field. It should return ``None`` if no initial values where
        given.
        """

        if hasattr(form, "initial"):
            return form.initial.get(name, None)
        return None

    def get_kwargs(self, form, name):
        """
        Return the keyword arguments that are used to instantiate the formset.
        """
        kwargs = {
            "prefix": self.get_prefix(form, name),
            "initial": self.get_initial(form, name),
        }
        kwargs.update(self.default_kwargs)
        return kwargs


class FormField(CompositeField):
    """
    A field that can be used to nest a form inside another form::

        from django import forms
        from material.forms import Form

        class AddressForm(forms.Form):
            street = forms.CharField()
            city = forms.CharField()

        class RegistrationForm(Form):
            first_name = forms.CharField()
            last_name = forms.CharField()
            address = FormField(AddressForm)

    The fields will all have a prefix in their name so that the naming does not
    clash with other fields on the page. The name attribute of the input tag
    for the ``street`` field in this example will be: ``form-address-street``.
    The name will change if you set a prefix on the material form::

        form = RegistrationForm(prefix='registration')

    Then the field name will be ``registration-form-address-street``.
    You can pass the ``kwargs`` argument to the ``__init__`` method in order to
    give keyword arguments that you want to pass through to the form when it is
    instaniated. So you could use this to pass in initial values::

        class RegistrationForm(Form):
            address = FormField(AddressForm, kwargs={
                'initial': {'street': 'Stairway to Heaven 1'}
            })

    But you can also use nested initial values which you pass into the
    material form::

        RegistrationForm(initial={
            'address': {'street': 'Highway to Hell 666'}
        })

    The first method (using ``kwargs``) will take precedence.
    """

    prefix_name = "form"
    widget = FormWidget

    def __init__(self, form_class, kwargs=None, **field_kwargs):
        super().__init__(**field_kwargs)

        self.form_class = form_class
        if kwargs is None:
            kwargs = {}
        self.default_kwargs = kwargs

    def get_form_class(self, form, name):
        """
        Return the form class that will be used for instantiation in
        ``get_form``. You can override this method in subclasses to change
        the behavior of the given form class.
        """
        return self.form_class

    def get_form(self, form, name):
        """
        Get an instance of the form.
        """
        kwargs = self.get_kwargs(form, name)
        form_class = self.get_form_class(form, name)
        composite_form = form_class(
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            **kwargs
        )
        return composite_form


class ModelFormField(FormField):
    """
    This class is the to :class:`~material.forms.fields.FormField` what
    Django's :class:`ModelForm` is to :class:`Form`. It has the same behavior
    as :class:`~material.forms.fields.FormField` but will also save the
    nested form if the material form is saved. Here is an example::

        from material.forms import ModelFormField

        class EmailForm(forms.ModelForm):
            class Meta:
                model = EmailAddress
                fields = ('email',)
        class UserForm(ModelForm):
            email = ModelFormField(EmailForm)
            class Meta:
                model = User
                fields = ('username',)
        user_form = UserForm(
            {'username': 'john', 'form-email-email': 'john@example.com'})
        if user_form.is_valid():
            user_form.save()

    This will save the ``user_form`` and create a new instance of ``User``
    model and it will also save the ``EmailForm`` and therefore create an
    instance of ``EmailAddress``!
    However you usually want to use one of the exiting subclasses, like

    :class:`~material.forms.fields.ForeignKeyFormField` or extend from
    ``ModelFormField`` class and override the
    :meth:`~material.forms.fields.ModelFormField.get_instance` method.
    .. note::
        Usually the :class:`~material.forms.fields.ModelFormField` is used
        inside a :class:`~material.forms.ModelForm`. You actually
        can use it within a :class:`~material.forms.Form`, but
        since this form type does not have a ``save()`` method, you will need
        to take care of saving the nested model form yourself.
    """

    def get_initial(self, form, name):
        """
        TODO: Fix, return form dictionary
        """
        return None

    def get_instance(self, form, name):
        """
        Provide an instance that shall be used when instantiating the
        modelform. The ``form`` argument is the material form instance that this
        ``ModelFormField`` is used in. ``name`` is the name of this field on
        the material form.
        This returns ``None`` by default. So you usually want to override this
        method in a subclass.
        """
        return None

    def get_kwargs(self, form, name):
        """
        Return the keyword arguments that are used to instantiate the formset.
        The ``instance`` kwarg will be set to the value returned by
        :meth:`~material.forms.ModelFormField.get_instance`. The
        ``empty_permitted`` kwarg will be set to the inverse of the
        ``required`` argument passed into the constructor of this field.
        """
        kwargs = super().get_kwargs(form, name)
        instance = self.get_instance(form, name)
        kwargs.setdefault("instance", instance)
        kwargs.setdefault("empty_permitted", not self.required)
        return kwargs

    def shall_save(self, form, name, composite_form):
        """
        Return ``True`` if the given ``composite_form`` (the nested form of
        this field) shall be saved. Return ``False`` if the form shall not be
        saved together with the material form.
        By default it will return ``False`` if the form was not changed and the
        ``empty_permitted`` argument for the form was set to ``True``. That way
        you can allow empty forms.
        """
        if composite_form.empty_permitted and not composite_form.has_changed():
            return False
        return True

    def save(self, form, name, composite_form, commit):
        """
        This method is called by
        :meth:`material.forms.ModelForm.save` in order to save the
        modelform that this field takes care of and calls on the nested form's
        ``save()`` method. But only if
        :meth:`~material.forms.ModelFormField.shall_save` returns
        ``True``.
        """
        if self.shall_save(form, name, composite_form):
            return composite_form.save(commit=commit)
        return None


class ForeignKeyFormField(ModelFormField):
    def __init__(
        self, form_class, kwargs=None, field_name=None, blank=None, **field_kwargs
    ):
        super().__init__(form_class, kwargs, **field_kwargs)
        self.field_name = field_name
        self.blank = blank

    def get_kwargs(self, form, name):
        kwargs = super().get_kwargs(form, name)
        if "instance" not in kwargs:
            kwargs.setdefault("instance", self.get_instance(form, name))
        if "empty_permitted" not in kwargs:
            if self.allow_blank(form, name):
                kwargs["empty_permitted"] = True
        return kwargs

    def get_field_name(self, form, name):
        return self.field_name or name

    def allow_blank(self, form, name):
        """
        Allow blank determines if the form might be completely empty. If it's
        empty it will result in a None as the saved value for the ForeignKey.
        """
        if self.blank is not None:
            return self.blank
        model = form._meta.model
        field = model._meta.get_field(self.get_field_name(form, name))
        return field.blank

    def get_form_class(self, form, name):
        form_class = self.form_class
        return form_class

    def get_instance(self, form, name):
        try:
            field_name = self.get_field_name(form, name)
            return getattr(form.instance, field_name)
        except ObjectDoesNotExist:
            return None

    def save(self, form, name, composite_form, commit):
        # Support the ``empty_permitted`` attribute. This is set if the field
        # is ``blank=True`` .
        if composite_form.empty_permitted and not composite_form.has_changed():
            saved_obj = composite_form.instance
        else:
            saved_obj = super().save(form, name, composite_form, commit)
        setattr(form.instance, self.get_field_name(form, name), saved_obj)
        if commit:
            form.instance.save()
        else:
            raise NotImplementedError(
                "ForeignKeyFormField cannot yet be used with non-commiting "
                "form saves."
            )
        return saved_obj


class FormSetField(CompositeField):
    """
    First argument is a formset class that is instantiated by this
    FormSetField.
    You can pass the ``kwargs`` argument to specify kwargs values that
    are used when the ``formset_class`` is instantiated.
    """

    prefix_name = "formset"
    widget = FormSetWidget

    def __init__(self, formset_class, kwargs=None, **field_kwargs):
        super().__init__(**field_kwargs)

        self.formset_class = formset_class
        if kwargs is None:
            kwargs = {}
        self.default_kwargs = kwargs

    def get_formset_class(self, form, name):
        """
        Return the formset class that will be used for instantiation in
        ``get_formset``. You can override this method in subclasses to change
        the behavior of the given formset class.
        """
        return self.formset_class

    def get_formset(self, form, name):
        """
        Get an instance of the formset.
        """
        kwargs = self.get_kwargs(form, name)
        formset_class = self.get_formset_class(form, name)
        formset = formset_class(
            form.data if form.is_bound else None,
            form.files if form.is_bound else None,
            **kwargs
        )
        return formset


class ModelFormSetField(FormSetField):
    def shall_save(self, form, name, formset):
        return True

    def save(self, form, name, formset, commit):
        if self.shall_save(form, name, formset):
            return formset.save(commit=commit)
        return None


class InlineFormSetField(ModelFormSetField):
    """
    The ``InlineFormSetField`` helps when you want to use a inline formset.

    You can pass in either the keyword argument ``formset_class`` which is a
    ready to use formset that inherits from ``BaseInlineFormSet`` or was
    created by the ``inlineformset_factory``.
    The other option is to provide the arguments that you would usually pass
    into the ``inlineformset_factory``. The required arguments for that are:

    ``model``
        The model class which should be represented by the forms in the
        formset.

    ``parent_model``
        The parent model is the one that is referenced by the model in a
        foreignkey.

    ``form`` (optional)
        The model form that is used as a baseclass for the forms in the inline
        formset.

    You can use the ``kwargs`` keyword argument to pass extra arguments for the
    formset that are passed through when the formset is instantiated.
    All other not mentioned keyword arguments, like ``extra``, ``max_num`` etc.
    will be passed directly to the ``inlineformset_factory``.
    Example::

        class Gallery(models.Model):
            name = models.CharField(max_length=50)

        class Image(models.Model):
            gallery = models.ForeignKey(Gallery)
            image = models.ImageField(...)

        class GalleryForm(ModelFormWithFormSets):
            images = InlineFormSetField(
                parent_model=Gallery, model=Image, extra=1)

            class Meta:
                model = Gallery
                fields = ('name',)
    """

    def __init__(
        self,
        parent_model=None,
        model=None,
        formset_class=None,
        kwargs=None,
        **factory_kwargs
    ):
        """
        You need to either provide the ``formset_class`` or the ``model``
        argument.
        If the ``formset_class`` argument is not given, the ``model`` argument
        is used to create the formset_class on the fly when needed by using the
        ``inlineformset_factory``.
        """

        # Make sure that all standard arguments will get passed through to the
        # parent's __init__ method.
        field_kwargs = {}
        for arg in ["required", "widget", "label", "help_text", "localize"]:
            if arg in factory_kwargs:
                field_kwargs[arg] = factory_kwargs.pop(arg)

        self.parent_model = parent_model
        self.model = model
        self.formset_factory_kwargs = factory_kwargs
        super().__init__(formset_class, kwargs=kwargs, **field_kwargs)
        if (
            self.formset_class is None
            and "form" not in self.formset_factory_kwargs
            and "fields" not in self.formset_factory_kwargs
            and "exclude" not in self.formset_factory_kwargs
        ):
            raise ValueError(
                "You need to either specify the `formset_class` argument or "
                "one of `form`/`fields`/`exclude` arguments "
                "when creating a {0}.".format(self.__class__.__name__)
            )

    def get_model(self, form, name):  # noqa D102
        return self.model

    def get_parent_model(self, form, name):  # noqa D102
        if self.parent_model is not None:
            return self.parent_model
        return form._meta.model

    def get_formset_class(self, form, name):
        """
        Return a formset class for the field.

        Either return the formset class that was provided as argument to the
        __init__ method, or build one based on the ``parent_model`` and
        ``model`` attributes.
        """
        if self.formset_class is not None:
            return self.formset_class
        formset_class = inlineformset_factory(
            self.get_parent_model(form, name),
            self.get_model(form, name),
            **self.formset_factory_kwargs
        )
        return formset_class

    def get_kwargs(self, form, name):  # noqa D102
        kwargs = super().get_kwargs(form, name)
        kwargs.setdefault("instance", form.instance)
        return kwargs
