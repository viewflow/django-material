from material.ptml import Div
from .base import get_field_renderer


class FormRenderer(object):
    def __init__(self, form, layout=None):
        self.form = form
        self.layout = layout

    def non_field_errors(self):
        errors = self.form.non_field_errors()
        return Div(class_="dmc-form__errors") / [
            Div(class_="dmc-form__error") / [error] for error in errors
        ] if errors else None

    def hidden_fields(self):
        hidden_fields = self.form.hidden_fields()
        return Div(class_="dmc-form__hiddenfields") / [
            str(bound_field) for bound_field in hidden_fields
        ] if hidden_fields else None

    def render_layout(self):
        return self.layout.render(self.form)

    def render_visible_fields(self):
        return Div(class_="dmc-form__visiblefields mdc-layout-grid__inner") / [
            Div(class_="mdc-layout-grid__cell mdc-layout-grid__cell--span-12") / [
                get_field_renderer(bound_field.field)(bound_field)
            ] for bound_field in self.form.visible_fields()
        ]

    def as_ptml(self):
        return Div(class_="dmc-form mdc-layout-grid") / [
            self.non_field_errors(),
            self.hidden_fields(),
            self.render_layout() if self.layout else self.render_visible_fields()
        ]

    def __str__(self):
        return str(self.as_ptml())
