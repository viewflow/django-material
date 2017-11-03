from django.core.exceptions import PermissionDenied


class SiteMiddleware(object):
    """
    Middleware that sets `site` and `app` attributes to request.resolver_match object.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if not hasattr(request, 'user'):
            raise ValueError(
                'No `request.user` found. `django.contrib.auth.context_processors.auth` '
                'missing or `material.middleware.site included before it.` '
                'You need to add auth middleware or change middlewares order.')
        match = request.resolver_match
        if match:
            extra = getattr(match.url_name, 'extra', {})
            site, app = extra.get('site'), extra.get('app')

            if site:
                request.resolver_match.site = site
                if not site.has_perm(request.user):
                    raise PermissionDenied

            if app:
                request.resolver_match.app = app
                if not app.has_perm(request.user):
                    raise PermissionDenied

        return None
