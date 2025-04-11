from django.conf import settings
from django.views import generic
from django.urls import path, reverse_lazy
from django.utils.translation import gettext_lazy as _

from viewflow import Icon
from viewflow.urls import Application, AppMenuMixin

from .bank_form import BankForm
from .checkout_form import CheckoutForm
from .comment_form import CommentForm
from .contact_form import ContactForm
from .hospital_form import HospitalRegistrationForm
from .login_form import LoginForm
from .order_form import OrderForm
from .profile_form import ProfileForm
from .registration_form import RegistrationForm
from .signup_form import SignupForm
from .wizard_form import WizardView
from .views import CheckoutFormView, CreateUserView


class Forms(AppMenuMixin, Application):
    title = _("Forms")
    icon = Icon("dynamic_form")
    menu_template_name = "forms/app_menu.html"
    permission = (lambda user: user.is_staff,)

    bank_form_path = path(
        "bank/",
        generic.FormView.as_view(
            form_class=BankForm,
            success_url="/forms/bank/",
            template_name="forms/form.html",
            extra_context={
                "title": "Personal Bank Account Initial Application",
                "button": "Save application",
            },
        ),
        name="bank_form",
    )

    checkout_form_path = path(
        "checkout/",
        CheckoutFormView.as_view(
            form_class=CheckoutForm,
            success_url="/forms/checkout/",
            template_name="forms/form.html",
            extra_context={"title": "Checkout form", "button": "Submit request"},
        ),
        name="checkout_form",
    )

    if settings.DEBUG:
        comment_form_path = path(
            "comment/",
            generic.FormView.as_view(
                form_class=CommentForm,
                success_url="/forms/comment/",
                template_name="forms/form.html",
                extra_context={"title": "Comment form", "button": "Add comment"},
            ),
            name="comment_form",
        )

    contact_form_path = path(
        "contact/",
        generic.FormView.as_view(
            form_class=ContactForm,
            success_url="/forms/contact/",
            template_name="forms/form.html",
            extra_context={"title": "Contact Form", "button": "Send message"},
        ),
        name="contact_form",
    )

    hospital_form_path = path(
        "hospital/",
        generic.FormView.as_view(
            form_class=HospitalRegistrationForm,
            success_url="/forms/hospital/",
            template_name="forms/form.html",
            extra_context={
                "title": "Hospital registration form",
                "button": "Registration",
            },
        ),
        name="hospital_form",
    )

    login_form_path = path(
        "login/",
        generic.FormView.as_view(
            form_class=LoginForm,
            success_url="/forms/login/",
            template_name="forms/form.html",
            extra_context={"title": "Login form", "button": "Submit"},
        ),
        name="login_form",
    )

    if settings.DEBUG:
        order_form_path = path(
            "order/",
            generic.FormView.as_view(
                form_class=OrderForm,
                success_url="/forms/order/",
                template_name="forms/form.html",
                extra_context={"title": "Order services", "button": "Submit request"},
            ),
            name="order_form",
        )

    profile_form_path = path(
        "profile/",
        generic.FormView.as_view(
            form_class=ProfileForm,
            success_url="/forms/profile/",
            template_name="forms/form.html",
            extra_context={"title": "Profile form", "button": "Submit"},
        ),
        name="profile_form",
    )

    registration_form_path = path(
        "registration/",
        generic.FormView.as_view(
            form_class=RegistrationForm,
            success_url="/forms/registration/",
            template_name="forms/form.html",
            extra_context={"title": "Registration form", "button": "Submit"},
        ),
        name="registration_form",
    )

    signup_form_path = path(
        "signup/",
        generic.FormView.as_view(
            form_class=SignupForm,
            success_url="/forms/signup/",
            template_name="forms/form.html",
            extra_context={"title": "Signup form", "button": "Submit"},
        ),
        name="signup_form",
    )

    wizard_form_path = path("wizard/", WizardView.as_view(), name="wizard_form")

    user_form_path = path(
        "user/",
        CreateUserView.as_view(success_url=reverse_lazy("forms:user_form")),
        name="user_form",
    )
