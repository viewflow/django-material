from material.ptml import Div, Span, Ul, Li, Label
from .base import FieldRender


class SelectRenderer(FieldRender):
    def __str__(self):
        label_classes = {
           "": True,
        }
        element = Div(class_='mdc-form-field dmc-form-field') / [
            Label(for_=self.bound_field.id_for_label, class_=label_classes, style="display:block") / [self.bound_field.label],
            Div(class_="mdc-select", role="listbox", tabindex="0", data_mdc_auto_init="MDCSelect") / [
                Span(class_="mdc-select__selected-text") / ["Pick a food group"],
                Div(class_="mdc-simple-menu mdc-select__menu") / [
                    Ul(class_="mdc-list mdc-simple-menu__items") / [
                        Li(class_="mdc-list-item", role="option", id_="grains", aria_disabled="true") / [
                            "Pick a food group"
                        ],
                        Li(class_="mdc-list-item", role="option", id_="grains", tabindex="0") / [
                            "Bread, Cereal, Rice, and Pasta"
                        ],
                        Li(class_="mdc-list-item", role="option", id_="vegetables", tabindex="0") / [
                            "Vegetables"
                        ],
                        Li(class_="mdc-list-item", role="option", id_="fruit", tabindex="0") / [
                            "Fruit"
                        ],
                        Li(class_="mdc-list-item", role="option", id_="dairy", tabindex="0") / [
                            "Milk, Yogurt, and Cheese"
                        ],
                        Li(class_="mdc-list-item", role="option", id_="meat", tabindex="0") / [
                            "Meat, Poultry, Fish, Dry Beans, Eggs, and Nuts"
                        ],
                        Li(class_="mdc-list-item", role="option", id_="fats", tabindex="0") / [
                            "Fats, Oils, and Sweets"
                        ]
                    ]
                ],
            ],
        ]

        return str(element)
