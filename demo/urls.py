from django.conf import settings
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.shortcuts import render
from django.views import generic, static

import debug_toolbar

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
    path('', index_view),
    path(r'__debug__/', include(debug_toolbar.urls)),

    # demo
    path(r'demo/login/', generic.FormView.as_view(
        form_class=forms.LoginForm, success_url='/demo/login/', template_name="demo.html")),
    path(r'demo/registration/', generic.FormView.as_view(
        form_class=forms.RegistrationForm, success_url='/demo/registration/', template_name="demo.html")),
    path('demo/contact/', generic.FormView.as_view(
        form_class=forms.ContactForm, success_url='/demo/contact/', template_name="demo.html")),
    path('demo/order/', generic.FormView.as_view(
        form_class=forms.OrderForm, success_url='/demo/order/', template_name="demo.html")),
    path('demo/checkout/', generic.FormView.as_view(
        form_class=forms.CheckoutForm, success_url='/demo/checkout/', template_name="demo.html")),
    path('demo/comment/', generic.FormView.as_view(
        form_class=forms.CommentForm, success_url='/demo/comment/', template_name="demo.html")),
    path('demo/bank/', generic.FormView.as_view(
        form_class=forms.BankForm, success_url='/demo/bank/', template_name="demo.html")),
    path('demo/wizard/', Wizard.as_view()),
    path('foundation/basic/', generic.RedirectView.as_view(url='/?cache=no', permanent=False)),

    # core widgets test
    path('demo/widget/', generic.RedirectView.as_view(url='/demo/widget/boolean/', permanent=False)),
    path('demo/widget/boolean/', WidgetFormView.as_view(form_class=widget_forms.BooleanFieldForm)),
    path('demo/widget/char/', WidgetFormView.as_view(form_class=widget_forms.CharFieldForm)),
    path('demo/widget/choice/', WidgetFormView.as_view(form_class=widget_forms.ChoiceFieldForm)),
    path('demo/widget/date/', WidgetFormView.as_view(form_class=widget_forms.DateFieldForm)),
    path('demo/widget/datetime/', WidgetFormView.as_view(form_class=widget_forms.DateTimeFieldForm)),
    path('demo/widget/decimal/', WidgetFormView.as_view(form_class=widget_forms.DecimalFieldForm)),
    path('demo/widget/duration/', WidgetFormView.as_view(form_class=widget_forms.DurationFieldForm)),
    path('demo/widget/email/', WidgetFormView.as_view(form_class=widget_forms.EmailFieldForm)),
    path('demo/widget/file/', WidgetFormView.as_view(form_class=widget_forms.FileFieldForm)),
    path('demo/widget/filepath/', WidgetFormView.as_view(form_class=widget_forms.FilePathFieldForm)),
    path('demo/widget/float/', WidgetFormView.as_view(form_class=widget_forms.FloatFieldForm)),
    path('demo/widget/image/', WidgetFormView.as_view(form_class=widget_forms.ImageFieldForm)),
    path('demo/widget/integer/', WidgetFormView.as_view(form_class=widget_forms.IntegerFieldForm)),
    path('demo/widget/ipaddress/', WidgetFormView.as_view(form_class=widget_forms.GenericIPAddressFieldForm)),
    path('demo/widget/multiplechoice/', WidgetFormView.as_view(form_class=widget_forms.MultipleChoiceFieldForm)),
    path('demo/widget/nullbolean/', WidgetFormView.as_view(form_class=widget_forms.NullBooleanFieldForm)),
    path('demo/widget/regex/', WidgetFormView.as_view(form_class=widget_forms.RegexFieldForm)),
    path('demo/widget/slug/', WidgetFormView.as_view(form_class=widget_forms.SlugFieldForm)),
    path('demo/widget/time/', WidgetFormView.as_view(form_class=widget_forms.TimeFieldForm)),
    path('demo/widget/url/', WidgetFormView.as_view(form_class=widget_forms.URLFieldForm)),
    path('demo/widget/uuid/', WidgetFormView.as_view(form_class=widget_forms.UUIDField)),
    path('demo/widget/combo/', WidgetFormView.as_view(form_class=widget_forms.ComboFieldForm)),
    path('demo/widget/splitdatetime/', WidgetFormView.as_view(form_class=widget_forms.SplitDateTimeFieldForm)),
    path('demo/widget/modelchoice/', WidgetFormView.as_view(form_class=widget_forms.ModelChoiceFieldForm)),
    path('demo/widget/modelmultichoice/', WidgetFormView.as_view(form_class=widget_forms.ModelMultipleChoiceFieldForm)),

    path('demo/widget/password/', WidgetFormView.as_view(form_class=widget_forms.PasswordInputForm)),
    path('demo/widget/hidden/', WidgetFormView.as_view(form_class=widget_forms.HiddenInputForm)),
    path('demo/widget/textarea/', WidgetFormView.as_view(form_class=widget_forms.TextareaForm)),
    path('demo/widget/radioselect/', WidgetFormView.as_view(form_class=widget_forms.RadioSelectForm)),
    path('demo/widget/checkboxmultiple/', WidgetFormView.as_view(
        form_class=widget_forms.CheckboxSelectMultipleForm)),
    path('demo/widget/fileinput/', WidgetFormView.as_view(form_class=widget_forms.FileInputForm)),
    path('demo/widget/splithiddendatetime/', WidgetFormView.as_view(
        form_class=widget_forms.SplitHiddenDateTimeWidgetForm)),
    path('demo/widget/selectdate/', WidgetFormView.as_view(form_class=widget_forms.SelectDateWidgetForm)),

    # admin widgets test
    path('demo/widget/admin/', generic.RedirectView.as_view(
        url='/demo/widget/admin/filteredselectmultiple/', permanent=False)),
    path('demo/widget/admin/filteredselectmultiple/', AdminFormView.as_view(
        form_class=admin_forms.FilteredSelectMultipleForm)),
    path('demo/widget/admin/admindatewidget/', AdminFormView.as_view(
        form_class=admin_forms.AdminDateWidgetForm)),
    path('demo/widget/admin/admintimewidget/', AdminFormView.as_view(
        form_class=admin_forms.AdminTimeWidgetForm)),
    path('demo/widget/admin/adminsplitdatetime/', AdminFormView.as_view(
        form_class=admin_forms.AdminSplitDateTimeForm)),
    path('demo/widget/admin/adminradioselect/', AdminFormView.as_view(
        form_class=admin_forms.AdminRadioSelectForm)),
    path('demo/widget/admin/adminfilewidget/', AdminFormView.as_view(
        form_class=admin_forms.AdminFileWidgetForm)),
    path('demo/widget/admin/foreignkeyrawidwidget/', AdminFormView.as_view(
        form_class=admin_forms.ForeignKeyRawIdWidgetForm)),
    path('demo/widget/admin/manytomanyrawidwidget/', AdminFormView.as_view(
        form_class=admin_forms.ManyToManyRawIdWidgetForm)),
    path('demo/widget/admin/relatedfieldwidgetwrapper/', AdminFormView.as_view(
        form_class=admin_forms.RelatedFieldWidgetWrapperForm)),
    path('demo/widget/admin/admintextareawidget/', AdminFormView.as_view(
        form_class=admin_forms.AdminTextareaWidgetForm)),
    path('demo/widget/admin/admintextinputwidget/', AdminFormView.as_view(
        form_class=admin_forms.AdminTextInputWidgetForm)),
    path('demo/widget/admin/adminemailfield/', AdminFormView.as_view(
        form_class=admin_forms.AdminEmailFieldForm)),
    path('demo/widget/admin/adminurlfieldwidget/', AdminFormView.as_view(
        form_class=admin_forms.AdminURLFieldWidgetForm)),
    path('demo/widget/admin/adminintegerfieldwidget/', AdminFormView.as_view(
        form_class=admin_forms.AdminIntegerFieldWidgetForm)),
    path('demo/widget/admin/adminbigintegerfieldwidget/', AdminFormView.as_view(
        form_class=admin_forms.AdminBigIntegerFieldWidgetForm)),

    # frontend
    path('frontend/', generic.RedirectView.as_view(url='/frontend/accounting/', permanent=False), name="index"),
    path('', include(frontend_urls)),
]

urlpatterns += [
    re_path(r'^static/(?P<path>.*)', static.serve,
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True})
]

if 'material.frontend' not in settings.INSTALLED_APPS:
    urlpatterns += [path('admin/', include(admin.site.urls))]

if 'django.contrib.flatpages' in settings.INSTALLED_APPS:
    from django.contrib.flatpages import views
    urlpatterns += [re_path(r'^(?P<url>.*/)', views.flatpage)]
