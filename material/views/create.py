# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote as urlquote

if TYPE_CHECKING:
    from django.http import HttpResponseBase

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms import Form, ModelForm as DjangoModelForm, Widget
from django.forms.models import modelform_factory
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.views import generic

from material.forms import (
    FormAjaxCompleteMixin,
    FormDependentSelectMixin,
    ModelForm,
    MaterialFormRenderer,
)
from material.utils import has_object_perm, viewprop

from .base import FormLayoutMixin


@method_decorator(login_required, name="dispatch")
class CreateModelView(
    FormLayoutMixin, FormDependentSelectMixin, FormAjaxCompleteMixin, generic.CreateView
):
    """
    View for creating a new model instance.

    Provides a form for creating a new model instance with material design styling.
    Includes permission checks and success message handling.
    """

    viewset: Any | None = None
    layout: Any | None = None
    form_widgets: dict[str, type[Widget]] | None = None
    model: type[models.Model]
    fields: str | list[str] = "__all__"
    form_class: type[Form] | None = None
    object: models.Model

    template_name_suffix = "_create"

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Check if the user has permission to add instances of this model.

        Args:
            request: The current request

        Returns:
            True if the user has permission, False otherwise
        """
        if self.viewset is not None and hasattr(self.viewset, "has_add_permission"):
            return self.viewset.has_add_permission(request.user)
        else:
            return has_object_perm(request.user, "add", self.model)

    def get_object_url(self, obj: models.Model) -> str | None:
        """
        Get the URL for viewing the newly created object.

        Args:
            obj: The model instance

        Returns:
            URL string or None if not available
        """
        if self.viewset is not None and hasattr(self.viewset, "get_object_url"):
            return self.viewset.get_object_url(self.request, obj)
        elif hasattr(obj, "get_absolute_url") and has_object_perm(self.request.user, "change", obj):
            return obj.get_absolute_url()  # type: ignore
        return None

    def message_user(self) -> None:
        """
        Add a success message after creating an object.

        Includes a link to view the object if available.
        """
        url = self.get_object_url(self.object)
        link = ""
        if url:
            link = format_html('<a href="{}">{}</a>', urlquote(url), _("View"))

        message = format_html(
            str(_("The {obj} was added successfully. {link}")),
            obj=str(self.object),
            link=link,
        )
        messages.add_message(self.request, messages.SUCCESS, message, fail_silently=True)

    @viewprop
    def queryset(self) -> models.QuerySet[Any] | None:
        """
        Get the queryset for this view.

        Returns:
            QuerySet instance or None if not available
        """
        if self.viewset is not None and hasattr(self.viewset, "get_queryset"):
            return self.viewset.get_queryset(self.request)
        return None

    def get_form_widgets(self) -> dict[str, type[Widget]] | None:
        """
        Get form widgets for the form.

        Returns:
            Dictionary mapping field names to widget classes or None
        """
        if self.form_widgets is not None:
            return self.form_widgets
        elif self.viewset and hasattr(self.viewset, "get_create_form_widgets"):
            return self.viewset.get_create_form_widgets(self.request)
        elif self.viewset and hasattr(self.viewset, "get_form_widgets"):
            return self.viewset.get_form_widgets(self.request)
        return None

    def get_form_class(self) -> type[Form] | type[DjangoModelForm[Any]]:
        """
        Get the form class for this view.

        Returns:
            Form class for creating model instances
        """
        if self.form_class is not None:
            return self.form_class
        elif self.viewset and hasattr(self.viewset, "get_create_form_class"):
            return self.viewset.get_create_form_class(self.request)
        elif self.viewset and hasattr(self.viewset, "get_form_class"):
            return self.viewset.get_form_class(self.request)
        else:
            return modelform_factory(
                self.model,
                form=ModelForm,
                fields=self.fields,
                widgets=self.get_form_widgets(),  # type: ignore
            )

    def get_form_kwargs(self) -> dict:
        result = super().get_form_kwargs()
        result["renderer"] = MaterialFormRenderer
        return result

    def get_template_names(self) -> list[str]:
        """
        List of templates for the view.

        If no `self.template_name` defined, uses::
             [<app_label>/<model_label>_<suffix>.html,
              <app_label>/<model_label>_form.html,
              'material/views/form.html']

        Returns:
            List of template names to try
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                f"{opts.app_label}/{opts.model_name}{self.template_name_suffix}.html",
                f"{opts.app_label}/{opts.model_name}_form.html",
                "material/views/form.html",
            ]
        return [self.template_name]

    def form_valid(self, form: Form) -> HttpResponseRedirect:
        """
        Process a valid form submission.

        Args:
            form: The validated form

        Returns:
            Redirect response to success URL
        """
        response = super().form_valid(form)
        self.message_user()
        return response  # type: ignore

    def get_success_url(self) -> str:
        """
        Get the URL to redirect to after successful form submission.

        Returns:
            Success URL string
        """
        if self.viewset and hasattr(self.viewset, "get_success_url"):
            return self.viewset.get_success_url(self.request, obj=self.object)
        return "../"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """
        Main entry point for handling requests.

        Checks permissions before processing.

        Args:
            request: The current request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response

        Raises:
            PermissionDenied: If user doesn't have permission
        """
        if not self.has_add_permission(request):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
