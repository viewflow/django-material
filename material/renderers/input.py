from material.ptml import Div, I, P, Input, Label
from .base import FieldRender


class InputRenderer(FieldRender):
    def prefix(self):
        return None

    def suffix(self):
        return None

    def autoinit(self):
        return "MDCTextField"

    def help_text(self):
        if self.bound_field.help_text:
            return P(class_="mdc-text-field-helptext  mdc-text-field-helptext--persistent") / [
                self.bound_field.help_text or " "
            ]

    def __str__(self):
        value = self.bound_field.value()
        textfield_classes = {
            "dmc-text-field": True,
            "mdc-text-field": True,
            "mdc-text-field--upgraded": value
        }
        label_classes = {
            "mdc-text-field__label": True,
            "mdc-text-field__label--float-above": value
        }
        input_attrs = {
            'checked': self.bound_field.value(),
            'class': "mdc-text-field__input dmc-text-field__input",
            'disabled': self.disabled,
            'id': self.bound_field.id_for_label,
            'name': self.bound_field.html_name,
            'type': self.widget.input_type,
            'value': self.widget.format_value(self.bound_field.value())
        }

        element = Div(class_='mdc-form-field dmc-form-field', data_mcd_auto_init="MDCFormField") / [
            self.prefix(),
            Div(class_=textfield_classes, data_mdc_auto_init=self.autoinit()) / [
                Input(**input_attrs),
                Label(for_=self.bound_field.id_for_label, class_=label_classes) / [self.bound_field.label],
            ],
            self.help_text(),
            self.suffix(),
        ]

        return str(element)


class MaterialInputRenderer(InputRenderer):
    def autoinit(self):
        return self.widget.autoinit

    def prefix(self):
        if self.widget.prefix:
            return I(class_="material-icons dmc-text-field__prefix") / [self.widget.prefix]

    def suffix(self):
        if self.widget.suffix:
            return I(class_="material-icons dmc-text-field__suffix") / [self.widget.suffix]
