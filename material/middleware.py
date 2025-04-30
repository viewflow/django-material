# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

from typing import Any, Callable, Dict, Optional, Union

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpRequest, HttpResponse


class SiteMiddleware:
    """
    Middleware that processes site and app permissions based on URL patterns.
    
    This middleware:
    1. Checks if the user has permission to access the current site and app
    2. Adds site and app objects to the request.resolver_match for view access
    3. Injects app context data into template responses
    
    The site and app objects are expected to be provided in the url_name.extra
    dictionary with 'site' and 'app' keys. These objects should implement:
    - has_view_permission(user) method
    - get_context_data(request) method (for app objects)
    """

    def __init__(self, get_response: Callable) -> None:
        """
        Initialize the middleware with the get_response callable.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request and return the response.
        
        Args:
            request: The incoming HTTP request
            
        Returns:
            HttpResponse: The processed response
        """
        return self.get_response(request)

    def process_view(
        self, request: HttpRequest, view_func: Callable, view_args: list, view_kwargs: dict
    ) -> Optional[HttpResponse]:
        """
        Process the view before it's called, checking permissions.
        
        Args:
            request: The incoming HTTP request
            view_func: The view function to be called
            view_args: Positional arguments for the view
            view_kwargs: Keyword arguments for the view
            
        Returns:
            None if processing should continue, HttpResponse otherwise
            
        Raises:
            ImproperlyConfigured: If the auth middleware is not properly set up
            PermissionDenied: If the user doesn't have permission to view the site/app
        """
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "No `request.user` found. `django.contrib.auth.context_processors.auth` "
                "missing or `material.middleware.SiteMiddleware` included before it. "
                "You need to add auth middleware or change middlewares order."
            )
            
        match = request.resolver_match
        if not match:
            return None
            
        # Get site and app from URL pattern extra data
        try:
            extra = getattr(match.url_name, "extra", {}) or {}
        except AttributeError:
            # url_name is not an object with attributes (e.g., it's a string)
            return None
            
        site = extra.get("site")
        app = extra.get("app")

        # Check site permission
        if site and hasattr(site, "has_view_permission"):
            if not site.has_view_permission(request.user):
                raise PermissionDenied

        # Check app permission
        if app and hasattr(app, "has_view_permission"):
            if not app.has_view_permission(request.user):
                raise PermissionDenied

        # Copy all extra attributes to resolver_match for view access
        for name, value in extra.items():
            setattr(match, name, value)

        return None

    def process_template_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """
        Process the template response, adding app context data.
        
        Args:
            request: The HTTP request
            response: The template response
            
        Returns:
            HttpResponse: The processed response with app context
            
        Raises:
            ValueError: If an app context key clashes with the response context
        """
        match = getattr(request, "resolver_match", None)
        if not match:
            return response
            
        app = getattr(match, "app", None)
        if not app or not hasattr(app, "get_context_data"):
            return response
            
        try:
            app_context = app.get_context_data(request)
            
            # Only process if we have context data and it's a dict
            if app_context and hasattr(response, "context_data"):
                for key, value in app_context.items():
                    if key in response.context_data:
                        raise ValueError(
                            f"App context key '{key}' clashes with view response context"
                        )
                    response.context_data[key] = value
        except Exception as e:
            # Log the exception but don't break the response
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error processing app context: {str(e)}")
            
        return response