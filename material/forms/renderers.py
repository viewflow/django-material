"""
Makes bound_field available in widget templates, fixing Django's limitation.
Injects field context (errors, help_text, label) into widget rendering.
"""

from typing import Any

from django.forms import BoundField, Form
from django.forms.renderers import TemplatesSetting


class ProxyForm:
    """Intercepts form.renderer access to inject bound_field into context."""

    def __init__(self, bound_field: "MaterialBoundField", form: Form) -> None:
        self._bound_field = bound_field
        self._form = form

    def __getattr__(self, attr: str) -> Any:
        if attr == "renderer":
            return BoundRenderer(self._bound_field)
        return getattr(self._form, attr)


class MaterialBoundField(BoundField):
    """Replaces form attribute with proxy to enable renderer interception."""

    def __getattribute__(self, name: str) -> Any:
        if name == "form":
            raw_form = object.__getattribute__(self, "form")
            return ProxyForm(self, raw_form)

        return object.__getattribute__(self, name)


class MaterialFormRenderer(TemplatesSetting):
    """Custom form renderer with material design templates."""

    form_template_name = "material/django/forms/div.html"
    formset_template_name = "material/django/forms/formsets/div.html"
    field_template_name = "material/django/forms/field.html"

    bound_field_class = MaterialBoundField  # Enable our BoundField proxy


class BoundRenderer(MaterialFormRenderer):
    """Injects bound_field into widget template context."""

    def __init__(self, bound_field: "MaterialBoundField") -> None:
        self._bound_field = bound_field
        super().__init__()

    def render(
        self, template_name: str, context: dict[str, Any], request: Any | None = None
    ) -> str:
        # Make field accessible in widget templates
        context["bound_field"] = self._bound_field
        return super().render(f"material/{template_name}", context, request=request)
