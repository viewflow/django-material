from material.ptml import Div, Input, Svg, Path, Label
from .base import FieldRender


class CheckboxInputRenderer(FieldRender):
    def __str__(self):
        disabled = self.bound_field.field.disabled
        input_attrs = {
            'checked': self.bound_field.value(),
            'class': "mdc-checkbox__native-control",
            'disabled': disabled,
            'id': self.bound_field.id_for_label,
            'name': self.bound_field.html_name,
            'type': "checkbox"
        }

        element = Div(class_='mdc-form-field') / [
            Div(class_={'mdc-checkbox': True, 'mdc-checkbox--disabled': disabled}) / [
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
            ],
            Label(for_=self.bound_field.id_for_label) / [self.bound_field.label]
        ]

        return str(element)
