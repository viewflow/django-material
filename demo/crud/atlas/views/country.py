"""
Country views for atlas CRUD functionality.
"""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse

from ..models import Country
from .base import (
    model_permission_required, 
    get_form_class, 
    paginate_queryset, 
    get_success_url,
    get_object,
)


def get_queryset(search_query=None):
    """
    Get the base country queryset with optional filtering.
    
    Args:
        search_query: Optional search string
    
    Returns:
        Filtered Country queryset
    """
    queryset = Country.objects.select_related('continent').all()
    
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | 
            Q(code__icontains=search_query) |
            Q(continent__name__icontains=search_query)
        )
    
    return queryset.order_by('name')


@model_permission_required(Country, 'view')
def country_list(request, per_page=10):
    """
    Display a list of countries with search and pagination.
    """
    search_query = request.GET.get('q', '')
    queryset = get_queryset(search_query)
    paginator, page = paginate_queryset(queryset, request, per_page)
    
    return render(request, "atlas/country_list.html", {
        'object_list': page.object_list,
        'page_obj': page,
        'search_query': search_query,
    })


@model_permission_required(Country, 'view')
def country_detail(request, pk):
    """
    Display details of a single country with its cities.
    """
    queryset = get_queryset().prefetch_related('cities')
    country = get_object(queryset, pk)
    
    cities = country.cities.all()
    
    return render(request, "atlas/country_detail.html", {
        'object': country,
        'cities': cities,
    })


@model_permission_required(Country, 'add')
def country_create(request, success_url=None):
    """
    Create a new country.
    """
    CountryForm = get_form_class(Country)
    form = CountryForm(request.POST or None)
    
    if form.is_valid():
        country = form.save()
        messages.success(request, f"Country {country.name} was created successfully.")
        redirect_url = get_success_url(
            request, 
            country, 
            success_url, 
            reverse('atlas:country_list')
        )
        return HttpResponseRedirect(redirect_url)
    
    return render(request, "atlas/country_form.html", {
        'form': form,
        'form_title': Country._meta.verbose_name.title(),
        'action': 'Create',
    })


@model_permission_required(Country, 'change')
def country_update(request, pk, success_url=None):
    """
    Update an existing country.
    """
    country = get_object(Country.objects, pk=pk)
    
    CountryForm = get_form_class(Country)
    form = CountryForm(request.POST or None, instance=country)
    
    if form.is_valid():
        country = form.save()
        messages.success(request, f"Country {country.name} was updated successfully.")
        redirect_url = get_success_url(
            request, 
            country, 
            success_url, 
            reverse('atlas:country_detail', kwargs={'pk': country.pk})
        )
        return HttpResponseRedirect(redirect_url)
    
    return render(request, "atlas/country_form.html", {
        'form': form,
        'object': country,
        'action': 'Update',
    })


@model_permission_required(Country, 'delete')
def country_delete(request, pk, success_url=None):
    """
    Delete a country with confirmation.
    """
    country = get_object(Country.objects, pk=pk)
    
    # Check if country has cities
    cities_count = country.cities.count()
    
    if request.method == 'POST':
        if 'confirm' in request.POST:
            country_name = country.name
            country.delete()
            messages.success(request, f"Country {country_name} was deleted successfully.")
            redirect_url = get_success_url(
                request, 
                None, 
                success_url, 
                reverse('atlas:country_list')
            )
            return HttpResponseRedirect(redirect_url)
    
    return render(request, "atlas/country_confirm_delete.html", {
        'object': country,
        'cities_count': cities_count,
    })