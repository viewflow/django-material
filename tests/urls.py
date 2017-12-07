from django.urls import path
from django.views.generic import FormView, TemplateView

from material import Site
from material.contrib.auth import AuthViewset
from material.contrib.admin import Admin

from .forms import widgets, demo
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

    # widgets
    path('widget/checkboxinput/', FormView.as_view(
        template_name='form.html',
        form_class=widgets.CheckboxInputForm,
        success_url='.')
    ),
    path('widget/textinput/', FormView.as_view(
        template_name='form.html',
        form_class=widgets.TextInputForm,
        success_url='.')
    ),
    path('widget/passwordinput/', FormView.as_view(
        template_name='form.html',
        form_class=widgets.PasswordInputForm,
        success_url='.')
    ),
    path('widget/select/', FormView.as_view(
        template_name='form.html',
        form_class=widgets.SelectForm,
        success_url='.')
    ),

    # demo forms
    path('demo/login/', FormView.as_view(
        template_name='form.html',
        form_class=demo.LoginForm,
        success_url='.')
    ),
    path('demo/contact/', FormView.as_view(
        template_name='form.html',
        form_class=demo.ContactForm,
        success_url='.')
    ),
    path('demo/registration/', FormView.as_view(
        template_name='form.html',
        form_class=demo.RegistrationForm,
        success_url='.')
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
]
