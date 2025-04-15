# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

from collections.abc import Collection, Generator
from typing import Any, cast

from django.contrib import messages
from django.contrib.admin.utils import unquote
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models, router
from django.db.models.deletion import Collector
from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.views import generic

from material.utils import has_object_perm, viewprop


@method_decorator(login_required, name="dispatch")
class DeleteModelView(generic.DeleteView):
    viewset: Any | None = None

    def has_delete_permission(self, request: HttpRequest, obj: models.Model | None = None) -> bool:
        if self.viewset is not None:
            return self.viewset.has_delete_permission(request.user, obj=obj)
        else:
            return has_object_perm(request.user, "delete", self.model, obj=obj)

    def get_deleted_objects(
        self,
    ) -> Generator[tuple[type[models.Model], Collection[models.Model]], None, None]:
        collector = Collector(using=router.db_for_write(self.object))
        # Cast to satisfy typechecker (self.object is known to be a models.Model)
        model_obj = cast("models.Model", self.object)
        # Django's type stubs for collect() are not perfect
        collector.collect([model_obj])  # type: ignore
        return ((model_class, objects) for model_class, objects in collector.data.items())

    @viewprop
    def queryset(self) -> models.QuerySet | None:
        if self.viewset is not None and hasattr(self.viewset, "get_queryset"):
            return self.viewset.get_queryset(self.request)
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

        if not self.has_delete_permission(self.request, obj):
            raise PermissionDenied

        return obj

    def get_template_names(self) -> list[str]:
        """
        List of templates for the view.
        If no `self.template_name` defined, uses::
             [<app_label>/<model_label>_delete.html,
              'material/views/confirm_delete.html']
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                f"{opts.app_label}/{opts.model_name}{self.template_name_suffix}.html",
                "material/views/confirm_delete.html",
            ]
        return [self.template_name]

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
        self.object = self.get_object()
        success_url = self.get_success_url()

        # to be sure that str(self.object) works, prepare message before object deletion
        # Type ignore needed because Django's typings don't handle lazy translation well
        message = format_html(
            _("The {obj} was deleted successfully."),  # type: ignore
            obj=str(self.object),
        )
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, message, fail_silently=True)
        return HttpResponseRedirect(success_url)

    def get_success_url(self) -> str:
        if self.viewset and hasattr(self.viewset, "get_success_url"):
            return self.viewset.get_success_url(self.request)
        return "../"
