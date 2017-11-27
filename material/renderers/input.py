from django.utils.html import mark_safe, conditional_escape

from material.ptml import Div, I, P, Input, Label
from .base import FieldRender


class InputRenderer(FieldRender):
    def prefix(self):
        return None

    def suffix(self):
        return None

    def autoinit(self):
        return "MDCTextField"

    def help_text(self, errors):
        classes = [
            "dmc-text-field-helptext",
            "mdc-text-field-helptext",
            "mdc-text-field-helptext--persistent",
            "mdc-text-field-helptext--validation-msg"
        ]

        text = mark_safe('&nbsp;')
        if errors:
            text = '<br/>'.join(conditional_escape(error) for error in errors)
        elif self.bound_field.help_text:
            text = self.bound_field.help_text

        return P(class_=classes) / [
                text
            ]

    def __str__(self):
        value = self.bound_field.value()
        errors = self.bound_field.errors

        wrapper_attrs = {
            'class': {
                'dmc-form-field': True,
                'dmc-form-field--invalid': bool(errors)
            },
            'title': self.bound_field.help_text
        }
        textfield_classes = {
            "dmc-text-field": True,
            "mdc-text-field": True,
            "mdc-text-field--upgraded": bool(value),
            "mdc-text-field--invalid": bool(errors),
        }
        label_classes = {
            "mdc-text-field__label": True,
            "mdc-text-field__label--float-above": bool(value)
        }
        input_attrs = {
            'class': "mdc-text-field__input dmc-text-field__input",
            'disabled': self.disabled,
            'id': self.bound_field.id_for_label,
            'name': self.bound_field.html_name,
            'type': self.widget.input_type,
            'value': self.widget.format_value(self.bound_field.value()),
            **self.field.widget.attrs
        }

        element = Div(**wrapper_attrs) / [
            self.prefix(),
            Div(class_="dmc-form-field__input") / [
                Div(class_=textfield_classes, data_mdc_auto_init=self.autoinit()) / [
                    Input(**input_attrs),
                    Label(for_=self.bound_field.id_for_label, class_=label_classes) / [self.bound_field.label],
                    Div(class_="mdc-text-field__bottom-line")
                ],
                self.help_text(errors),
            ],
            self.suffix()
        ]

        return str(element)


class MaterialInputRenderer(InputRenderer):
    def autoinit(self):
        return self.widget.autoinit

    def prefix(self):
        if self.widget.prefix:
            return self.widget.prefix

    def suffix(self):
        if self.widget.suffix:
            return I(class_="material-icons dmc-text-field__suffix") / [self.widget.suffix]
