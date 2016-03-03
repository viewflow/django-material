from django.contrib.admin import widgets
from . import demo as forms


class FilteredSelectMultipleForm(forms.Form):
    description = "FilteredSelectMultiple"
    CHOICES = (
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermeloun'))

    field1 = forms.ChoiceField(help_text='stacked', choices=CHOICES,
                               widget=widgets.FilteredSelectMultiple(
                                   verbose_name='Field One',
                                   is_stacked=True))
    field2 = forms.ChoiceField(help_text='not stacked', choices=CHOICES,
                               widget=widgets.FilteredSelectMultiple(
                                   verbose_name='Field One',
                                   is_stacked=False))


# AdminDateWidget
# AdminTimeWidget
# AdminSplitDateTime
# AdminRadioFieldRenderer
# AdminRadioSelect
# AdminFileWidget
# ForeignKeyRawIdWidget
# ManyToManyRawIdWidget
# RelatedFieldWidgetWrapper
# AdminTextareaWidget
# AdminTextInputWidget
# AdminEmailInputWidget
# AdminURLFieldWidget
# AdminIntegerFieldWidget
# AdminBigIntegerFieldWidget
# AdminCommaSeparatedIntegerFieldWidget
