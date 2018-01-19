from django.utils.formats import get_format
from material.ptml import Button, Div, Icon, Input, Label, P

from .base import FieldRender


def find_target_date_format(proposed_format=None):
    if proposed_format is None:
        formats = get_format('DATE_INPUT_FORMATS')
    else:
        formats = [proposed_format]

    supported_formats = [  # input mask friendly formats
        r'%Y-%m-%d', r'%m-%d-%Y',
        r'%Y-%d-%m', r'%d-%m-%Y',
    ]
    for date_format in formats:
        lookup = date_format.replace('.', '-').replace('/', '-')
        if lookup in supported_formats:
            separator = date_format[2]
            return lookup.replace('-', separator)

    raise ValueError("Widget should accept one of input-mask friendly date input format.")


class InlineCalendarRenderer(FieldRender):
    wrapper_class = None

    def wrapper_attrs(self):
        return {
            'class': {
                'dmc-form-field': True,
                'dmc-inline-calendar-field': True,
                'dmc-form-field--invalid': bool(self.errors),
                self.wrapper_class: bool(self.wrapper_class)
            },
            'title': self.bound_field.help_text or self.bound_field.label
        }

    def label_attrs(self):
        return {
            'class': {
                'dmc-inline-calendar__label': True,
                'dmc-inline-calendar__label--invalid': bool(self.errors),
                'dmc-inline-calendar__label--required': self.required
            }
        }

    def control_attrs(self):
        return {
            'class': {
                "dmc-calendar": True,
                "dmc-calendar--disabled": self.disabled,
            },
            'data-mdc-auto-init': self.widget.autoinit,
            'data-date-target': self.bound_field.id_for_label
        }

    def help_text_attrs(self):
        return {
            'class': {
                "dmc-inline-calendar__helptext": True,
                "dmc-inline-calendar__helptext--invalid": bool(self.errors)
            }
        }

    def calendar(self):
        return Div(class_="dmc-calendar__surface") / [
            Div(class_="dmc-calendar__month dmc-calendar__month--current") / [
                Div(class_="dmc-calendar__title") / [],
                Div(class_="dmc-calendar__grid") / [
                    Div(class_="dmc-calendar__weekdays") / [],
                    Div(class_="dmc_calendar__days") / []
                ]
            ]
        ]

    def navigation(self):
        return [
            Button(tabindex="0", class_="mdc-button mdc-button--compact dmc-calendar__prev", type_="button") / [
                Icon('chevron_left')
            ],
            Button(tabindex="0", class_="mdc-button mdc-button--compact dmc-calendar__next", type_="button") / [
                Icon('chevron_right')
            ]
        ] if not self.disabled else []

    def control(self):
        return Div(**self.control_attrs()) / [
            Div(class_="dmc-calendar__body") / [
                self.calendar(),
                *self.navigation(),
            ]
        ]

    def hidden_control(self):
        input_attrs = {
            'type': 'hidden',
            'id': self.bound_field.id_for_label,
            'name': self.bound_field.html_name,
            'value': self.formatted_value,
            'data-date-format': find_target_date_format(self.widget.format),
        }
        return Input(**input_attrs)

    def help_text(self):
        return P(**self.help_text_attrs()) / [self.format_help_text()]

    def __str__(self):
        element = Div(**self.wrapper_attrs()) / [
            Div(class_="dmc-form-field__input") / [
                Label(**self.label_attrs()) / [self.bound_field.label],
                self.control(),
                self.hidden_control(),
                self.help_text(),
            ]
        ]

        return str(element)
