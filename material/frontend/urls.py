from django.conf.urls import include, url
from . import default_registry, views


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/', views.profile),
    url(r'^accounts/avatar/', views.avatar),
    url(r'^', include(default_registry.urls)),
]
