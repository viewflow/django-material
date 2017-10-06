from material.ptml import Div, I, P, Input, Label
from .base import FieldRender


class InputRenderer(FieldRender):
    def prefix(self):
        return None

    def suffix(self):
        return None

    def autoinit(self):
        return "MDCTextfield"

    def help_text(self):
        if self.bound_field.help_text:
            return P(class_="mdc-textfield-helptext  mdc-textfield-helptext--persistent") / [
                self.bound_field.help_text
            ]

    def __str__(self):
        value = self.bound_field.value()
        textfield_classes = {
            "mdc-textfield": True,
            "dmc-textfield": True,
            "mdc-textfield--upgraded": value
        }
        label_classes = {
            "mdc-textfield__label": True,
            "mdc-textfield__label--float-above": value
        }
        input_attrs = {
            'checked': self.bound_field.value(),
            'class': "mdc-textfield__input dmc-textfield__input",
            'disabled': self.disabled,
            'id': self.bound_field.id_for_label,
            'name': self.bound_field.html_name,
            'type': self.widget.input_type,
            'value': self.widget.format_value(self.bound_field.value())
        }

        element = Div(class_='mdc-form-field dmc-form-field') / [
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
            return I(class_="material-icons dmc-textfield__prefix") / [self.widget.prefix]

    def suffix(self):
        if self.widget.suffix:
            return I(class_="material-icons dmc-textfield__suffix") / [self.widget.suffix]
