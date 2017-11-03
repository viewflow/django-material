from django.urls import path
from django.views import generic
from material.views import ModelViewset


class CountryViewset(ModelViewset):
    pass


class CityViewset(ModelViewset):
    detail_url = path(
        'detail/<int:pk>/',
        generic.TemplateView.as_view(template_name='material/base.html'),
        name="detail"
    )

    list_url = path(
        '',
        generic.TemplateView.as_view(template_name='material/base.html'),
        name="list"
    )
