from django.urls import path
from django.views.generic import FormView as BaseFormView


from . import widgets, demo


class FormView(BaseFormView):
    template_name = 'form.html'

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


urlpatterns = [
    # widgets
    path('widget/checkbox/', FormView.as_view(form_class=widgets.CheckboxInputForm)),
    # path('widget/checkboxmultiple/', FormView.as_view(form_class=widgets.CheckboxSelectMultipleForm)),
    # path('widget/combo/', FormView.as_view(form_class=widgets.ComboFieldForm)),
    path('widget/date/', FormView.as_view(form_class=widgets.DateFieldForm)),
    # path('widget/datetime/', FormView.as_view(form_class=widgets.DateTimeFieldForm)),
    path('widget/decimal/', FormView.as_view(form_class=widgets.DecimalFieldForm)),
    # path('widget/duration/', FormView.as_view(form_class=widgets.DurationFieldForm)),
    path('widget/email/', FormView.as_view(form_class=widgets.EmailFieldForm)),
    # path('widget/file/', FormView.as_view(form_class=widgets.FileFieldForm)),
    # path('widget/fileinput/$', FormView.as_view(form_class=widgets.FileInputForm)),
    # path('widget/filepath/', FormView.as_view(form_class=widgets.FilePathFieldForm)),
    path('widget/float/', FormView.as_view(form_class=widgets.FloatFieldForm)),
    path('widget/hidden/', FormView.as_view(form_class=widgets.HiddenInputForm)),
    # path('widget/image/', FormView.as_view(form_class=widgets.ImageFieldForm)),
    path('widget/inlinecalendar/', FormView.as_view(form_class=widgets.InlineCalendarForm)),
    path('widget/integer/', FormView.as_view(form_class=widgets.IntegerFieldForm)),
    # path('widget/ipaddress/', FormView.as_view(form_class=widgets.GenericIPAddressFieldForm)),
    # path('widget/modelchoice/$', FormView.as_view(form_class=widgets.ModelChoiceFieldForm)),
    # path('widget/modelmultichoice/$', FormView.as_view(form_class=widgets.ModelMultipleChoiceFieldForm)),
    # path('widget/multiplechoice/', FormView.as_view(form_class=widgets.MultipleChoiceFieldForm)),
    # path('widget/nullboolean/', FormView.as_view(form_class=widgets.NullBooleanFieldForm)),
    path('widget/passwordinput/', FormView.as_view(form_class=widgets.PasswordInputForm)),
    # path('widget/regex/', FormView.as_view(form_class=widgets.RegexFieldForm)),
    # path('widget/radioselect/', FormView.as_view(form_class=widgets.RadioSelectForm)),
    path('widget/select/', FormView.as_view(form_class=widgets.SelectForm)),
    # path('widget/selectdate/$', FormView.as_view(form_class=widgets.SelectDateWidgetForm)),
    # path('widget/slug/', FormView.as_view(form_class=widgets.SlugFieldForm)),
    # path('widget/splitdatetime/', FormView.as_view(form_class=widgets.SplitDateTimeFieldForm)),
    # path('widget/splithiddendatetime/', FormView.as_view(form_class=widgets.SplitHiddenDateTimeWidgetForm)),
    # path('/widget/textarea/', FormView.as_view(form_class=widgets.TextareaForm)),
    path('widget/textinput/', FormView.as_view(form_class=widgets.TextInputForm)),
    # path('widget/time/', FormView.as_view(form_class=widgets.TimeFieldForm)),
    path('widget/url/', FormView.as_view(form_class=widgets.URLFieldForm)),
    # path('widget/uuid/', FormView.as_view(form_class=widgets.UUIDField)),

    # demo forms
    path('demo/login/', FormView.as_view(form_class=demo.LoginForm)),
    path('demo/contact/', FormView.as_view(form_class=demo.ContactForm)),
    path('demo/registration/', FormView.as_view(form_class=demo.RegistrationForm)),
]
