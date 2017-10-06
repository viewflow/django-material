from django.forms import widgets

from .base import get_field_renderer
from .form import FormRenderer
from .checkbox import CheckboxInputRenderer
from .input import InputRenderer
from .select import SelectRenderer

__all__ = (
    'get_field_renderer', 'FormRenderer',
    'WIDGET_RENDERES', 'FIELD_RENDERERS'
)

WIDGET_RENDERES = {
    widgets.CheckboxInput: CheckboxInputRenderer,
    widgets.TextInput: InputRenderer,
    widgets.EmailInput: InputRenderer,
    widgets.PasswordInput: InputRenderer,
    widgets.Select: SelectRenderer,
}


FIELD_RENDERERS = {

}
