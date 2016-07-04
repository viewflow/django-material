from django.conf.urls import url, include
from django.views import generic

from . import views

urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./city/'), name="index"),
    url('^city/', include(views.CityViewSet().urls)),
    url('^continent/', include(views.ContinentViewSet().urls)),
    url('^country/', include(views.CountryViewSet().urls)),
    url('^ocean/', include(views.OceanViewSet().urls)),
    url('^sea/', include(views.SeaViewSet().urls)),
]
