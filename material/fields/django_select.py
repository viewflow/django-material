from ...html_factory import (
    Part, Label, Select
)

from .base import (
    PartHelpText, PartErrors, PartHiddenInitial,
    ControlWrapper
)


def select(bound_field):
    field = bound_field.field

    options = []
    for option_value, option_label in field.widget.choices:
        pass

    label = Label(
        for_=bound_field.id_for_label()
    ).Attr(
        bound_field, 'label'
    ).Content(
        bound_field.label
    )

    select = Select(
        id_="id_{}".format(bound_field.html_name),
        class_="invalid" if bound_field.errors else None,
        name=bound_field.html_name
    ).Attr(
        bound_field, 'widget', field.widget.attrs
    ).Content(
        Part(bound_field, "options").Content(options)
    )

    return ControlWrapper(
        bound_field, class_="select-field"
    ).Content(
        Part(bound_field, 'prefix'),
        Part(bound_field, 'label').Content(label),
        Part(bound_field, 'control').Content(select),
        PartHelpText(bound_field),
        PartErrors(bound_field),
        PartHiddenInitial(bound_field)
    )
