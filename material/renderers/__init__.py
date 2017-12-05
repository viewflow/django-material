from django.forms import widgets

from material import widgets as material_widgets

from .base import get_field_renderer
from .form import FormRenderer
from .checkbox import CheckboxInputRenderer
from .input import (
    InputRenderer, MaterialInputRenderer, PasswordRenderer,
    MaterialPasswordRenderer
)
from .select import SelectRenderer, MaterialSelectRenderer


__all__ = (
    'get_field_renderer', 'FormRenderer',
    'WIDGET_RENDERERS', 'FIELD_RENDERERS'
)

WIDGET_RENDERERS = {
    widgets.CheckboxInput: CheckboxInputRenderer,

    widgets.TextInput: InputRenderer,
    material_widgets.MaterialTextInput: MaterialInputRenderer,

    widgets.EmailInput: InputRenderer,
    material_widgets.MaterialEmailInput: MaterialInputRenderer,

    widgets.PasswordInput: PasswordRenderer,
    material_widgets.MaterialPasswordInput: MaterialPasswordRenderer,

    widgets.Select: SelectRenderer,
    material_widgets.MaterialSelect: MaterialSelectRenderer
}


FIELD_RENDERERS = {

}
