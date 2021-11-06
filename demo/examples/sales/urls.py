from django.urls import path
from django.views import generic

from . import views


urlpatterns = [
    path('', generic.RedirectView.as_view(url='./customers/', permanent=False), name="index"),
    path('customers/', generic.TemplateView.as_view(template_name="sales/index.html"),
        name="leads"),
    path('leads/', generic.TemplateView.as_view(template_name="sales/index.html"),
        name="leads"),
    path('opportunities/', generic.TemplateView.as_view(template_name="sales/index.html"),
        name="opportunities"),
    path('shipment/new/', views.NewShipmentView.as_view(template_name="sales/form.html"),
        name="shipment_new"),
]
