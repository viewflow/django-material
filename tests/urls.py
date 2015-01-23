from django.conf.urls import include, url
from django.contrib import admin
from django.views import generic

from . import forms


urlpatterns = [
    # Examples:
    # url(r'^$', 'tests.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^demo/login/$', generic.FormView.as_view(
        form_class=forms.LoginForm,
        success_url='/demo/login/',
        template_name="demo.html")),
    url(r'^demo/registration/$', generic.FormView.as_view(
        form_class=forms.RegistrationForm,
        success_url='/demo/registration/',
        template_name="demo.html")),
    url(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^admin/', include(admin.site.urls)),
]
