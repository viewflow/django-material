from django.urls import path
from material import Application
from . import views


class Atlas(Application):
    title = 'Atlas'

    def get_urls(self):
        return super().get_urls() + [
            path('city/', [views.CityViewset().urls, 'city']),
            path('country/', [views.CountryViewset().urls, 'country'])
        ]
