"""Django-material - material design for the django framework."""

from .base import (
    Layout, Fieldset, Row, Column, Span, Field,
    Span2, Span3, Span4, Span5, Span6, Span7,
    Span8, Span9, Span10, Span11, Span12,
    LayoutMixin)


__all__ = (
    'Layout', 'Fieldset', 'Row', 'Column', 'Span', 'Field',
    'Span2', 'Span3', 'Span4', 'Span5', 'Span6', 'Span7',
    'Span8', 'Span9', 'Span10', 'Span11', 'Span12',
    'LayoutMixin'
)

import warnings

warnings.warn("The package was merged into django-viewflow. Please consider to switch to django-viewflow>=2.0.0b1")

