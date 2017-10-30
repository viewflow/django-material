from django.urls import path
from django.views import generic
from material.views import ModelViewset


class CountryViewset(ModelViewset):
    pass


class CityViewset(ModelViewset):
    detail_view = path(
        'detail/<int:pk>/',
        generic.TemplateView.as_view(template_name='material/base.html'),
        name="detail"
    )

    list_view = path(
        '',
        generic.TemplateView.as_view(template_name='material/base.html'),
        name="list"
    )
