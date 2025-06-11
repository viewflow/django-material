# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.db.models import Model, QuerySet
    from django.forms import Form
    from django.http import HttpRequest

from django.db import router
from django.db.models.deletion import Collector
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.functional import cached_property
from django.views import generic
from django.views.generic.list import MultipleObjectMixin
from .base import BulkActionForm
from .filters import FilterableViewMixin


class BaseBulkActionView(FilterableViewMixin, MultipleObjectMixin, generic.FormView):
    model: type[Model] | None = None
    viewset: Any = None
    form: Form  # Set in post method
    object_list: QuerySet[Any]  # Set by get_queryset
    filterset: Any  # Set by FilterableViewMixin

    form_class = BulkActionForm
    template_name_suffix = "_action"

    def get_template_names(self) -> list[str]:
        opts = self.model._meta  # type: ignore
        names = [
            "{}/{}{}.html".format(opts.app_label, opts.model_name, self.template_name_suffix),
        ]
        if self.template_name:
            names.append(self.template_name)
        return names

    def get_success_url(self) -> str:
        if self.viewset and hasattr(self.viewset, "get_success_url"):
            return self.viewset.get_success_url(self.request)
        return "../"

    def get_form_kwargs(self) -> dict[str, Any]:
        return {
            "model": self.model,
            **super().get_form_kwargs(),
        }

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()  # type: ignore
        pks = self.request.POST.getlist("pk")
        select_all = self.request.POST.get("select_all")
        if not select_all and pks:
            queryset = queryset.filter(pk__in=pks)
        self.object_list = queryset
        return queryset

    @cached_property
    def objects_count(self) -> int | None:
        if self.request.POST.get("select_all") and self.filterset and not self.filterset.form.has_changed():
            return None
        return self.object_list.count()

    def form_not_confirmed(self, form: Form) -> Any:
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
        messages.add_message(
            self.request, messages.SUCCESS, "No objects selected", fail_silently=True
        )
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.form = self.get_form()
        self.object_list = self.get_queryset()
        if self.form.is_valid():
            if "_confirm" in self.request.POST:
                return self.form_valid(self.form)
            else:
                return self.form_not_confirmed(self.form)
        else:
            return self.form_invalid(self.form)


class DeleteBulkActionView(BaseBulkActionView):
    template_name = "viewflow/views/delete_action.html"
    template_name_suffix = "_delete_action"

    def get_deleted_objects(self, query: QuerySet[Any]) -> list[tuple[type[Model], list[Model]]]:
        collector = Collector(using=router.db_for_write(self.model))  # type: ignore
        collector.collect(query)  # type: ignore
        return [(model_class, list(objects)) for model_class, objects in collector.data.items()]  # type: ignore

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Extend view context data.
        `{{ deleted_objects }}` - list of related objects to delete
        """
        if hasattr(self, 'form') and self.form.is_valid() and not self.form.cleaned_data.get("select_all"):
            kwargs.setdefault("deleted_objects", self.get_deleted_objects(self.get_queryset()))
        return super(DeleteBulkActionView, self).get_context_data(**kwargs)

    def form_valid(self, form: Form) -> HttpResponseRedirect:
        self.get_queryset().delete()
        self.message_user()
        return HttpResponseRedirect(self.get_success_url())

    def message_user(self) -> None:
        message = "The objects were deleted successfully"
        messages.add_message(self.request, messages.SUCCESS, message, fail_silently=True)
