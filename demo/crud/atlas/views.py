from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from cursor_pagination import CursorPaginator
from material.views import list
from .models import City


def list_view(request: HttpRequest) -> HttpResponse:
    queryset = City.objects.all()

    page = None
    columns = []

    return render(
        request,
        "material/views/list.html",
        {"list": list.List(columns, page)},
    )


def custor_list_view(request: HttpRequest) -> HttpResponse:
    columns = []

    queryset = City.objects.all()
    paginator = CursorPaginator(
        queryset,
        ordering=list.get_ordering(columns, request.GET.get("_order")),
    )
    page = paginator.page(first=10, after=request.GET.get("_page"))

    return render(
        request,
        "material/views/list.html",
        {"list": list.List(columns, page)},
    )
