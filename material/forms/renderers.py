"""
Makes bound_field available in widget templates, fixing Django's limitation.
Injects field context (errors, help_text, label) into widget rendering.
"""

from django.forms.bound_field import BoundField
from django.forms.renderers import DjangoTemplates


class ProxyForm:
    """Intercepts form.renderer access to inject bound_field into context."""
    
    def __init__(self, bound_field, form):
        self._bound_field = bound_field
        self._form = form

    def __getattr__(self, attr):
        if attr == "renderer":
            return BoundRenderer(self._bound_field)
        return getattr(self._form, attr)


class MaterialBoundField(BoundField):
    """Replaces form attribute with proxy to enable renderer interception."""
    
    def __getattribute__(self, name):
        if name == "form":
            raw_form = object.__getattribute__(self, "form")
            return ProxyForm(self, raw_form)

        return object.__getattribute__(self, name)


class MaterialFormRenderer(DjangoTemplates):
    """Custom form renderer with material design templates."""
    
    form_template_name = "material/forms/div.html"
    formset_template_name = "material/forms/formsets/div.html"
    field_template_name = "material/forms/field.html"

    bound_field_class = MaterialBoundField  # Enable our BoundField proxy


class BoundRenderer(MaterialFormRenderer):
    """Injects bound_field into widget template context."""
    
    def __init__(self, bound_field):
        self._bound_field = bound_field
        super().__init__()

    def render(self, template_name, context, request=None):
        context["bound_field"] = self._bound_field  # Make field accessible in widget templates
        return super().render(template_name, context, request=request)
