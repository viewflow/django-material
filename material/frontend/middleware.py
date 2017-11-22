from django.http import HttpResponseRedirect

try:
    from urllib.parse import urlencode, parse_qs, urlsplit, urlunsplit
except ImportError:
    from urlparse import parse_qs, urlsplit, urlunsplit
    from urllib import urlencode


class SmoothNavigationMiddleware(object):
    """Keep `?back=` queryset parameter on POST requests."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):  # noqa D102
        response = self.get_response(request)

        if isinstance(response, HttpResponseRedirect):
            back = request.GET.get('back')
            if back:
                _, _, back_path, _, _ = urlsplit(back)
                scheme, netloc, path, query_string, fragment = urlsplit(response['location'])
                query_params = parse_qs(query_string)

                if path == back_path:
                    query_params.pop('back', None)
                elif 'back' not in query_params:
                    query_params['back'] = [back]

                new_query_string = urlencode(query_params, doseq=True)
                response['location'] = urlunsplit((scheme, netloc, path, new_query_string, fragment))

        return response
