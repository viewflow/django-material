from django.utils.html import mark_safe, conditional_escape

from material.ptml import Div, P, A, Input, Label
from .base import FieldRender


class InputRenderer(FieldRender):
    wrapper_class = None

    def autoinit(self):
        return "MDCTextField"

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

        text = mark_safe('&nbsp;')
        if errors:
            text = '<br/>'.join(conditional_escape(error) for error in errors)
        elif self.bound_field.help_text:
            text = self.bound_field.help_text

        return P(class_=classes) / [
                text
            ]

    def control(self, value):
        is_required = (
            self.widget.use_required_attribute(self.bound_field.initial) and
            self.field.required and
            self.bound_field.form.use_required_attribute
        )
        input_attrs = {
            'class': "mdc-text-field__input dmc-text-field__input",
            'disabled': self.disabled,
            'id': self.bound_field.id_for_label,
            'name': self.bound_field.html_name,
            'type': self.widget.input_type,
            'value': self.widget.format_value(value),
            'required': is_required,
            **self.field.widget.attrs
        }

        label_classes = {
            "mdc-text-field__label": True,
            "mdc-text-field__label--float-above": bool(value)
        }

        return [
            Input(**input_attrs),
            Label(for_=self.bound_field.id_for_label, class_=label_classes) / [self.bound_field.label],
            Div(class_="mdc-text-field__bottom-line")
        ]

    def __str__(self):
        value = self.bound_field.value()
        errors = self.bound_field.errors

        wrapper_attrs = {
            'class': {
                'dmc-form-field': True,
                'dmc-form-field--invalid': bool(errors),
                self.wrapper_class: bool(self.wrapper_class)
            },
            'title': self.bound_field.help_text
        }
        textfield_classes = {
            "dmc-text-field": True,
            "mdc-text-field": True,
            "mdc-text-field--upgraded": True,
            "mdc-text-field--invalid": bool(errors),
        }

        element = Div(**wrapper_attrs) / [
            self.prefix(),
            Div(class_="dmc-form-field__input") / [
                Div(class_=textfield_classes, data_mdc_auto_init=self.autoinit()) / self.control(value),
                self.help_text(errors),
            ],
            self.suffix()
        ]

        return str(element)


class MaterialInputRenderer(InputRenderer):
    def autoinit(self):
        return self.widget.autoinit

    def prefix(self):
        return self.widget.prefix

    def suffix(self):
        return self.widget.suffix


class PasswordRenderer(InputRenderer):
    wrapper_class = 'dmc-password-field'

    def autoinit(self):
        return "DMCPasswordField"

    def control(self, value):
        toggle_attrs = {
            'class': 'material-icons dmc-password-field__toggle',
            'href': '#',
            'tabindex': '-1',
            'aria-hidden': 'true'
        }
        return super().control(value) + [
            A(**toggle_attrs) / ["visibility"]
        ]


class MaterialPasswordRenderer(PasswordRenderer):
    def autoinit(self):
        return self.widget.autoinit

    def prefix(self):
        return self.widget.prefix

    def suffix(self):
        return self.widget.suffix
