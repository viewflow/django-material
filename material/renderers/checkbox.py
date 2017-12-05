from django.utils.html import conditional_escape

from material.ptml import Div, Input, Svg, P, Path, Label
from .base import FieldRender


class CheckboxInputRenderer(FieldRender):
    wrapper_class = "dmc-checkbox-field"

    def autoinit(self):
        return "MDCCheckbox"

    def prefix(self):
        return None

    def suffix(self):
        return None

    def help_text(self, errors):
        classes = [
            "dmc-text-field-helptext",
            "mdc-text-field-helper-text",
            "mdc-text-field-helper-text--persistent",
            "mdc-text-field-helper-text--validation-msg"
        ]

        text = None
        if errors:
            text = '<br/>'.join(conditional_escape(error) for error in errors)
        elif self.bound_field.help_text:
            text = self.bound_field.help_text

        if text:
            return P(class_=classes) / [
                text
            ]

    def control(self):
        input_attrs = {
            'checked': self.bound_field.value(),
            'class': "mdc-checkbox__native-control",
            'disabled': self.bound_field.field.disabled,
            'id': self.bound_field.id_for_label,
            'name': self.bound_field.html_name,
            'type': "checkbox"
        }

        return [
            Input(**input_attrs),
            Div(class_="mdc-checkbox__background") / [
                Svg(class_="mdc-checkbox__checkmark", viewbox="0 0 24 24") / [
                    Path(
                        class_="mdc-checkbox__checkmark__path",
                        d="M1.73,12.91 8.1,19.28 22.79,4.59",
                        fill="none", stroke="white")
                ],
                Div(class_="mdc-checkbox__mixedmark"),
            ]
        ]

    def __str__(self):
        errors = self.bound_field.errors

        wrapper_attrs = {
            'class': {
                'mdc-form-field': False,
                'dmc-form-field': True,
                'dmc-form-field--invalid': bool(errors),
                self.wrapper_class: bool(self.wrapper_class)
            },
            'title': self.bound_field.help_text
        }

        control_attrs = {
            'class': {
                'mdc-checkbox': True,
                'mdc-checkbox--disabled': self.bound_field.field.disabled,
            },
            'data-mdc-auto-init': self.autoinit()
        }

        element = Div(**wrapper_attrs) / [
            self.prefix(),
            Div(class_="dmc-form-field__input") / [
                Div(class_="mdc-form-field", data_mdc_auto_init="MDCFormField" if self.autoinit() else False) / [
                    Div(**control_attrs) / self.control(),
                    Label(for_=self.bound_field.id_for_label) / [self.bound_field.label],
                ],
                self.help_text(errors),
            ],
            self.suffix(),
        ]

        return str(element)
