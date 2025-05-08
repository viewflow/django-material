from django import forms
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from import_export.signals import post_export
from material.views import BaseBulkActionView, BulkActionForm


class ExportForm(BulkActionForm):
    file_format = forms.ChoiceField(
        label=_("Format"),
        choices=(),
        required=False,
        widget=forms.RadioSelect(attrs={"inline": True}),
    )

    def __init__(self, formats=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for i, f in enumerate(formats or []):
            choices.append(
                (
                    str(i),
                    f().get_title(),
                )
            )
        self.fields["file_format"].choices = choices


class ExportView(BaseBulkActionView):
    form_class = ExportForm
    template_name = "viewflow/contrib/import_export/export_action.html"
    template_name_suffix = "_export_action"

    def get_form_kwargs(self):
        return {
            "formats": self.viewset.get_export_formats(),
            **super().get_form_kwargs(),
        }

    def get_export_data(self, file_format, queryset, *args, **kwargs):
        data = self.viewset.get_data_for_export(self.request, queryset, *args, **kwargs)
        export_data = file_format.export_data(data)
        return export_data

    def form_valid(self, form):
        formats = self.viewset.get_export_formats()
        file_format = formats[int(form.cleaned_data["file_format"] or "0")]()

        queryset = self.get_queryset()
        export_data = self.get_export_data(file_format, queryset)
        content_type = file_format.get_content_type()
        response = HttpResponse(export_data, content_type=content_type, status=201)
        response["Content-Disposition"] = 'attachment; filename="%s"' % (
            self.viewset.get_export_filename(file_format),
        )
        post_export.send(sender=None, model=self.model)
        return response


class ImportView(FormView):
    template_name = "viewflow/contrib/import_export/import_action.html"
    template_name_suffix = "_import_action"
