from django import forms


class FormSetWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        if value is None:
            value = self.attrs['formset_cls'](prefix=name)
        return '<table>{}</table>'.format(value)

    def get_formset(self, name):
        return self.attrs['formset_cls'](prefix=name)

    def value_from_datadict(self, data, files, name):
        return self.attrs['formset_cls'](data or None, files or None, prefix=name)


class FormSetField(forms.Field):
    widget = FormSetWidget

    def __init__(self, formset_cls, *args, **kwargs):
        self.formset_cls = formset_cls
        super(FormSetField, self).__init__(*args, **kwargs)

    def validate(self, value):
        if not value.is_valid():
            raise forms.ValidationError(value.non_form_errors())

    def clean(self, value):
        value = super(FormSetField, self).clean(value)
        return value.cleaned_data

    def widget_attrs(self, widget):
        return {'formset_cls': self.formset_cls}

    def prepare_value(self, value):
        return value
