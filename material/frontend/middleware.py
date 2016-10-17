from django.http import QueryDict, HttpResponseRedirect

try:
    from urllib.parse import urlencode, parse_qs, urlsplit, urlunsplit
except ImportError:
    from urlparse import parse_qs, urlsplit, urlunsplit
    from urllib import urlencode


class SmoothNavigationMiddleware(object):
    """Keep `?back=` queryst parameter on POST requests."""

    def process_response(self, request, response):  # noqa D102
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


class UnpjaxMiddleware(object):
    """Remove the `_pjax` parameter from query string."""

    def process_request(self, request):  # noqa D102
        if "_pjax" in request.META.get("QUERY_STRING", ""):
            qs = QueryDict(request.META.get("QUERY_STRING", ""),
                           encoding=request.encoding, mutable=True)
            qs.pop("_pjax", None)
            request.META["QUERY_STRING"] = qs.urlencode()
            request.META["PJAX"] = True
