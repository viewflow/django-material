from django.urls import path
from django.views import generic
from material.views import CRUDViewset


class CountryViewset(CRUDViewset):
    index_url = path(
        '',
        generic.TemplateView.as_view(template_name='material/base.html'),
        name="index"
    )


class CityViewset(CRUDViewset):
    detail_url = path(
        'detail/<int:pk>/',
        generic.TemplateView.as_view(template_name='material/base.html'),
        name="detail"
    )

    index_url = path(
        '',
        generic.TemplateView.as_view(template_name='material/base.html'),
        name="index"
    )
