"""
Layout classes for customizing form rendering.

Provides a set of layout elements that can be used to structure form fields
in various layouts including rows, columns, fieldsets, and spans.
"""

from typing import Any, Dict, List, Optional
from django.forms import Form
from django.template.loader import render_to_string
from django.template import Context


class LayoutElement:
    """Base class for all layout elements."""

    template_name: Optional[str] = None

    def __init__(self, *fields: Any, **kwargs: Any) -> None:
        self.fields = fields
        self.attrs = kwargs

    def render(self, form: Form, context: Optional[Context] = None) -> str:
        """Render this layout element with the given form."""
        if context is None:
            context = Context({})

        field_instances: List[Any] = []
        for field_name in self.fields:
            if isinstance(field_name, LayoutElement):
                field_instances.append(field_name.render(form, context))
            elif field_name in form.fields:
                field_instances.append(form[field_name])

        template_context: Dict[str, Any] = {
            "fields": field_instances,
            "attrs": self.attrs,
            "form": form,
        }
        template_context.update(context.flatten())  # type: ignore

        return render_to_string(self.template_name, template_context)  # type: ignore


class Layout(LayoutElement):
    """Top-level layout container."""

    template_name = "material/layout/layout.html"

    def __init__(self, *elements: Any, **kwargs: Any) -> None:
        super().__init__(*elements, **kwargs)


class Row(LayoutElement):
    """Horizontal arrangement of fields or other layout elements."""

    template_name = "material/layout/row.html"


class Column(LayoutElement):
    """Vertical arrangement of fields or other layout elements."""

    template_name = "material/layout/column.html"


class FieldSet(LayoutElement):
    """Grouping of fields with an optional title."""

    template_name = "material/layout/fieldset.html"

    def __init__(self, title: str, *fields: Any, **kwargs: Any) -> None:
        self.title = title
        super().__init__(*fields, **kwargs)

    def render(self, form: Form, context: Optional[Context] = None) -> str:
        """Override to include title in context."""
        if context is None:
            context = Context({})
        context["title"] = self.title
        return super().render(form, context)  # type: ignore


class Caption(LayoutElement):
    """A heading or label with optional styling."""
    
    template_name = "material/layout/caption.html"
    
    def __init__(self, text: str, **kwargs: Any) -> None:
        self.text = text
        super().__init__(**kwargs)
        
    def render(self, form: Form, context: Optional[Context] = None) -> str:
        """Override to include caption text in context."""
        if context is None:
            context = Context({})
        context["text"] = self.text
        return super().render(form, context)  # type: ignore


class Span(LayoutElement):
    """A field that can specify different widths at different breakpoints."""

    template_name = "material/layout/span.html"

    def __init__(self, field_name: str, **kwargs: Any) -> None:
        # Convert keyword arguments like desktop=3 to class attributes
        # that will be rendered as Tailwind responsive classes
        breakpoint_classes = {}
        for breakpoint, size in kwargs.items():
            if breakpoint in [
                "sm",
                "md",
                "lg",
                "xl",
                "2xl",
                "desktop",
                "tablet",
                "mobile",
            ]:
                if breakpoint == "desktop":
                    breakpoint = "lg"
                elif breakpoint == "tablet":
                    breakpoint = "md"
                elif breakpoint == "mobile":
                    breakpoint = "sm"

                # Convert size to column span class
                if isinstance(size, int) and 1 <= size <= 12:
                    if breakpoint == "sm":
                        breakpoint_classes[f"sm:col-span-{size}"] = True
                    else:
                        breakpoint_classes[f"{breakpoint}:col-span-{size}"] = True

        # Create new kwargs with the breakpoint classes
        new_kwargs = {
            "class": " ".join(key for key, val in breakpoint_classes.items() if val)
        }
        new_kwargs.update(
            {k: v for k, v in kwargs.items() if k not in breakpoint_classes}
        )

        super().__init__(field_name, **new_kwargs)