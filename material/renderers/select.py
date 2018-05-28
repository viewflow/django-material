from material.ptml import Div, Select, Option, Optgroup, Label

from .base import FormFieldRender


class MDCSelectMenu(object):
    """
    MDC Select Menu Element

    https://material.io/develop/web/components/input-controls/select-menus/
    """
    def __init__(self, name, controller=None, label_text=None, optgroups=None, disabled=False):
        self.name = name
        self.controller = controller
        self.label_text = label_text
        self.optgroups = optgroups
        self.disabled = disabled

    def wrapper_attrs(self):
        return {
            'class': {
                'mdc-select': True,
            },
            'data-controller': self.controller
        }

    def control_attrs(self):
        return {
            'class': {
                'mdc-select__native-control': True
            }
        }

    def label_attrs(self):
        return {
            'class': {
                'mdc-floating-label': True,
                'mdc-floating-label--float-above': True,
            }
        }

    def items(self):
        result = []

        for group_name, group_choices, group_index in self.optgroups:
            options = []

            for option in group_choices:
                option_attrs = {}
                options.append(
                    Option(**option_attrs) / [option['label']]
                )

            if group_name is not None:
                result.append(
                    Optgroup(label=group_name) / options
                )
            else:
                result += options

        # <option value="" disabled="" selected="">

        return result

    def element(self):
        return Div(**self.wrapper_attrs()) / [
            Select(**self.control_attrs()) / self.items(),
            Label(**self.label_attrs()) / [self.label_text] if self.label_text is not None else None,
            Div(class_='mdc-line-ripple')
        ]

    def __str__(self):
        return str(self.element())


class SelectRenderer(FormFieldRender):
    control_class = MDCSelectMenu
    controller = 'dmc-select-field'

    def help_text(self):
        pass

    def body(self):
        control = self.control_class(
            name=self.html_name,
            controller=self.controller,
            label_text=self.label_text,
            optgroups=self.widget.optgroups(self.html_name, self.formatted_value),
            disabled=self.disabled
        )

        return [
            control,
            self.help_text(),
        ]

    # def native_control(self, options):
    #     items = []

    #     for group_name, group_choices, group_index in options:
    #         options = []

    #         for option in group_choices:
    #             option_attrs = {
    #                 'disabled': option['value'] == '',
    #                 'value': str(option['value']),
    #                 **option['attrs']
    #             }
    #             options.append(
    #                 Option(**option_attrs) / [option['label']]
    #             )

    #         if group_name is not None:
    #             items.append(
    #                 Optgroup(label=group_name) / options
    #             )
    #         else:
    #             items += options

    #     return Div(class_={
    #             'mdc-select': True,
    #             'mdc-select--disabled': self.disabled,
    #         }) / [
    #         Select(class_="mdc-select__native-control", name=self.bound_field.name, disabled=self.disabled,
    #                #**self.widget.attrs) / items
    #     ]


class MaterialSelectRenderer(SelectRenderer):
    def controller(self):
        return self.widget.controller

    def prefix(self):
        return self.widget.prefix

    def suffix(self):
        return self.widget.suffix
