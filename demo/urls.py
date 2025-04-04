from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='demo/index.html'), name='index'),
    path('buttons/', TemplateView.as_view(template_name='demo/buttons.html'), name='buttons'),
    path('navigation/', TemplateView.as_view(template_name='demo/navigation.html'), name='navigation'),
    path('tables/', TemplateView.as_view(template_name='demo/tables.html'), name='tables'),
    path('templates/', TemplateView.as_view(template_name='demo/templates.html'), name='templates'),
    path('breadcrumbs/', TemplateView.as_view(template_name='demo/breadcrumbs.html'), name='breadcrumbs'),
    path('colors/', TemplateView.as_view(template_name='demo/colors.html'), name='colors'),
    path('checkboxes/', TemplateView.as_view(template_name='demo/checkboxes.html'), name='checkboxes'),
]