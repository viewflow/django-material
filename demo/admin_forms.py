from django.contrib.auth.models import Permission, Group
from django.contrib.admin import site as admin_site
from django.contrib.admin import widgets
from django.utils.encoding import python_2_unicode_compatible

from . import demo as forms


@python_2_unicode_compatible
class FakeFieldFile(object):
    """
    Quacks like a FieldFile (has a .url and unicode representation), but
    doesn't require us to care about storages etc.
    """
    url = 'something.py'

    def __str__(self):
        return self.url


class FilteredSelectMultipleForm(forms.Form):
    description = "FilteredSelectMultiple"
    CHOICES = (
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermelon'))

    field1 = forms.ChoiceField(help_text='stacked', choices=CHOICES,
                               widget=widgets.FilteredSelectMultiple(
                                   verbose_name='Field One',
                                   is_stacked=True))
    field2 = forms.ChoiceField(help_text='not stacked', choices=CHOICES,
                               widget=widgets.FilteredSelectMultiple(
                                   verbose_name='Field One',
                                   is_stacked=False))


class AdminDateWidgetForm(forms.Form):
    description = "AdminDateWidget"

    field1 = forms.DateField(help_text='default', widget=widgets.AdminDateWidget)


class AdminTimeWidgetForm(forms.Form):
    description = "AdminTimeWidget"

    field1 = forms.TimeField(help_text='default', widget=widgets.AdminTimeWidget)


class AdminSplitDateTimeForm(forms.Form):
    description = "AdminSplitDateTime"

    field1 = forms.SplitDateTimeField(help_text='default', widget=widgets.AdminSplitDateTime)


class AdminRadioSelectForm(forms.Form):
    description = "AdminRadioSelect"
    CHOICES = (
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermeloun'))

    field1 = forms.ChoiceField(
        help_text='default', choices=CHOICES, widget=widgets.AdminRadioSelect)


class AdminFileWidgetForm(forms.Form):
    description = "AdminFileWidget"

    field1 = forms.FileField(help_text='default', widget=widgets.AdminFileWidget)
    field2 = forms.FileField(
        help_text='initial value', initial=FakeFieldFile(),
        widget=widgets.AdminFileWidget)
    field3 = forms.FileField(
        help_text='optional', required=False, initial=FakeFieldFile(),
        widget=widgets.AdminFileWidget)


class ForeignKeyRawIdWidgetForm(forms.Form):
    description = "ForeignKeyRawIdWidget"

    field1 = forms.ModelChoiceField(
        help_text='default', queryset=Permission.objects.all(),
        widget=widgets.ForeignKeyRawIdWidget(
            rel=Permission._meta.get_field('content_type').remote_field,
            admin_site=admin_site))


class ManyToManyRawIdWidgetForm(forms.Form):
    description = "ManyToManyRawIdWidget"

    field1 = forms.ModelMultipleChoiceField(
        help_text='default', queryset=Permission.objects.all(),
        widget=widgets.ManyToManyRawIdWidget(
            rel=Group._meta.get_field('permissions').remote_field,
            admin_site=admin_site))


class RelatedFieldWidgetWrapperForm(forms.Form):
    description = "RelatedFieldWidgetWrapper"

    field1 = forms.ModelChoiceField(
        help_text='default', queryset=Permission.objects.all(),
        widget=widgets.RelatedFieldWidgetWrapper(
            widget=forms.Select(),
            rel=Permission._meta.get_field('content_type').remote_field,
            admin_site=admin_site))


class AdminTextareaWidgetForm(forms.Form):
    description = "AdminTextareaWidget"

    field1 = forms.CharField(help_text='default', widget=widgets.AdminTextareaWidget)


class AdminTextInputWidgetForm(forms.Form):
    description = "AdminTextInputWidget"

    field1 = forms.CharField(help_text='default', widget=widgets.AdminTextInputWidget)


class AdminEmailFieldForm(forms.Form):
    description = "AdminEmailInputWidget"

    field1 = forms.EmailField(help_text='default', widget=widgets.AdminEmailInputWidget)


class AdminURLFieldWidgetForm(forms.Form):
    description = "AdminURLFieldWidget"

    field1 = forms.URLField(help_text='default', widget=widgets.AdminURLFieldWidget)


class AdminIntegerFieldWidgetForm(forms.Form):
    description = "AdminIntegerFieldWidget"

    field1 = forms.IntegerField(help_text='default', widget=widgets.AdminIntegerFieldWidget)


class AdminBigIntegerFieldWidgetForm(forms.Form):
    description = "AdminBigIntegerFieldWidget"

    field1 = forms.IntegerField(help_text='default', widget=widgets.AdminBigIntegerFieldWidget)
