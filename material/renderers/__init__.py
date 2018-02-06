from django.forms import widgets

from material import widgets as material_widgets

from .base import get_field_renderer
from .form import FormRenderer
from .calendar import InlineCalendarRenderer, DateInputRenderer
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

    widgets.DateInput: DateInputRenderer,

    widgets.TextInput: InputRenderer,
    material_widgets.TextInput: MaterialInputRenderer,

    widgets.NumberInput: InputRenderer,
    material_widgets.NumberInput: MaterialInputRenderer,

    widgets.EmailInput: InputRenderer,
    material_widgets.EmailInput: MaterialInputRenderer,

    widgets.PasswordInput: PasswordRenderer,
    material_widgets.PasswordInput: MaterialPasswordRenderer,

    widgets.Select: SelectRenderer,
    material_widgets.Select: MaterialSelectRenderer,

    widgets.URLInput: InputRenderer,
    material_widgets.URLInput: MaterialInputRenderer,

    material_widgets.InlineCalendar: InlineCalendarRenderer,
}


FIELD_RENDERERS = {

}
