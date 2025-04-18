"""
City views for atlas CRUD functionality.
"""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse

from ..models import City
from .base import (
    model_permission_required, 
    get_form_class, 
    paginate_queryset, 
    get_success_url,
    get_object,
)


def get_queryset(search_query=None):
    """
    Get the base city queryset with optional filtering.
    
    Args:
        search_query: Optional search string
    
    Returns:
        Filtered City queryset
    """
    queryset = City.objects.select_related('country').all()
    
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | 
            Q(country__name__icontains=search_query)
        )
    
    return queryset.order_by('country__name', 'name')


@model_permission_required(City, 'view')
def city_list(request, per_page=10):
    """
    Display a list of cities with search and pagination.
    """
    search_query = request.GET.get('q', '')
    queryset = get_queryset(search_query)
    paginator, page = paginate_queryset(queryset, request, per_page)
    
    return render(request, "atlas/city_list.html", {
        'object_list': page.object_list,
        'page_obj': page,
        'search_query': search_query,
    })


@model_permission_required(City, 'view')
def city_detail(request, pk):
    """
    Display details of a single city.
    """
    queryset = get_queryset().select_related('country')
    city = get_object(queryset, pk)
    
    return render(request, "atlas/city_detail.html", {
        'object': city,
    })


@model_permission_required(City, 'add')
def city_create(request, success_url=None):
    """
    Create a new city.
    """
    CityForm = get_form_class(City)
    form = CityForm(request.POST or None)
    
    if form.is_valid():
        city = form.save()
        messages.success(request, f"City {city.name} was created successfully.")
        redirect_url = get_success_url(
            request, 
            city, 
            success_url, 
            reverse('atlas:city_list')
        )
        return HttpResponseRedirect(redirect_url)
    
    return render(request, "atlas/city_form.html", {
        'form': form,
        'form_title': City._meta.verbose_name.title(),
        'action': 'Create',
    })


@model_permission_required(City, 'change')
def city_update(request, pk, success_url=None):
    """
    Update an existing city.
    """
    city = get_object(City.objects, pk=pk)
    
    CityForm = get_form_class(City)
    form = CityForm(request.POST or None, instance=city)
    
    if form.is_valid():
        city = form.save()
        messages.success(request, f"City {city.name} was updated successfully.")
        redirect_url = get_success_url(
            request, 
            city, 
            success_url, 
            reverse('atlas:city_detail', kwargs={'pk': city.pk})
        )
        return HttpResponseRedirect(redirect_url)
    
    return render(request, "atlas/city_form.html", {
        'form': form,
        'object': city,
        'action': 'Update',
    })


@model_permission_required(City, 'delete')
def city_delete(request, pk, success_url=None):
    """
    Delete a city with confirmation.
    """
    city = get_object(City.objects, pk=pk)
    
    if request.method == 'POST':
        city_name = city.name
        city.delete()
        messages.success(request, f"City {city_name} was deleted successfully.")
        redirect_url = get_success_url(
            request, 
            None, 
            success_url, 
            reverse('atlas:city_list')
        )
        return HttpResponseRedirect(redirect_url)
    
    return render(request, "atlas/city_confirm_delete.html", {
        'object': city,
    })