from django.conf.urls import url
from django.views import generic


urlpatterns = [
    url('^$', generic.TemplateView.as_view(template_name="accounting/index.html"), name="index"),
]
