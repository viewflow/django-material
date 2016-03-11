from django.conf.urls import include, url
from . import modules


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'', include(modules.urls)),
]
