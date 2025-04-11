from django.urls import path
from django.views.generic.base import RedirectView
from .views import FormView
from .contact_form import ContactForm
from .login_form import LoginForm
from .profile_form import ProfileForm
from .signup_form import SignupForm
from .registration_form import RegistrationForm

urlpatterns = [
    path("", RedirectView.as_view(url="contact/", permanent=False)),
    path("contact/", FormView.as_view(form_class=ContactForm, extra_context={'title': 'Contact Form'})),
    path("login/", FormView.as_view(form_class=LoginForm, extra_context={'title': 'Login Form'})),
    path("profile/", FormView.as_view(form_class=ProfileForm, extra_context={'title': 'Profile Form'})),
    path("signup/", FormView.as_view(form_class=SignupForm, extra_context={'title': 'Signup Form'})),
    path("registration/", FormView.as_view(form_class=RegistrationForm, extra_context={'title': 'Registration Form'})),
]