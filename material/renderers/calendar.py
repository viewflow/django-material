import re

from django.utils.formats import get_format, localize_input
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _

from material.ptml import A, Aside, Button, Div, Icon, Input, Label, P
from .base import FieldRender, FormFieldRender
from .input import TextInput


def find_target_date_format(proposed_formats=None):
    if not proposed_formats:
        formats = get_format('DATE_INPUT_FORMATS')
    else:
        formats = proposed_formats

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


def date_format_placeholder(date_format):
    i18n = {
        r'%Y': _('YYYY'),
        r'%m': _('MM'),
        r'%d': _('DD'),
    }
    split_format = re.split(r'([.\-/])', date_format)
    items = [i18n.get(item, item) for item in split_format]
    return format_lazy('{}' * len(items), *items)


class InlineCalendar(object):
    def __init__(self, renderer, controller=None, header=False, actions=False):
        self.renderer = renderer
        self.controller = controller
        self.with_header = header
        self.with_actions = actions

    def wrapper_attrs(self):
        return {
            'class': {
                "dmc-calendar": True,
                "dmc-calendar--disabled": self.renderer.disabled,
            },
            'data-controller': self.controller,
            'data-date-target': self.renderer.bound_field.id_for_label
        }

    def header(self):
        if self.with_header:
            return Div(class_="dmc-calendar-header") / [
                Div(class_="dmc-calendar-header__year mdc-typography--subheading1"),
                Div(class_="dmc-calendar-header__date mdc-typography--display1") / [
                    Div(class_="dmc-calendar-header__weekday"),
                    Div(class_="dmc-calendar-header__day")
                ]
            ]

    def actions(self):
        if self.with_actions:
            return Div(class_="dmc-calendar__actions") / [
                Button(
                    tabindex="3", type_="button",
                    class_="mdc-button mdc-dialog__footer__button mdc-dialog__footer__button--cancel"
                ) / ['cancel'],
                Button(
                    tabindex="2",
                    type_="button",
                    class_="mdc-button mdc-dialog__footer__button mdc-dialog__footer__button--accept"
                ) / ['ok'],
            ]

    def calendar(self):
        return Div(class_='dmc-calendar__surface') / [
            Div(class_='dmc-calendar__month dmc-calendar__month--current') / [
                Div(class_="dmc-calendar__title") / [],
                Div(class_="dmc-calendar__grid") / [
                    Div(class_="dmc-calendar__weekdays") / [],
                    Div(class_="dmc_calendar__days") / []
                ]
            ]
        ]

    def navigation(self):
        return [
            Button(
                class_="mdc-button mdc-button--compact dmc-calendar__prev",
                tabindex="0",
                type_="button",
            ) / [
                Icon('chevron_left')
            ],
            Button(
                class_="mdc-button mdc-button--compact dmc-calendar__next",
                tabindex="0",
                type_="button",
            ) / [
                Icon('chevron_right')
            ]
        ] if not self.renderer.disabled else []

    def element(self):
        return Div(**self.wrapper_attrs()) / [
            self.header(),
            Div(class_="dmc-calendar__body") / [
                self.calendar(),
                *self.navigation(),
                self.actions(),
            ],
        ]

    def __str__(self):
        return str(self.element())


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

    def help_text_attrs(self):
        return {
            'class': {
                "dmc-inline-calendar__helptext": True,
                "dmc-inline-calendar__helptext--invalid": bool(self.errors)
            }
        }

    def hidden_control(self):
        date_format = find_target_date_format(
            [self.widget.format] if self.widget.format else self.field.input_formats)

        value = self.value
        if value:
            value = localize_input(value, date_format)

        input_attrs = {
            'type': 'hidden',
            'id': self.bound_field.id_for_label,
            'name': self.bound_field.html_name,
            'value': value,
            'data-date-format': date_format,
        }
        return Input(**input_attrs)

    def help_text(self):
        return P(**self.help_text_attrs()) / [self.format_help_text()]

    def __str__(self):
        element = Div(**self.wrapper_attrs()) / [
            Div(class_="dmc-form-field__input") / [
                Label(**self.label_attrs()) / [self.bound_field.label],
                InlineCalendar(self, controller='dmc-inline-calendar-field'),
                self.hidden_control(),
                self.help_text(),
            ]
        ]

        return str(element)


class DateTextInput(TextInput):
    def control_attrs(self):
        date_format = find_target_date_format(
            [self.renderer.widget.format] if self.renderer.widget.format else self.renderer.field.input_formats)

        attrs = super().control_attrs()
        attrs['class'].update({
            'dmc-text-field__input--date': True
        })
        attrs.update({
            'placeholder': date_format_placeholder(date_format),
            'data-date-format': date_format,
        })
        return attrs


class DateInputRenderer(FormFieldRender):
    controller = "dmc-date-input-field"

    def wrapper_attrs(self):
        attrs = super().wrapper_attrs()
        attrs.update({
            'data-controller': self.controller
        })
        return attrs

    def help_text_attrs(self):
        return {
            'class': {
                "dmc-datepicker__helptext": True,
                "dmc-datepicker__helptext--invalid": bool(self.errors)
            }
        }

    def suffix(self):
        return A(href='#', class_="mdc-button mdc-button--compact dmc-datepicker__button") / [
            Icon('insert_invitation')
        ]

    def popup(self):
        return Aside(class_='mdc-dialog') / [
            Div(class_='mdc-dialog__surface dmc-datepicker__surface') / [
                Div(class_='mdc-dialog__body') / [
                    InlineCalendar(self, header=True, actions=True, controller='dmc-popup-calendar')
                ]
            ],
            Div(class_="mdc-dialog__backdrop")
        ]

    def help_text(self):
        return P(**self.help_text_attrs()) / [self.format_help_text()]

    def body(self):
        return [
            DateTextInput(self),
            self.help_text(),
            self.popup()
        ]
