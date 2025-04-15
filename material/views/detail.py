# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

from collections.abc import Sequence
from typing import Any

from django.contrib.admin.utils import unquote
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views import generic

from material.utils import get_object_data, has_object_perm, viewprop


@method_decorator(login_required, name="dispatch")
class DetailModelView(generic.DetailView):
    viewset: Any | None = None
    page_actions: Sequence[dict[str, Any]] | None = None
    object_actions: Sequence[dict[str, Any]] | None = None

    def has_view_permission(self, user, obj: models.Model | None = None) -> bool:
        if self.viewset is not None and hasattr(self.viewset, "has_view_permission"):
            return self.viewset.has_view_permission(user, obj=obj)
        else:
            return has_object_perm(user, "view", self.model, obj=obj) or has_object_perm(
                user, "change", self.model, obj=obj
            )

    def get_object_data(self) -> dict[str, Any]:
        """List of object fields to display.
        Choice fields values are expanded to readable choice label.
        """
        field_data = {}
        for _field, field_name, value in get_object_data(self.object):
            field_data[field_name] = value
        return field_data

    def get_page_actions(self, *actions) -> Sequence[dict[str, Any]]:
        result = list(actions)
        if self.viewset and hasattr(self.viewset, "get_detail_page_actions"):
            result = self.viewset.get_detail_page_actions(self.request, self.object) + result
        if self.page_actions:
            result = list(self.page_actions) + result
        return result

    def get_object_actions(self, *actions) -> Sequence[dict[str, Any]]:
        result = list(actions)
        if self.viewset and hasattr(self.viewset, "get_detail_page_object_actions"):
            result = self.viewset.get_detail_page_object_actions(self.request, self.object) + result
        if self.object_actions:
            result = list(self.object_actions) + result
        return result

    @viewprop
    def get_object_change_link(self) -> str | None:
        if (
            self.viewset
            and hasattr(self.viewset, "has_change_permission")
            and self.viewset.has_change_permission(self.request.user, self.object)
            and hasattr(self.viewset, "get_change_url")
        ):
            return self.viewset.get_change_url(self.request, self.object.pk)
        return None

    def get_object(self) -> models.Model:
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            pk = unquote(pk)
            try:
                self.kwargs[self.pk_url_kwarg] = self.model._meta.pk.to_python(pk)
            except (ValidationError, ValueError):
                raise Http404 from None
        obj = super().get_object()

        if not self.has_view_permission(self.request.user, obj):
            raise PermissionDenied

        return obj

    def get_template_names(self) -> list[str]:
        """
        List of templates for the view.
        If no `self.template_name` defined, uses::
             [<app_label>/<model_label>_detail.html,
              'material/views/detail.html']
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                f"{opts.app_label}/{opts.model_name}{self.template_name_suffix}.html",
                "material/views/detail.html",
            ]
        return [self.template_name]
