"""URL configuration for the Atlas CRUD app."""

from django.urls import path
from .views import (
    city_list, city_detail, city_create, city_update, city_delete,
    country_list, country_detail, country_create, country_update, country_delete,
)

app_name = 'atlas'

urlpatterns = [
    # City URLs
    path('cities/', city_list, name='city_list'),
    path('cities/<int:pk>/', city_detail, name='city_detail'),
    path('cities/create/', city_create, name='city_create'),
    path('cities/<int:pk>/update/', city_update, name='city_update'),
    path('cities/<int:pk>/delete/', city_delete, name='city_delete'),
    
    # Country URLs
    path('countries/', country_list, name='country_list'),
    path('countries/<int:pk>/', country_detail, name='country_detail'),
    path('countries/create/', country_create, name='country_create'),
    path('countries/<int:pk>/update/', country_update, name='country_update'),
    path('countries/<int:pk>/delete/', country_delete, name='country_delete'),
]