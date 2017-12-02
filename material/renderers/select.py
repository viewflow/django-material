from django.utils.html import mark_safe, conditional_escape

from material.ptml import Div, Span, Ul, Li, Label, P, H3
from .base import FieldRender


class SelectRenderer(FieldRender):
    wrapper_class = "dmc-select-field"

    def autoinit(self):
        return "DMCSelect"

    def help_text(self, errors):
        classes = [
            "dmc-select-field__helptext",
        ]

        text = mark_safe('&nbsp;')
        if errors:
            text = '<br/>'.join(conditional_escape(error) for error in errors)
        elif self.bound_field.help_text:
            text = self.bound_field.help_text

        return P(class_=classes) / [
                text
            ]

    def list_items(self):
        optgroup_classes = [
            'mdc-list-group__subheader',
            'dmc-select-field__optgroup',
        ]

        value = self.widget.format_value(self.bound_field.value())
        for group_name, group_choices, group_index in self.widget.optgroups(self.bound_field.name, value):
            if group_name:
                yield H3(class_=optgroup_classes) / [group_name]

            for option in group_choices:
                option_attrs = {
                    'class': "mdc-list-item",
                    'role': "option",
                    'value': str(option['value']),
                    **option['attrs']
                }
                yield Li(**option_attrs) / [
                    option['label']
                ]

    def control(self, value):
        return Div(class_="mdc-select", role="listbox", tabindex="0", data_mdc_auto_init="DMCSelect") / [
            Span(class_="mdc-select__selected-text") / ["Pick a food group"],
            Div(class_="mdc-simple-menu mdc-select__menu") / [
                Ul(class_="mdc-list mdc-simple-menu__items") / list(self.list_items())
            ]
        ]

    def __str__(self):
        value = self.bound_field.value()
        errors = self.bound_field.errors

        wrapper_attrs = {
            'class': {
                'mdc-form-field': False,
                'data-mdc-auto-init': "MDCFormField" if self.autoinit() else False,
                'dmc-form-field': True,
                'dmc-form-field--invalid': bool(errors),
                self.wrapper_class: bool(self.wrapper_class)
            },
            'title': self.bound_field.help_text
        }

        label_attrs = {
           'for': self.bound_field.id_for_label,
           'class': 'dmc-select-field__label',
        }

        element = Div(**wrapper_attrs) / [
            Div(class_="dmc-form-field__input") / [
                Label(**label_attrs) / [self.bound_field.label],
                self.control(value),
                self.help_text(errors),
            ]
        ]

        return str(element)
