from django.urls import path
from django.views.generic.base import RedirectView
from .views import FormView
from .checkbox import CheckboxInputForm

urlpatterns = [
    path("", RedirectView.as_view(url="checkbox/", permanent=False)),
    path("checkbox/", FormView.as_view(form_class=CheckboxInputForm, extra_context={'title': 'Checkbox Input Form'})),
]