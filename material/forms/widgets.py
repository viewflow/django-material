# Copyright (c) 2017-2023, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

from django import forms
from django.forms import widgets


class InlineCalendar(widgets.DateInput):
    """
    InlineCalendar: A full-sized month calendar widget for Django forms.

    See the demo at: https://demo.viewflow.io/widget/inlinecalendar/

    Attributes:
        format (str): Date format for the widget. Default is "%d.%m.%Y".

    Usage:

    .. code-block:: python

        from viewflow.forms import InlineCalendar

        class InlineCalendarForm(forms.Form):
            start_date = forms.DateField(
                help_text="custom input format",
                initial=date(1969, 7, 21),
                input_formats=["%d.%m.%Y"],
                widget=InlineCalendar(format="%d.%m.%Y"),
            )

    """


class FormWidget(forms.Widget):
    template_name = "viewflow/formfield.html"
    value_context_name = "form"

    def format_value(self, value):
        return value


class FormSetWidget(forms.Widget):
    template_name = "viewflow/formsetfield.html"
    value_context_name = "formset"

    def format_value(self, value):
        return value


class AjaxModelSelect(forms.TextInput):
    """
    A widget for ModelChoiceField providing AJAX-based autocomplete functionality.

    Parameters:
        lookups (list): Fields on the associated model to be queried for suggestions.
            For example, `lookups=['name__istartswith']` will provide suggestions where
            the `name` starts with the entered query.

    See the demo at: https://demo.viewflow.io/atlas/city/add/

    Demo source code `CRUD101::Atlas <https://github.com/viewflow/cookbook/blob/main/crud101/atlas/viewset.py>`_

    Usage:
        To integrate `AjaxModelSelect` in a Django form:

        .. code-block:: python

            from viewflow.forms import InlineCalendar

            class AddressForm(ModelForm):
                class Meta:
                    model = models.Address
                    fields = '__all__'
                    widgets = {
                        'country': AjaxModelSelect(lookups=['name__istartswith'])
                    }

    AJAX Integration:
        To fetch suggestions, an OPTIONS request is made to the form's URL with an additional
        `X-Request-Autocomplete` HTTP header.

        .. code-block:: python

            if request.method == "OPTIONS" and "HTTP_X_REQUEST_AUTOCOMPLETE" in request.META:
                query = request.META.get("HTTP_X_REQUEST_AUTOCOMPLETE")
                options = QueryDict(query, encoding=self.request.encoding)
                field_name = options.get("field", "")
                query = options.get("query")
                ...

        The server should return a JSON response structured as:

        .. code-block:: json

            {
                "suggestions": [
                    { "value": "Chicago Blackhawks", "data": { "id": 1 } },
                    { "value": "Chicago Bulls", "data": { "id": 2 } }
                ]
            }

    Utility Mixin:
        To simplify the integration, use the built-in `FormAjaxCompleteMixin`:

        .. code-block:: python

            from viewflow.forms import FormAjaxCompleteMixin

            class UpdateAddressView(FormAjaxCompleteMixin, generic.UpdateView):
                form_class = AddressForm

    """

    def __init__(self, *args, **kwargs):
        self.lookups = kwargs.pop("lookups", None)
        if not self.lookups:
            raise ValueError("AjaxModelSelect need `lookups` to be provided")
        super().__init__(*args, **kwargs)


class AjaxMultipleModelSelect(forms.TextInput):
    """
    A widget designed for `ModelMultipleChoiceField` that introduces AJAX-based autocomplete
    functionality for multiple selections.

    This widget is suitable for forms where users might need to select multiple entries
    from a model, with the convenience of autocomplete suggestions as they type.

    The behavior of this widget is similar to `AjaxModelSelect`, but is tailored
    for handling multiple model choices.

    Usage:
        To integrate `AjaxModelSelect` in a Django form:

        .. code-block:: python

            class CountryForm(forms.Form):
                cities = forms.ModelMultipleChoiceField(
                    queryset=City.objects.all(),
                    widget=widgets.AjaxMultipleModelSelect(lookups=["name__istartswith"]),
                    help_text="default",
                )

    Demo source code `CRUD101::Atlas <https://github.com/viewflow/cookbook/blob/main/crud101/atlas/viewset.py>`_

    See Also:
        For a similar widget focused on singular model choice, refer to:
        :class:`viewflow.form.widgets.AjaxModelSelect`.
    """

    def __init__(self, *args, **kwargs):
        self.lookups = kwargs.pop("lookups", None)
        if not self.lookups:
            raise ValueError("AjaxMultiModelSelect need `lookups` to be provided")
        super().__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)


class TrixEditorWidget(forms.TextInput):
    """
    WYSIWYG editor widget based on the Trix editor.

    See a demo: https://demo.viewflow.io/review/review/add/

    Usage:
        .. code-block:: python

            from viewflow.forms import TrixEditorWidget
            from viewflow.views import CreateModelView

            class AddReviewView(CreateModelView):
                fields = ["title", "text"]
                form_widgets = {"text": TrixEditorWidget}

    .. seealso::
        https://trix-editor.org/
    """

    def __init__(self, options=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Media:
        js = [
            "viewflow/js/trix.js",
        ]
        css = {"all": ("viewflow/css/trix.css",)}


class DependentModelSelect(forms.Select):
    """
    A chained select widget where choice options depend on the value selected in
    another field.

    Parameters:
        - depends_on (str): The name of the field this widget depends on.
        - queryset (callable): A lambda or function returning a queryset based
          on the parent selection.

    Usage:
        For a model named `Sea` with a field `parent` see that depends on the
        `ocean` field:

        .. code-block:: python

            class SeaViewset(DeleteViewMixin, ModelViewset):
                model = models.Sea

                form_widgets = {
                    'parent': DependentModelSelect(
                        depends_on='ocean', queryset=lambda parent:
                        models.Sea.objects.filter(ocean=parent)
                    )
                }

    Demo source code `CRUD101::Atlas <https://github.com/viewflow/cookbook/blob/main/crud101/atlas/viewset.py>`_

    AJAX Integration:
        Choices are fetched via an OPTIONS request to the form's URL with the
        additional `X-Request-Select-Options` HTTP header.

        .. code-block:: python

            if request.method == "OPTIONS" and "HTTP_X_REQUEST_SELECT_OPTIONS" in request.META:
                query = request.META.get("HTTP_X_REQUEST_SELECT_OPTIONS")
                options = QueryDict(query, encoding=self.request.encoding)
                field_name = options.get("field", "")
                query = options.get("query")
                ...

        The server should return a JSON response structured as:

        .. code-block:: json

            {
                "data":  [
                    {'name': "", "options": {"key1": "value1", "key2": "value2", ...}}
                    {'name': "Option group", "options": {"key3": "value3", "key4": "value4", ...}}
                ]
            }

    Utility Mixin:
        To simplify the integration, use the built-in `FormDependentSelectMixin`

        .. code-block:: python

            from viewflow.forms import FormDependentSelectMixin

            class SeeView(FormDependentSelectMixin, generic.UpdateView):
                ...
    """

    def __init__(self, *args, **kwargs):
        self.depends_on = kwargs.pop("depends_on", None)
        self.queryset = kwargs.pop("queryset", None)
        # TODO exclude_self option for queryset

        if not self.depends_on or self.queryset is None:
            raise ValueError(
                "DependentModelSelect need both depends_on and queryset been provided"
            )
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        name_prefix = ""
        if context["widget"]["name"].startswith("formset-"):
            form_prefix = context["widget"]["name"].rsplit("-", 1)[0]
            name_prefix = f"{form_prefix}-"
        context["widget"]["attrs"]["parent"] = f"{name_prefix}{self.depends_on}"

        return context


class TotalCounterWidget(forms.TextInput):
    """
    A widget to calculate the total for form fields based on given expressions.

    It supports basic arithmetic expressions, such as:
      - field1*field2+field3*field4

    For formsets, it can aggregate values across forms with syntax:
      - sum(formsetName.field1*formsetName.field2)
    This translates to aggregating operations across each form instance in the formset:
      - formset-form0.field1*formset-form0.field2 + formset-form1.field1*formset-form1.field2 + ...

    Parameters:
        - expression (str): The arithmetic expression used to compute the total.
        - round (int, optional): The number of decimal places to round to, if any.

    See a demo: https://demo.viewflow.io/workflow/flows/shipment/start/

    Demo source code `Workflow101::Shipment <https://github.com/viewflow/cookbook/blob/main/workflow101/shipment/forms.py>`_

    Usage:

        .. code-block:: python

            from viewflow.forms import TotalCounterWidget

            class ShipmentForm(ModelForm):
                items = InlineFormSetField(
                    Shipment,
                    ShipmentItem,
                    fields=["name", "quantity", "cost"],
                    can_delete=False,
                    extra=1,
                )

                total = forms.CharField(
                    widget=TotalCounterWidget(expression="sum(items.quantity*items.cost)"),
                    label="",
                )

                layout = Layout(
                    "items",
                    Row(
                        Tag(
                            "h4",
                            text="Total:",
                            style="text-align:right",
                            class_="mdc-typography",
                        ),
                        "total",
                    ),
                )
    """

    def __init__(self, *args, expression="", round=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["expression"] = expression
        self.attrs["round"] = round


class JSONEditorWiget(forms.TextInput):
    pass
