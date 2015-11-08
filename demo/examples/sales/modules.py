from django.conf.urls import url
from material.frontend import Module

from . import views


class Sales(Module):
    icon = "mdi-communication-quick-contacts-dialer"

    def get_urls(self):
        from django.views import generic
        return [
            url('^$', generic.RedirectView.as_view(url='./customers/', permanent=False), name="index"),
            url('^customers/$', generic.TemplateView.as_view(template_name="{}/index.html".format(self.app_label)),
                name="leads"),
            url('^leads/$', generic.TemplateView.as_view(template_name="{}/index.html".format(self.app_label)),
                name="leads"),
            url('^opportunities/$', generic.TemplateView.as_view(template_name="{}/index.html".format(self.app_label)),
                name="opportunities"),
            url('^shipment/new/$', views.NewShipmentView.as_view(template_name="{}/form.html".format(self.app_label)),
                name="shipment_new"),
        ]
