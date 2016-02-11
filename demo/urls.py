from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import generic
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from material.frontend import urls as frontend_urls

from . import forms, widget_forms


def index_view(request):
    context = {
        'login': forms.LoginForm(),
        'registration': forms.RegistrationForm(),
        'checkout': forms.CheckoutForm(),
        'order': forms.OrderForm(),
        'comment': forms.CommentForm(),
        'bank': forms.BankForm(),
        'hospital': forms.HospitalRegistrationForm(),
    }
    return render(request, 'index.html', context)


class Wizard(SessionWizardView):
    form_list = [forms.WizardForm1, forms.WizardForm2]

    def done(self, form_list, **kwargs):
        return render(self.request, 'formtools/wizard/wizard_done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


class WidgetFormView(generic.FormView):
    template_name = 'widgets_demo.html'

    def form_valid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


urlpatterns = [
    url(r'^$', index_view),

    # demo
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
    url(r'^demo/wizard/$', Wizard.as_view()),
    url(r'^demo/hospital/$', generic.FormView.as_view(
        form_class=forms.HospitalRegistrationForm, success_url='/demo/hospital/', template_name="demo.html")),
    url(r'^foundation/basic/', generic.RedirectView.as_view(url='/?cache=no', permanent=False)),

    # widget test
    url(r'^demo/widget/boolean/$', WidgetFormView.as_view(form_class=widget_forms.BooleanFieldForm)),
    url(r'^demo/widget/char/$', WidgetFormView.as_view(form_class=widget_forms.CharFieldForm)),
    url(r'^demo/widget/choice/$', WidgetFormView.as_view(form_class=widget_forms.ChoiceFieldForm)),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # frontend
    url(r'^frontend/$', generic.RedirectView.as_view(url='/frontend/accounting/', permanent=False), name="index"),
    url(r'', include(frontend_urls)),
]


if 'zinnia' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^weblog/', include('zinnia.urls', namespace='zinnia'))]
