from django import forms
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from formtools.wizard.views import SessionWizardView
from material.forms import Layout, Row, Span


class WizardForm1(forms.Form):
    # Default renderer will be added later when needed
    title = _("Contact Data")

    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()


class WizardForm2(forms.Form):
    # Default renderer will be added later when needed
    title = _("Message")

    message = forms.CharField(widget=forms.Textarea)
    confirm = forms.BooleanField()

    layout = Layout(Row(Span("message", desktop=10), "confirm"))


class WizardView(SessionWizardView):
    title = _("Mail a client")
    form_list = [WizardForm1, WizardForm2]

    def done(self, form_list, **kwargs):
        return render(
            self.request,
            "formtools/wizard/wizard_done.html",
            {
                "form_data": [form.cleaned_data for form in form_list],
            },
        )
