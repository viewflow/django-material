from django.utils.html import mark_safe, conditional_escape

from material.ptml import (
    Div, Select, Option, Optgroup,
    Ul, Li, P, H3
)
from .base import FieldRender


class SelectRenderer(FieldRender):
    wrapper_class = "dmc-select-field"

    def controller(self):
        return "dmc-select-field"

    def prefix(self):
        return None

    def suffix(self):
        return None

    def help_text(self):
        classes = [
            "dmc-select-field__helptext",
        ]

        text = mark_safe('&nbsp;')
        if self.errors:
            text = '<br/>'.join(conditional_escape(error) for error in self.errors)
        elif self.bound_field.help_text:
            text = self.bound_field.help_text

        return P(class_=classes) / [
                text
            ]

    def selected_text(self, options):
        selected = []
        for _, group_choices, _ in options:
            for option in group_choices:
                if option['selected']:
                    selected.append(option)
        if selected:
            return ','.join(str(option['label']) for option in selected)
        else:
            first_choice = next(iter(self.widget.choices), None)
            if first_choice is not None:
                _, label = first_choice
                if isinstance(label, (list, tuple)):  # options group
                    try:
                        label = label[0][1]
                    except IndexError:
                        pass  # never happens? do nothing
                return label

    def list_items(self, options):
        optgroup_classes = [
            'mdc-list-group__subheader',
            'dmc-select-field__groupheader',
        ]

        for group_name, group_choices, group_index in options:
            items = []

            for option in group_choices:
                option_attrs = {
                    'class': "mdc-list-item",
                    'role': "option",
                    'value': str(option['value']),
                    'aria-selected': option['selected'] and option['value'] != '',
                    'aria-disabled': "true" if option['value'] == '' else False,
                    **option['attrs']
                }
                items.append(
                    Li(**option_attrs) / [option['label']]
                )

            if group_name:
                items.insert(0, H3(class_=optgroup_classes) / [group_name])
                yield Div(class_="mdc-list-group dmc-select-field__group") / items
            else:
                yield from iter(items)

    def control(self, options):
        control_attrs = {
            'class': {
                'mdc-select': True,
                'mdc-select--disabled': self.disabled,
            },
            'role': "listbox",
            'tabindex': "-1" if self.disabled else "0",
        }

        return Div(**control_attrs) / [
            Div(class_="mdc-select__surface", tabindex="0") / [
                Div(class_="mdc-select__label mdc-select__label--float-above") / [self.bound_field.label],
                Div(class_="mdc-select__selected-text") / [self.selected_text(options)],
                Div(class_="mdc-select__bottom-line")
            ],
            Div(class_="mdc-menu mdc-select__menu") / [
                Ul(class_="mdc-list mdc-menu__items") / list(self.list_items(options))
            ]
        ]

    def native_control(self, options):
        items = []

        for group_name, group_choices, group_index in options:
            options = []

            for option in group_choices:
                option_attrs = {
                    'disabled': option['value'] == '',
                    'value': str(option['value']),
                    **option['attrs']
                }
                options.append(
                    Option(**option_attrs) / [option['label']]
                )

            if group_name is not None:
                items.append(
                    Optgroup(label=group_name) / options
                )
            else:
                items += options

        return Select(class_="dmc-select-field__native", name=self.bound_field.name, **self.widget.attrs) / items

    def __str__(self):
        options = list(self.widget.optgroups(self.bound_field.name, self.formatted_value))

        wrapper_attrs = {
            'class': {
                'mdc-form-field': False,
                # 'data-controller': "MDCFormField" if self.controller() else False,
                'dmc-form-field': True,
                'dmc-form-field--invalid': bool(self.errors),
                self.wrapper_class: bool(self.wrapper_class)
            },
            'title': self.bound_field.help_text
        }

        element = Div(**wrapper_attrs) / [
            self.prefix(),
            Div(class_="dmc-form-field__input", data_controller=self.controller()) / [
                # Label(**label_attrs) / [self.bound_field.label],
                self.control(options),
                self.native_control(options),
                self.help_text(),
            ],
            self.suffix()
        ]

        return str(element)


class MaterialSelectRenderer(SelectRenderer):
    def controller(self):
        return self.widget.controller

    def prefix(self):
        return self.widget.prefix

    def suffix(self):
        return self.widget.suffix
