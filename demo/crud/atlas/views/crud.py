"""
Functional CRUD views for Atlas models.

This module provides a set of functional views that implement Create, Read, Update, 
and Delete operations for City and Country models with minimal context.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import modelform_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from functools import wraps

from ..models import City, Country


def model_permission_required(model, action):
    """
    Decorator to check if the user has the required permission for a model action.
    """
    permission = f"{model._meta.app_label}.{action}_{model._meta.model_name}"
    
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        @permission_required(permission, raise_exception=True)
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper
    
    return decorator


def get_form_class(model, fields=None, exclude=None, widgets=None):
    """
    Create a dynamic ModelForm for the given model.
    """
    if fields is None and exclude is None:
        fields = '__all__'
    
    form_kwargs = {
        'fields': fields,
        'exclude': exclude,
    }
    
    if widgets:
        form_kwargs['widgets'] = widgets
    
    return modelform_factory(model, **form_kwargs)


def paginate_queryset(queryset, request, per_page=10):
    """
    Paginate a queryset and handle page navigation.
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page', 1)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return paginator, page


def get_success_url(request, obj=None, success_url=None, default_url=None):
    """
    Determine the URL to redirect to after a successful form submission.
    
    Args:
        request: The HTTP request
        obj: The model instance that was created/updated/deleted
        success_url: An explicitly provided success URL
        default_url: The default URL to use if no other URLs are provided
    
    Returns:
        URL to redirect to
    """
    if success_url:
        return success_url
    
    if 'next' in request.GET:
        return request.GET['next']
    
    if obj and hasattr(obj, 'get_absolute_url') and callable(obj.get_absolute_url):
        return obj.get_absolute_url()
    
    return default_url


# City CRUD Views

@model_permission_required(City, 'view')
def city_list(request, per_page=10):
    """
    Display a list of cities with search and pagination.
    """
    search_query = request.GET.get('q', '')
    
    # Get base queryset
    queryset = City.objects.select_related('country').all()
    
    # Apply search if provided
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | 
            Q(country__name__icontains=search_query)
        )
    
    # Apply ordering
    queryset = queryset.order_by('country__name', 'name')
    
    # Paginate the results
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
    city = get_object_or_404(City.objects.select_related('country'), pk=pk)
    
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
    city = get_object_or_404(City, pk=pk)
    
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
    city = get_object_or_404(City, pk=pk)
    
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


# Country CRUD Views

@model_permission_required(Country, 'view')
def country_list(request, per_page=10):
    """
    Display a list of countries with search and pagination.
    """
    search_query = request.GET.get('q', '')
    
    # Get base queryset
    queryset = Country.objects.select_related('continent').all()
    
    # Apply search if provided
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | 
            Q(code__icontains=search_query) |
            Q(continent__name__icontains=search_query)
        )
    
    # Apply ordering
    queryset = queryset.order_by('name')
    
    # Paginate the results
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
    country = get_object_or_404(
        Country.objects.select_related('continent').prefetch_related('cities'), 
        pk=pk
    )
    
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
    country = get_object_or_404(Country, pk=pk)
    
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
    country = get_object_or_404(Country, pk=pk)
    
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