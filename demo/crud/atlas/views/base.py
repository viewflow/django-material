"""
Base module for atlas CRUD functionality.

This module provides common helper functions and decorators for CRUD operations.
"""

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import modelform_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from functools import wraps


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


def get_object(queryset, pk):
    """
    Get a single object from a queryset by primary key.
    
    Args:
        queryset: The base queryset to filter
        pk: The primary key value
    
    Returns:
        The requested object or raises Http404
    """
    return get_object_or_404(queryset, pk=pk)