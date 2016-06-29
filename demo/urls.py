from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.shortcuts import render
from django.views import generic

from formtools.wizard.views import SessionWizardView
from material.frontend import urls as frontend_urls

from . import forms, widget_forms, admin_forms


def index_view(request):
    context = {
        'login': forms.LoginForm(),
        'registration': forms.RegistrationForm(),
        'checkout': forms.CheckoutForm(),
        'order': forms.OrderForm(),
        'comment': forms.CommentForm(),
        'bank': forms.BankForm(),
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


class AdminFormView(generic.FormView):
    template_name = 'admin_demo.html'

    @classmethod
    def as_view(cls, *args, **kwargs):
        return login_required(super(AdminFormView, cls).as_view(*args, **kwargs))

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
    url(r'^foundation/basic/', generic.RedirectView.as_view(url='/?cache=no', permanent=False)),

    # core widgets test
    url(r'^demo/widget/$', generic.RedirectView.as_view(url='/demo/widget/boolean/', permanent=False)),
    url(r'^demo/widget/boolean/$', WidgetFormView.as_view(form_class=widget_forms.BooleanFieldForm)),
    url(r'^demo/widget/char/$', WidgetFormView.as_view(form_class=widget_forms.CharFieldForm)),
    url(r'^demo/widget/choice/$', WidgetFormView.as_view(form_class=widget_forms.ChoiceFieldForm)),
    url(r'^demo/widget/date/$', WidgetFormView.as_view(form_class=widget_forms.DateFieldForm)),
    url(r'^demo/widget/datetime/$', WidgetFormView.as_view(form_class=widget_forms.DateTimeFieldForm)),
    url(r'^demo/widget/decimal/$', WidgetFormView.as_view(form_class=widget_forms.DecimalFieldForm)),
    url(r'^demo/widget/duration/$', WidgetFormView.as_view(form_class=widget_forms.DurationFieldForm)),
    url(r'^demo/widget/email/$', WidgetFormView.as_view(form_class=widget_forms.EmailFieldForm)),
    url(r'^demo/widget/file/$', WidgetFormView.as_view(form_class=widget_forms.FileFieldForm)),
    url(r'^demo/widget/filepath/$', WidgetFormView.as_view(form_class=widget_forms.FilePathFieldForm)),
    url(r'^demo/widget/float/$', WidgetFormView.as_view(form_class=widget_forms.FloatFieldForm)),
    url(r'^demo/widget/image/$', WidgetFormView.as_view(form_class=widget_forms.ImageFieldForm)),
    url(r'^demo/widget/integer/$', WidgetFormView.as_view(form_class=widget_forms.IntegerFieldForm)),
    url(r'^demo/widget/ipaddress/$', WidgetFormView.as_view(form_class=widget_forms.GenericIPAddressFieldForm)),
    url(r'^demo/widget/multiplechoice/$', WidgetFormView.as_view(form_class=widget_forms.MultipleChoiceFieldForm)),
    url(r'^demo/widget/nullbolean/$', WidgetFormView.as_view(form_class=widget_forms.NullBooleanFieldForm)),
    url(r'^demo/widget/regex/$', WidgetFormView.as_view(form_class=widget_forms.RegexFieldForm)),
    url(r'^demo/widget/slug/$', WidgetFormView.as_view(form_class=widget_forms.SlugFieldForm)),
    url(r'^demo/widget/time/$', WidgetFormView.as_view(form_class=widget_forms.TimeFieldForm)),
    url(r'^demo/widget/url/$', WidgetFormView.as_view(form_class=widget_forms.URLFieldForm)),
    url(r'^demo/widget/uuid/$', WidgetFormView.as_view(form_class=widget_forms.UUIDField)),
    url(r'^demo/widget/combo/$', WidgetFormView.as_view(form_class=widget_forms.ComboFieldForm)),
    url(r'^demo/widget/splitdatetime/$', WidgetFormView.as_view(form_class=widget_forms.SplitDateTimeFieldForm)),
    url(r'^demo/widget/modelchoice/$', WidgetFormView.as_view(form_class=widget_forms.ModelChoiceFieldForm)),
    url(r'^demo/widget/modelmultichoice/$', WidgetFormView.as_view(form_class=widget_forms.ModelMultipleChoiceFieldForm)),

    url(r'^demo/widget/password/$', WidgetFormView.as_view(form_class=widget_forms.PasswordInputForm)),
    url(r'^demo/widget/hidden/$', WidgetFormView.as_view(form_class=widget_forms.HiddenInputForm)),
    url(r'^demo/widget/textarea/$', WidgetFormView.as_view(form_class=widget_forms.TextareaForm)),
    url(r'^demo/widget/radioselect/$', WidgetFormView.as_view(form_class=widget_forms.RadioSelectForm)),
    url(r'^demo/widget/checkboxmultiple/$', WidgetFormView.as_view(
        form_class=widget_forms.CheckboxSelectMultipleForm)),
    url(r'^demo/widget/fileinput/$', WidgetFormView.as_view(form_class=widget_forms.FileInputForm)),
    url(r'^demo/widget/splithiddendatetime/$', WidgetFormView.as_view(
        form_class=widget_forms.SplitHiddenDateTimeWidgetForm)),
    url(r'^demo/widget/selectdate/$', WidgetFormView.as_view(form_class=widget_forms.SelectDateWidgetForm)),

    # admin widgets test
    url(r'^demo/widget/admin/$', generic.RedirectView.as_view(
        url='/demo/widget/admin/filteredselectmultiple/', permanent=False)),
    url(r'^demo/widget/admin/filteredselectmultiple/$', AdminFormView.as_view(
        form_class=admin_forms.FilteredSelectMultipleForm)),
    url(r'^demo/widget/admin/admindatewidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminDateWidgetForm)),
    url(r'^demo/widget/admin/admintimewidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminTimeWidgetForm)),
    url(r'^demo/widget/admin/adminsplitdatetime/$', AdminFormView.as_view(
        form_class=admin_forms.AdminSplitDateTimeForm)),
    url(r'^demo/widget/admin/adminradioselect/$', AdminFormView.as_view(
        form_class=admin_forms.AdminRadioSelectForm)),
    url(r'^demo/widget/admin/adminfilewidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminFileWidgetForm)),
    url(r'^demo/widget/admin/foreignkeyrawidwidget/$', AdminFormView.as_view(
        form_class=admin_forms.ForeignKeyRawIdWidgetForm)),
    url(r'^demo/widget/admin/manytomanyrawidwidget/$', AdminFormView.as_view(
        form_class=admin_forms.ManyToManyRawIdWidgetForm)),
    url(r'^demo/widget/admin/relatedfieldwidgetwrapper/$', AdminFormView.as_view(
        form_class=admin_forms.RelatedFieldWidgetWrapperForm)),
    url(r'^demo/widget/admin/admintextareawidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminTextareaWidgetForm)),
    url(r'^demo/widget/admin/admintextinputwidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminTextInputWidgetForm)),
    url(r'^demo/widget/admin/adminemailfield/$', AdminFormView.as_view(
        form_class=admin_forms.AdminEmailFieldForm)),
    url(r'^demo/widget/admin/adminurlfieldwidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminURLFieldWidgetForm)),
    url(r'^demo/widget/admin/adminintegerfieldwidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminIntegerFieldWidgetForm)),
    url(r'^demo/widget/admin/adminbigintegerfieldwidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminBigIntegerFieldWidgetForm)),

    # frontend
    url(r'^frontend/$', generic.RedirectView.as_view(url='/frontend/accounting/', permanent=False), name="index"),
    url(r'', include(frontend_urls)),
]


if 'material.frontend' not in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^admin/', include(admin.site.urls))]

if 'django.contrib.flatpages' in settings.INSTALLED_APPS:
    from django.contrib.flatpages import views
    urlpatterns += [url(r'^(?P<url>.*/)$', views.flatpage)]
