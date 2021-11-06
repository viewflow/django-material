from django.urls import include, path
from . import modules


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include(modules.urls)),
]
