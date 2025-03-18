from django.forms.bound_field import BoundField
from django.forms.renderers import DjangoTemplates


class ProxyForm:
    def __init__(self, bound_field, form):
        self._bound_field = bound_field
        self._form = form

    def __getattr__(self, attr):
        if attr == "renderer":
            return BoundRenderer(self.bound_field)
        return getattr(self._form, attr)


class MaterialBoundField(BoundField):
    def __getattribute__(self, name):
        if name == "form":
            raw_form = object.__getattribute__(self, "form")
            return ProxyForm(self, raw_form)

        return object.__getattribute__(self, name)


class MaterialFormRenderer(DjangoTemplates):
    form_template_name = "material/forms/div.html"
    formset_template_name = "material/forms/formsets/div.html"
    field_template_name = "material/forms/field.html"

    bound_field_class = MaterialBoundField


class BoundRender(MaterialFormRender):
    def __init__(self, bound_field):
        self._bound_field = bound_field

    def render(self, template_name, context, request=None):
        context["bound_field"] = self._bound_field
        return super().render(template_name, context, request=request)
