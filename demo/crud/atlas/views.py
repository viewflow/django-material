"""
Demo views for showcasing Material library's list view capabilities with standard and cursor-based pagination.

These views illustrate how to:
- Render a paginated table using standard Django pagination.
- Render a paginated and sortable table using cursor-based pagination for efficient navigation of large datasets.
- Use custom column definitions and ordering, including related model lookups.
"""

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from cursor_pagination import CursorPaginator
from material.views import list
from .models import City


def list_view(request: HttpRequest) -> HttpResponse:
    """
    Display a paginated list of cities using Django's standard pagination.'
    """
    queryset = City.objects.all()
    columns = [
        list.Column("name"),
        list.Column("is_capital"),
    ]

    ordering = list.get_ordering(columns, request.GET.get("_order"))
    queryset = queryset.order_by(*ordering)

    page_num = request.GET.get("_next") or request.GET.get("_prev") or 1
    paginator = Paginator(queryset, 25)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(
        request,
        "material/views/list.html",
        {"list": list.List(columns, page)},
    )


def cursor_list_view(request: HttpRequest) -> HttpResponse:
    """
    Display a paginated and sortable list of cities using cursor-based pagination.
    """
    queryset = City.objects.all().order_by("id")

    columns = [
        list.Column("name"),
        list.Column("is_capital"),
        list.Column("country__name"),
    ]

    ordering = list.get_ordering(columns, request.GET.get("_order"))
    paginator = CursorPaginator(queryset, ordering=ordering)

    after = request.GET.get("_next")
    before = request.GET.get("_prev") if after is None else None
    page_kwargs = {"first": 25} if after or not before else {"last": 25}
    page = paginator.page(after=after, before=before, **page_kwargs)

    return render(
        request,
        "material/views/list.html",
        {"list": list.List(columns, page)},
    )
