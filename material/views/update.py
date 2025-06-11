# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any
from urllib.parse import quote as urlquote

if TYPE_CHECKING:
    from django.http import HttpResponseBase

from django.contrib import messages
from django.contrib.admin.utils import unquote
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.forms import Form, ModelForm as DjangoModelForm, Widget
from django.forms.models import modelform_factory
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.views import generic

from material.forms import FormAjaxCompleteMixin, FormDependentSelectMixin, ModelForm
from material.utils import has_object_perm, viewprop

from .base import FormLayoutMixin


@method_decorator(login_required, name="dispatch")
class UpdateModelView(
    FormLayoutMixin, FormDependentSelectMixin, FormAjaxCompleteMixin, generic.UpdateView
):
    """
    View for updating an existing model instance.

    Provides a form for editing an existing model instance with material design styling.
    Includes permission checks and success message handling.
    """

    viewset: Any | None = None
    layout: Any | None = None
    form_widgets: dict[str, type[Widget]] | None = None
    model: type[models.Model]
    fields: str | list[str] = "__all__"
    form_class: type[Form] | None = None
    object: models.Model
    page_actions: Sequence[dict[str, Any]] | None = None

    template_name_suffix = "_update"

    def has_change_permission(self, request: HttpRequest, obj: models.Model | None = None) -> bool:
        """
        Check if the user has permission to change this model instance.

        Args:
            request: The current request
            obj: The model instance being changed, or None

        Returns:
            True if the user has permission, False otherwise
        """
        if self.viewset is not None and hasattr(self.viewset, "has_change_permission"):
            return self.viewset.has_change_permission(request.user, obj=obj)
        else:
            return has_object_perm(request.user, "change", self.model, obj=obj)

    def get_object_url(self, obj: models.Model) -> str | None:
        """
        Get the URL for viewing the object.

        Args:
            obj: The model instance

        Returns:
            URL string or None if not available
        """
        if self.viewset is not None and hasattr(self.viewset, "get_object_url"):
            return self.viewset.get_object_url(self.request, obj)
        elif hasattr(obj, "get_absolute_url") and self.has_change_permission(self.request, obj):
            return obj.get_absolute_url()  # type: ignore
        return None

    def get_page_actions(self, *actions: Any) -> Sequence[dict[str, Any]]:
        """
        Get actions to display on the page.

        Args:
            *actions: Additional actions to include

        Returns:
            List of action dictionaries
        """
        result = list(actions)
        if self.viewset and hasattr(self.viewset, "get_update_page_actions"):
            result = self.viewset.get_update_page_actions(self.request, self.object) + result
        if self.page_actions:
            result = list(self.page_actions) + result
        return result

    def message_user(self) -> None:
        """
        Add a success message after updating an object.

        Includes a link to view the object if available.
        """
        url = self.get_object_url(self.object)
        link = ""
        if url:
            link = format_html('<a href="{}">{}</a>', urlquote(url), _("View"))

        message = format_html(
            str(_("The {obj} was changed successfully. {link}")),
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
        elif self.viewset and hasattr(self.viewset, "get_update_form_widgets"):
            return self.viewset.get_update_form_widgets(self.request)
        elif self.viewset and hasattr(self.viewset, "get_form_widgets"):
            return self.viewset.get_form_widgets(self.request)
        return None

    def get_form_class(self) -> type[Form] | type[DjangoModelForm[Any]]:
        """
        Get the form class for this view.

        Returns:
            Form class for updating model instances
        """
        if self.form_class is not None:
            return self.form_class
        elif self.viewset and hasattr(self.viewset, "get_update_form_class"):
            return self.viewset.get_update_form_class(self.request)
        elif self.viewset and hasattr(self.viewset, "get_form_class"):
            return self.viewset.get_form_class(self.request)
        else:
            return modelform_factory(
                self.model,
                form=ModelForm,
                fields=self.fields,
                widgets=self.get_form_widgets(),  # type: ignore
            )

    def get_object(self) -> models.Model:
        """
        Get the object to be updated.

        Returns:
            Model instance to update

        Raises:
            Http404: If the object doesn't exist
            PermissionDenied: If the user doesn't have permission to change it
        """
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            pk = unquote(pk)
            try:
                self.kwargs[self.pk_url_kwarg] = self.model._meta.pk.to_python(pk)
            except (ValidationError, ValueError):
                raise Http404 from None
        obj = super().get_object()

        if not self.has_change_permission(self.request, obj):
            raise PermissionDenied

        return obj

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
        # Object permission check is done in get_object
        return super().dispatch(request, *args, **kwargs)
