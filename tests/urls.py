from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import generic
from django.shortcuts import render

from . import forms


def index_view(request):
    context = {
        'login': forms.LoginForm(),
        'registration': forms.RegistrationForm(),
        'checkout': forms.CheckoutForm(),
        'order': forms.OrderForm(),
        'comment': forms.CommentForm(),
        'bank': forms.BankForm()
    }
    return render(request, 'index.html', context)


urlpatterns = [
    url(r'^$', index_view),
    url(r'^demo/login/$', generic.FormView.as_view(
        form_class=forms.LoginForm, success_url='/demo/login/', template_name="demo.html")),
    url(r'^demo/registration/$', generic.FormView.as_view(
        form_class=forms.RegistrationForm, success_url='/demo/registration/', template_name="demo.html")),
    url(r'^demo/contact/$', generic.FormView.as_view(
        form_class=forms.ContactForm, success_url='/demo/contact/', template_name="demo.html")),
    url(r'^demo/order/$', generic.FormView.as_view(
        form_class=forms.OrderForm, success_url='/demo/order/', template_name="demo.html")),
    url(r'^demo/checkout/$', generic.FormView.as_view(
        form_class=forms.CheckoutForm, success_url='/demo/checkout/', template_name="demo.html")),
    url(r'^demo/comment/$', generic.FormView.as_view(
        form_class=forms.CommentForm, success_url='/demo/comment/', template_name="demo.html")),
    url(r'^demo/bank/$', generic.FormView.as_view(
        form_class=forms.BankForm, success_url='/demo/bank/', template_name="demo.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^foundation/basic/', generic.RedirectView.as_view(url='/?cache=no', permanent=False))
]


if 'zinnia' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^weblog/', include('zinnia.urls', namespace='zinnia'))]
