"""Django form widgets that render `@robustarush/material` web components."""

from django.forms.widgets import Textarea


class MaterialTextarea(Textarea):
    """Renders <material-textarea> with form-association.

    Django field errors are not propagated automatically — set ``error`` /
    ``error-text`` from the surrounding template if needed (e.g. via a
    BoundField-aware renderer).
    """

    template_name = "material/widgets/textarea.html"

    def __init__(
        self,
        attrs=None,
        *,
        variant="outlined",
        label=None,
        help_text=None,
        auto_resize=False,
        min_rows=None,
        max_rows=None,
    ):
        base = {"rows": 3}
        if attrs:
            base.update(attrs)
        super().__init__(base)
        self.variant = variant
        self.label = label
        self.help_text = help_text
        self.auto_resize = auto_resize
        self.min_rows = min_rows
        self.max_rows = max_rows

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ctx["widget"].update(
            {
                "variant": self.variant,
                "label": self.label,
                "help_text": self.help_text,
                "auto_resize": self.auto_resize,
                "min_rows": self.min_rows,
                "max_rows": self.max_rows,
            }
        )
        return ctx
