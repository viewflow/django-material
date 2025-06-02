from django.urls import path
from django.views.generic.base import RedirectView

from .checkbox import CheckboxInputForm
from .select import SelectForm
from .textinput import TextInputForm
from .views import FormView

urlpatterns = [
    path("", RedirectView.as_view(url="checkbox/", permanent=False)),
    path(
        "checkbox/",
        FormView.as_view(
            form_class=CheckboxInputForm, extra_context={"title": "Checkbox Input Form"}
        ),
    ),
    path(
        "text/",
        FormView.as_view(form_class=TextInputForm, extra_context={"title": "Text Input Form"}),
    ),
    path(
        "select/",
        FormView.as_view(form_class=SelectForm, extra_context={"title": "Select Form"}),
    ),
]
