from django import forms


class BooleanFieldForm(forms.Form):
    description = "BooleanField options"

    field1 = forms.BooleanField(help_text='default')
    field2 = forms.BooleanField(initial=True, help_text='initial value')


class CharFieldForm(forms.Form):
    description = "CharField options"

    field1 = forms.CharField(help_text='default')
    field2 = forms.CharField(initial="Initial value", help_text='initial value')
    field3 = forms.CharField(min_length=5, max_length=10, help_text='length between 5-10')


class ChoiceFieldForm(forms.Form):
    description = "ChoiceField options"
    CHOICES = (
        (None, 'Select a fruit'),
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermeloun'))
    LONG_CHOICES = ((n, n) for n in range(100))
    
    field1 = forms.ChoiceField(help_text='default', choices=CHOICES)
    field2 = forms.ChoiceField(help_text='initial value', choices=CHOICES, initial=2)
    field3 = forms.ChoiceField(help_text='long choices list', choices=LONG_CHOICES)
    field4 = forms.TypedChoiceField(help_text='cource to int', coerce=int, choices=CHOICES)

# CharField
# ChoiceField
# TypedChoiceField
# DateField
# DateTimeField
# DecimalField
# DurationField
# EmailField
# FileField
# FilePathField
# FloatField
# ImageField
# IntegerField
# GenericIPAddressField
# MultipleChoiceField
# TypedMultipleChoiceField
# NullBooleanField
# RegexField
# SlugField
# TimeField
# URLField
# UUIDField
