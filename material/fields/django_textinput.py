from ...html_factory import (
    Part, Div, Input, Label
)

from .base import (
    PartHelpText, PartErrors, PartHiddenInitial,
    attrs, attr
)


def textinput(bound_field):
    field = bound_field.field

    group_class = attrs("input-field", "col", "s12", attr("required", field.required))
    input_class = attr("invalid", bound_field.errors)
    control_id = "id_{}_control".format(bound_field.html_name)
    widget_id = "id_{}".format(bound_field.html_name)

    return Part(bound_field) / [
        Div(class_name="row", tag_id=control_id) / [
            Div(attr_group="group", tag_class=group_class) / [
                Part(bound_field, 'prefix'),
                Part(bound_field, 'control') / [
                    Input(
                        attr_group='widget',
                        attr_defaults=field.widget.attrs,
                        tag_id=widget_id,
                        tag_type=field.widget.input_type,
                        tag_class=input_class,
                        name=bound_field.html_name,
                        value=bound_field.value()
                    )
                ],
                Part(bound_field, 'label') / [
                    Label(
                        attr_group=(field, 'label'),
                        tag_for=bound_field.if_for_label(),
                        tag_class=attr("active", bound_field.value())
                    ) / [bound_field.label]
                ],
                PartHelpText(bound_field),
                PartErrors(bound_field),
                PartHiddenInitial(bound_field)
            ]
        ]
    ]
