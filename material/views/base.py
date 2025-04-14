# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial licence defined in file 'COMM_LICENSE',
# which is part of this source code package.

from typing import Any

from django import forms

from material.forms.layout import LayoutElement
from material.utils import viewprop


def _collect_elements(parent: Any, container: list[str] | None = None) -> list[str]:
    """
    Recursively collect all field names from a layout structure.

    Args:
        parent: A layout element or container to extract field names from
        container: Optional list to accumulate field names, created if not provided

    Returns:
        List of field names collected from the layout structure
    """
    if container is None:
        container = []

    if hasattr(parent, "fields"):
        for element in parent.fields:
            if isinstance(element, LayoutElement):
                _collect_elements(element, container=container)
            elif isinstance(element, str):
                container.append(element)

    return container


class FormLayoutMixin:
    """
    Mixin for FormView to infer View.fields definition from form Layout.

    Automatically determines the fields to display based on the layout
    defined on the form class.
    """

    form_class: Any = None

    @viewprop
    def layout(self) -> Any | None:
        """
        Get the layout from the form class.

        Returns:
            The layout object if defined on the form class, otherwise None
        """
        if self.form_class is not None and hasattr(self.form_class, "layout"):
            return self.form_class.layout
        return None

    @viewprop
    def fields(self) -> list[str] | str:
        """
        Get the list of fields to be displayed.

        Returns:
            List of field names if layout is defined, otherwise "__all__"
        """
        if self.form_class is not None and self.layout is not None:
            return _collect_elements(self.layout)
        return "__all__"


class Action:
    """
    Represents a UI action with a name, URL, and optional icon.

    Used for creating navigation elements or action buttons in views.
    """

    def __init__(
        self, name: str, url: str | None = None,
        viewname: str | None = None, icon: str | None = None
    ) -> None:
        """
        Initialize an action with name and destination.

        Args:
            name: Display name for the action
            url: Direct URL for the action (either url or viewname must be provided)
            viewname: Django view name for URL resolution
            icon: Optional icon identifier
        """
        assert url or viewname, "Either url or viewname must be provided"
        self.name = name
        self.url = url
        self.viewname = viewname
        self.icon = icon


class BulkActionForm(forms.Form):
    """
    Form for handling bulk actions on model instances.

    Provides fields for selecting multiple objects by primary key
    and a select_all option for operations on all objects.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the form with model-specific fields.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments, must include 'model'
        """
        model = kwargs.pop("model")
        super().__init__(*args, **kwargs)

        self.fields["pk"] = forms.ModelMultipleChoiceField(
            queryset=model._default_manager.all(),
            widget=forms.MultipleHiddenInput,
            required=False,
        )

        self.fields["select_all"] = forms.CharField(
            widget=forms.HiddenInput, required=False
        )
