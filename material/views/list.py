from typing import TYPE_CHECKING, Optional
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views import generic

if TYPE_CHECKING:
    from material.urls import BaseModelViewset

# { page_obj: ?? а вот как page и columns сводить,
#   columns:
# }


class OrderableListViewMixin:
    pass


class BulkActionsMixin:
    pass


class BaseListModelView(generic.ListView):
    """Base class for list views of model objects."""

    request: HttpRequest
    viewset: Optional["BaseModelViewset"]
    model: type[models.Model]

    def get_template_names(self) -> list[str]:
        """
        Return a list of template names to be used for the view.

        If `self.template_name` undefined, uses::
             [<app_label>/<model_label>_list.html,
              'material/views/list.html']

        Returns:
            List of template names to try
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                f"{opts.app_label}/{opts.model_name}{self.template_name_suffix}.html",
                "material/views/list.html",
            ]
        return [self.template_name]


@method_decorator(login_required, name="dispatch")
class ListModelView(BaseListModelView):
    """
    Render a list of model objects with sorting, filtering, and bulk actions.
    """
