from material import Application
from . import views


class Atlas(Application):
    title = 'Atlas'

    city_viewset = views.CityViewset()
    country_viewset = views.CountryViewset()
