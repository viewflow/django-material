from django.forms import widgets

from material import widgets as material_widgets

from .base import get_field_renderer
from .form import FormRenderer
from .checkbox import CheckboxInputRenderer
from .input import InputRenderer, MaterialInputRenderer
from .select import SelectRenderer


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

    widgets.PasswordInput: InputRenderer,
    material_widgets.MaterialPasswordInput: MaterialInputRenderer,

    widgets.Select: SelectRenderer,
}


FIELD_RENDERERS = {

}
