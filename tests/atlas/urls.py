from material import Application, Icon
from . import views


class Atlas(Application):
    title = 'Atlas'
    icon = Icon('public')

    city_viewset = views.CityViewset()
    continent_viewset = views.ContinentViewset()
    country_viewset = views.CountryViewset()
    ocean_viewset = views.OceanViewset()
    sea_viewset = views.SeaViewset()
