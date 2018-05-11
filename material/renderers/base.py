from functools import lru_cache
from django.utils.functional import cached_property
from django.utils.html import mark_safe, conditional_escape
from django.test.signals import setting_changed

from material.ptml import Div


class FieldRender(object):
    def __init__(self, bound_field):
        self.bound_field = bound_field

    @property
    def field(self):
        return self.bound_field.field

    @property
    def widget(self):
        return self.field.widget

    @property
    def disabled(self):
        return self.field.disabled

    @property
    def required(self):
        return (
            self.widget.use_required_attribute(self.bound_field.initial) and
            self.field.required and
            self.bound_field.form.use_required_attribute
        )

    @property
    def html_name(self):
        return self.bound_field.html_name

    @property
    def label_text(self):
        return self.bound_field.label

    @cached_property
    def value(self):
        return self.bound_field.value()

    @cached_property
    def formatted_value(self):
        return self.widget.format_value(self.value)

    @cached_property
    def errors(self):
        return self.bound_field.errors

    def format_help_text(self, default=mark_safe('&nbsp;')):
        text = default
        if self.errors:
            text = '<br/>'.join(conditional_escape(error) for error in self.errors)
        elif self.bound_field.help_text:
            text = self.bound_field.help_text
        return text

    def __str__(self):
        return str(self.bound_field)


class FormFieldRender(FieldRender):
    wrapper_class = None

    def wrapper_attrs(self):
        return {
            'class': {
                'dmc-form-field': True,
                'dmc-form-field--invalid': bool(self.errors),
                self.wrapper_class: bool(self.wrapper_class)
            },
            'title': self.bound_field.help_text
        }

    def prefix(self):
        return None

    def suffix(self):
        return None

    def body(self):
        return []

    def element(self):
        return Div(**self.wrapper_attrs()) / [
            self.prefix(),
            Div(class_="dmc-form-field__input") / [
                *self.body()
            ],
            self.suffix()
        ]

    def __str__(self):
        return str(self.element())


@lru_cache(maxsize=None)
def get_field_renderer(field):
    from material.settings import material_settings

    for field_class in type(field).mro()[:-2]:
        if field_class in material_settings.FIELD_RENDERERS:
            return material_settings.FIELD_RENDERERS[field_class]

    for widget_class in type(field.widget).mro()[:-2]:
        if widget_class in material_settings.WIDGET_RENDERERS:
            return material_settings.WIDGET_RENDERERS[widget_class]

    return FieldRender


def _clear_field_renderer_cache(*args, **kwargs):
    if kwargs['setting'] == 'MATERIAL':
        get_field_renderer.cache_clear()


setting_changed.connect(_clear_field_renderer_cache)
