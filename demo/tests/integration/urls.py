from django.conf.urls import url, include
from django.views import generic

from . import views

urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./city/'), name="index"),
    url('^city/', include(views.CityViewSet().urls)),
    url('^continent/', include(views.ContinentsViewSet().urls)),
    url('^country/', include(views.CountriesViewSet().urls)),
    url('^ocean/', include(views.OceansViewSet().urls)),
    url('^sea/', include(views.SeasViewSet().urls)),
]