from urllib.parse import urlencode, parse_qs, urlsplit, urlunsplit
from django.http import HttpResponseRedirect


class SmoothNavigationMiddleware(object):
    def process_response(self, request, response):
        if isinstance(response, HttpResponseRedirect):
            category = request.GET.get('category')
            if category:
                scheme, netloc, path, query_string, fragment = urlsplit(response['location'])
                query_params = parse_qs(query_string)
                if 'category' not in query_params:
                    query_params['category'] = [category]
                    new_query_string = urlencode(query_params, doseq=True)
                    response['location'] = urlunsplit((scheme, netloc, path, new_query_string, fragment))

        return response
