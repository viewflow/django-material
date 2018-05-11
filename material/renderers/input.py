from material.ptml import A, Div, Input, Label, P
from .base import FormFieldRender


class MDCTextInput(object):
    """
    MDC Text Field Element.

    https://material.io/develop/web/components/input-controls/text-field/
    """

    def control_type(self):
        return 'text'

    def label_text(self):
        return ''

    def wrapper_attrs(self):
        return {
            'class': {
                'dmc-text-field': True,
                'mdc-text-field': True
            }
        }

    def control_attrs(self):
        return {
            'type': self.control_type(),
            'class': {
                'dmc-text-field__input': True,
                'mdc-text-field__input': True,
            }
        }

    def label_attrs(self):
        return {
            'class': {
                'mdc-floating-label': True
            }
        }

    def element(self):
        return Div(**self.wrapper_attrs()) / [
            Input(**self.control_attrs()),
            Label(**self.label_attrs()) / [self.label_text()],
            Div(class_='mdc-line-ripple')
        ]

    def __str__(self):
        return str(self.element())


class TextInput(MDCTextInput):
    """Django-bound text field."""

    def __init__(self, render, controller=None):
        self.renderer = render
        self.controller = controller

    def control_type(self):
        return self.renderer.widget.input_type

    def label_text(self):
        return self.renderer.bound_field.label

    def wrapper_attrs(self):
        attrs = super().wrapper_attrs()
        attrs['data-controller'] = self.controller
        attrs['class'].update({
            'mdc-text-field--upgraded': True,
            'mdc-text-field--invalid': bool(self.renderer.errors)
        })
        return attrs

    def control_attrs(self):
        attrs = super().control_attrs()
        attrs.update({
            'disabled': self.renderer.disabled,
            'id': self.renderer.bound_field.id_for_label,
            'name': self.renderer.bound_field.html_name,
            'value': self.renderer.formatted_value,
            'required': self.renderer.required,
            **self.renderer.widget.attrs
        })
        return attrs

    def label_attrs(self):
        attrs = super().label_attrs()
        attrs['class'].update({
            'mdc-text-field__label--float-above': bool(self.renderer.formatted_value)
        })
        attrs['for'] = self.renderer.bound_field.id_for_label
        return attrs


class PasswordInput(TextInput):
    """Django-bound password field."""
    def control_attrs(self):
        attrs = super().control_attrs()
        attrs.update({
            'data-target': f'{self.controller}.input'
        })
        return attrs

    def toggle_attrs(self):
        return {
            'class': {
                'material-icons': True,
                'dmc-password-field__toggle': True
            },
            'href': '#',
            'tabindex': '-1',
            'aria-hidden': 'true',
            'data-action': f'{self.controller}#toggle'
        }

    def toggle(self):
        return A(**self.toggle_attrs()) / ["visibility"]

    def element(self):
        element = super().element()
        element.body.append(self.toggle())
        return element


class InputRenderer(FormFieldRender):
    wrapper_class = None
    control_class = TextInput

    def controller(self):
        return "dmc-input-field"

    def help_text(self):
        classes = [
            "dmc-text-field-helptext",
            "mdc-text-field-helper-text",
            "mdc-text-field-helper-text--persistent",
            "mdc-text-field-helper-text--validation-msg"
        ]

        return P(class_=classes) / [
                self.format_help_text()
        ]

    def body(self):
        return [
            self.control_class(self, controller=self.controller()),
            self.help_text(),
        ]


class MaterialInputRenderer(InputRenderer):
    def autoinit(self):
        return self.widget.autoinit

    def prefix(self):
        return self.widget.prefix

    def suffix(self):
        return self.widget.suffix


class PasswordRenderer(InputRenderer):
    wrapper_class = 'dmc-password-field'
    control_class = PasswordInput

    def controller(self):
        return "dmc-password-field"


class MaterialPasswordRenderer(PasswordRenderer):
    def autoinit(self):
        return self.widget.autoinit

    def prefix(self):
        return self.widget.prefix

    def suffix(self):
        return self.widget.suffix
