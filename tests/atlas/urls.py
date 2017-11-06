from material import Application, Icon
from . import views


class Atlas(Application):
    title = 'Atlas'
    icon = Icon('beach_access')

    city_viewset = views.CityViewset()
    country_viewset = views.CountryViewset()
