from django.urls import path
from django.views.generic.base import RedirectView
from .views import FormView
from .contact_form import ContactForm
from .login_form import LoginForm
from .profile_form import ProfileForm
from .signup_form import SignupForm
from .registration_form import RegistrationForm
from .bank_form import BankForm
from .comment_form import CommentForm
from .hospital_form import HospitalRegistrationForm
from .order_form import OrderForm
from .checkout_form import CheckoutForm
from .wizard_form import WizardView

urlpatterns = [
    path("", RedirectView.as_view(url="contact/", permanent=False)),
    path("contact/", FormView.as_view(form_class=ContactForm, extra_context={'title': 'Contact Form'})),
    path("login/", FormView.as_view(form_class=LoginForm, extra_context={'title': 'Login Form'})),
    path("profile/", FormView.as_view(form_class=ProfileForm, extra_context={'title': 'Profile Form'})),
    path("signup/", FormView.as_view(form_class=SignupForm, extra_context={'title': 'Signup Form'})),
    path("registration/", FormView.as_view(form_class=RegistrationForm, extra_context={'title': 'Registration Form'})),
    path("bank/", FormView.as_view(form_class=BankForm, extra_context={'title': 'Bank Account Form'})),
    path("comment/", FormView.as_view(form_class=CommentForm, extra_context={'title': 'Comment Form'})),
    path("hospital/", FormView.as_view(form_class=HospitalRegistrationForm, extra_context={'title': 'Hospital Registration'})),
    path("order/", FormView.as_view(form_class=OrderForm, extra_context={'title': 'Order Form'})),
    path("checkout/", FormView.as_view(form_class=CheckoutForm, extra_context={'title': 'Checkout Form'})),
    path("wizard/", WizardView.as_view(), name="wizard_form"),
    # User form requires model-based forms, will be implemented later
    # path("user/", UserFormView.as_view(), name="user_form"),
]