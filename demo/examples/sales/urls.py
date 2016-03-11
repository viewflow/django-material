from django.conf.urls import url
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./customers/', permanent=False), name="index"),
    url('^customers/$', generic.TemplateView.as_view(template_name="sales/index.html"),
        name="leads"),
    url('^leads/$', generic.TemplateView.as_view(template_name="sales/index.html"),
        name="leads"),
    url('^opportunities/$', generic.TemplateView.as_view(template_name="sales/index.html"),
        name="opportunities"),
    url('^shipment/new/$', views.NewShipmentView.as_view(template_name="sales/form.html"),
        name="shipment_new"),
]
