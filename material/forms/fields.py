# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    Union,
    cast,
    Callable,
    ClassVar,
    Iterable,
    Mapping,
    Set,
    Tuple,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from .forms import Form, ModelForm
    from django.forms.fields import Field

from django.core.exceptions import ObjectDoesNotExist
from django.forms import BaseForm
from django.forms.models import BaseModelForm, inlineformset_factory, BaseInlineFormSet
from django.forms.formsets import BaseFormSet
from django.db import models

from .boundfield import CompositeBoundField
from .widgets import FormWidget, FormSetWidget


class BaseCompositeField(object):
    """
    The ``BaseCompositeField`` takes care of keeping some kind of compatibility
    with the ``django.forms.Field`` class.
    """

    widget_class: ClassVar[Any] = FormWidget
    show_hidden_initial: bool = False

    # Tracks each time a FormSetField instance is created. Used to retain
    # order.
    creation_counter: ClassVar[int] = 0

    def __init__(
        self,
        required: bool = True,
        widget: Optional[Union[Type[FormWidget], FormWidget]] = None,
        label: Optional[str] = None,
        help_text: str = "",
        localize: bool = False,
        disabled: bool = False,
        initial: Optional[Any] = None,
    ) -> None:
        self.required: bool = required
        self.label: Optional[str] = label
        self.help_text: str = help_text
        self.disabled: bool = disabled
        self.initial: Optional[Any] = None

        widget_to_use = widget or self.widget_class
        if isinstance(widget_to_use, type):
            widget_to_use = widget_to_use()

        # Trigger the localization machinery if needed.
        self.localize: bool = localize
        if self.localize:
            widget_to_use.is_localized = True

        # Let the widget know whether it should display as required.
        widget_to_use.is_required = self.required

        # We do not call self.widget_attrs() here as the original field is
        # doing it.

        self.widget = widget_to_use  # type: ignore

        # Increase the creation counter, and save our local copy.
        self._creation_counter: int = BaseCompositeField.creation_counter
        BaseCompositeField.creation_counter += 1  # type: ignore


class CompositeField(BaseCompositeField):
    """
    Implements the base structure that is relevant for all composite fields.
    This field cannot be used directly, use a subclass of it.
    """

    prefix_name: str = "composite"
    default_kwargs: Dict[str, Any] = {}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # Let the widget know about the field for easier complex renderings in
        # the template.
        # Note: FormWidget has a dynamic attribute 'field' that's not in the type annotations
        # Ignore type error since CompositeBoundField is not a django Field but works at runtime
        if hasattr(self.widget, "field"):
            self.widget.field = self  # type: ignore

    def get_bound_field(self, form: "Form", field_name: str) -> CompositeBoundField:
        """Return a CompositeBoundField instance for this field."""
        # Type ignore because CompositeBoundField accepts our field type but pyright expects django Field
        return CompositeBoundField(form, self, field_name)  # type: ignore

    def get_prefix(self, form: "Form", name: str) -> str:
        """
        Return the prefix that is used for the formset.
        """
        return "{form_prefix}{prefix_name}-{field_name}".format(
            form_prefix=form.prefix + "-" if form.prefix else "",
            prefix_name=self.prefix_name,
            field_name=name,
        )

    def get_initial(self, form: "Form", name: str) -> Optional[Any]:
        """
        Get the initial data that got passed into the material form for this
        composite field. It should return ``None`` if no initial values where
        given.
        """
        if hasattr(form, "initial"):
            return form.initial.get(name, None)
        return None

    def get_kwargs(self, form: "Form", name: str) -> Dict[str, Any]:
        """
        Return the keyword arguments that are used to instantiate the formset.
        """
        kwargs: Dict[str, Any] = {
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

    prefix_name: str = "form"
    widget_class = FormWidget

    def __init__(
        self,
        form_class: Type[BaseForm],
        kwargs: Optional[Dict[str, Any]] = None,
        **field_kwargs: Any,
    ) -> None:
        super().__init__(**field_kwargs)

        self.form_class: Type[BaseForm] = form_class
        if kwargs is None:
            kwargs = {}
        self.default_kwargs: Dict[str, Any] = kwargs

    def get_form_class(self, form: "Form", name: str) -> Type[BaseForm]:
        """
        Return the form class that will be used for instantiation in
        ``get_form``. You can override this method in subclasses to change
        the behavior of the given form class.
        """
        return self.form_class

    def get_form(self, form: "Form", name: str) -> BaseForm:
        """
        Get an instance of the form.
        """
        kwargs = self.get_kwargs(form, name)
        form_class = self.get_form_class(form, name)
        composite_form = form_class(
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            **kwargs,
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

    def get_initial(self, form: "Form", name: str) -> Optional[Any]:
        """
        TODO: Fix, return form dictionary
        """
        return None

    def get_instance(self, form: "Form", name: str) -> Optional[models.Model]:
        """
        Provide an instance that shall be used when instantiating the
        modelform. The ``form`` argument is the material form instance that this
        ``ModelFormField`` is used in. ``name`` is the name of this field on
        the material form.
        This returns ``None`` by default. So you usually want to override this
        method in a subclass.
        """
        return None

    def get_kwargs(self, form: "Form", name: str) -> Dict[str, Any]:
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

    def shall_save(self, form: "Form", name: str, composite_form: BaseModelForm) -> bool:
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

    def save(
        self, form: "Form", name: str, composite_form: BaseModelForm, commit: bool
    ) -> Optional[models.Model]:
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
        self,
        form_class: Type[BaseModelForm],
        kwargs: Optional[Dict[str, Any]] = None,
        field_name: Optional[str] = None,
        blank: Optional[bool] = None,
        **field_kwargs: Any,
    ) -> None:
        super().__init__(form_class, kwargs, **field_kwargs)
        self.field_name: Optional[str] = field_name
        self.blank: Optional[bool] = blank

    def get_kwargs(self, form: "Form", name: str) -> Dict[str, Any]:
        kwargs = super().get_kwargs(form, name)
        if "instance" not in kwargs:
            kwargs.setdefault("instance", self.get_instance(form, name))
        if "empty_permitted" not in kwargs:
            if self.allow_blank(form, name):
                kwargs["empty_permitted"] = True
        return kwargs

    def get_field_name(self, form: "Form", name: str) -> str:
        return self.field_name or name

    def allow_blank(self, form: "Form", name: str) -> bool:
        """
        Allow blank determines if the form might be completely empty. If it's
        empty it will result in a None as the saved value for the ForeignKey.
        """
        if self.blank is not None:
            return self.blank
        # This is safe for ModelForm but not for Form, so we type-ignore it
        # The FormMixin from our forms module ensures ModelForm has _meta.model
        model = form._meta.model  # type: ignore
        field = model._meta.get_field(self.get_field_name(form, name))
        return field.blank

    def get_form_class(self, form: "Form", name: str) -> Type[BaseForm]:
        return self.form_class

    def get_instance(self, form: "Form", name: str) -> Optional[models.Model]:
        try:
            field_name = self.get_field_name(form, name)
            # This is safe for ModelForm but not for Form, so we type-ignore it
            return getattr(form.instance, field_name)  # type: ignore
        except ObjectDoesNotExist:
            return None

    def save(
        self, form: "Form", name: str, composite_form: BaseModelForm, commit: bool
    ) -> Optional[models.Model]:
        # Support the ``empty_permitted`` attribute. This is set if the field
        # is ``blank=True`` .
        if composite_form.empty_permitted and not composite_form.has_changed():
            saved_obj = composite_form.instance
        else:
            saved_obj = super().save(form, name, composite_form, commit)
        # This is safe for ModelForm but not for Form, so we type-ignore it
        setattr(form.instance, self.get_field_name(form, name), saved_obj)  # type: ignore
        if commit:
            # This is safe for ModelForm but not for Form, so we type-ignore it
            form.instance.save()  # type: ignore
        else:
            raise NotImplementedError(
                "ForeignKeyFormField cannot yet be used with non-commiting form saves."
            )
        return saved_obj


class FormSetField(CompositeField):
    """
    First argument is a formset class that is instantiated by this
    FormSetField.
    You can pass the ``kwargs`` argument to specify kwargs values that
    are used when the ``formset_class`` is instantiated.
    """

    prefix_name: str = "formset"
    widget_class = FormSetWidget

    def __init__(
        self,
        formset_class: Type[BaseFormSet],
        kwargs: Optional[Dict[str, Any]] = None,
        **field_kwargs: Any,
    ) -> None:
        super().__init__(**field_kwargs)

        self.formset_class = formset_class
        if kwargs is None:
            kwargs = {}
        self.default_kwargs: Dict[str, Any] = kwargs

    def get_formset_class(self, form: "Form", name: str) -> Type[BaseFormSet]:
        """
        Return the formset class that will be used for instantiation in
        ``get_formset``. You can override this method in subclasses to change
        the behavior of the given formset class.
        """
        return self.formset_class

    def get_formset(self, form: "Form", name: str) -> BaseFormSet:
        """
        Get an instance of the formset.
        """
        kwargs = self.get_kwargs(form, name)
        formset_class = self.get_formset_class(form, name)
        formset = formset_class(
            form.data if form.is_bound else None, form.files if form.is_bound else None, **kwargs
        )
        return formset


class ModelFormSetField(FormSetField):
    def shall_save(self, form: "Form", name: str, formset: BaseFormSet) -> bool:
        return True

    def save(
        self, form: "Form", name: str, formset: BaseFormSet, commit: bool
    ) -> Optional[List[models.Model]]:
        if self.shall_save(form, name, formset):
            # BaseFormSet doesn't have save() method by default,
            # but ModelFormSet classes will have it at runtime
            return formset.save(commit=commit)  # type: ignore
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
        parent_model: Optional[Type[models.Model]] = None,
        model: Optional[Type[models.Model]] = None,
        formset_class: Any = None,  # Using Any to avoid type error with None
        kwargs: Optional[Dict[str, Any]] = None,
        **factory_kwargs: Any,
    ) -> None:
        """
        You need to either provide the ``formset_class`` or the ``model``
        argument.
        If the ``formset_class`` argument is not given, the ``model`` argument
        is used to create the formset_class on the fly when needed by using the
        ``inlineformset_factory``.
        """

        # Make sure that all standard arguments will get passed through to the
        # parent's __init__ method.
        field_kwargs: Dict[str, Any] = {}
        for arg in ["required", "widget", "label", "help_text", "localize"]:
            if arg in factory_kwargs:
                field_kwargs[arg] = factory_kwargs.pop(arg)

        self.parent_model: Optional[Type[models.Model]] = parent_model
        self.model: Optional[Type[models.Model]] = model
        self.formset_factory_kwargs: Dict[str, Any] = factory_kwargs
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

    def get_model(self, form: "Form", name: str) -> Type[models.Model]:  # noqa D102
        if self.model is None:
            raise ValueError("Model is not specified")
        return self.model

    def get_parent_model(self, form: "Form", name: str) -> Type[models.Model]:  # noqa D102
        if self.parent_model is not None:
            return self.parent_model
        # This is safe for ModelForm but not for Form, so we type-ignore it
        return form._meta.model  # type: ignore

    def get_formset_class(self, form: "Form", name: str) -> Type[BaseFormSet]:
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
            **self.formset_factory_kwargs,
        )
        return formset_class

    def get_kwargs(self, form: "Form", name: str) -> Dict[str, Any]:  # noqa D102
        kwargs = super().get_kwargs(form, name)
        # This is safe for ModelForm but not for Form, so we type-ignore it
        kwargs.setdefault("instance", form.instance)  # type: ignore
        return kwargs
