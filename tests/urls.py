from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView


from material import Site
from material.contrib.auth import AuthViewset
from material.contrib.admin import Admin

from .forms import urls as forms_urls
from .atlas.urls import Atlas
from .employees.urls import Employees


site = Site(
    title="Django Material",
    apps=[
        Atlas(),
        Employees(),
        Admin(),
    ]
)

urlpatterns = [
    path('accounts/', AuthViewset().urls),
    path('', site.urls),

    # components
    path('components/snackbar/', TemplateView.as_view(
        template_name='components/snackbar.html')
    ),

    # pages
    path('page/logged_out/', TemplateView.as_view(
        template_name='registration/logged_out.html')
    ),
    path('page/400/', TemplateView.as_view(
        template_name='400.html')
    ),
    path('page/403/', TemplateView.as_view(
        template_name='403.html')
    ),
    path('page/404/', TemplateView.as_view(
        template_name='404.html')
    ),
    path('page/500/', TemplateView.as_view(
        template_name='500.html')
    ),
] + forms_urls.urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
