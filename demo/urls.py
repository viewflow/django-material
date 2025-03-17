from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='demo/index.html'), name='index'),
    path('cards/', TemplateView.as_view(template_name='demo/cards.html'), name='cards'),
    path('breadcrumbs/', TemplateView.as_view(template_name='demo/breadcrumbs.html'), name='breadcrumbs'),
]