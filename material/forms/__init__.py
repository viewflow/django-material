"""
Django Material forms module.
"""

from .layout import Caption, Column, FieldSet, Layout, Row, Span
from .renderers import MaterialBoundField, MaterialFormRenderer


class ModelForm:
    """
    Base form class for Material Design 3 forms.

    Implements better rendering for Material Design 3 form fields with
    proper error handling, annotations and styling.
    """

    pass


class FormAjaxCompleteMixin:
    """
    Form mixin to handle ajax field completion.

    Provides functionality for asynchronous field value completion based on
    partial user input.
    """

    pass


class FormDependentSelectMixin:
    """
    Form mixin to handle dependent select fields.

    Allows select fields to update their options based on the value of
    other fields in the form.
    """

    pass


__all__ = [
    "MaterialFormRenderer",
    "MaterialBoundField",
    "Layout",
    "Row",
    "Column",
    "FieldSet",
    "Span",
    "Caption",
    "ModelForm",
    "FormAjaxCompleteMixin",
    "FormDependentSelectMixin",
]
