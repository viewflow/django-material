from django.conf.urls import include, url
from . import modules, views


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/', views.profile),
    url(r'^accounts/avatar/', views.avatar),
    url(r'^', include(modules.urls)),
]
