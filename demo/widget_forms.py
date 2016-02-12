import uuid
import os.path
from datetime import timedelta
from decimal import Decimal

from django import forms
from django.contrib.auth.models import Permission
from django.core.files import File
from django.utils import timezone

import demo


class BooleanFieldForm(forms.Form):
    description = "BooleanField options"

    field1 = forms.BooleanField(help_text='default')
    field2 = forms.BooleanField(help_text='initial value', initial=True)


class CharFieldForm(forms.Form):
    description = "CharField options"

    field1 = forms.CharField(help_text='default')
    field2 = forms.CharField(help_text='initial value', initial="Initial value")
    field3 = forms.CharField(help_text='length between 5-10', min_length=5, max_length=10)


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


class DateFieldForm(forms.Form):
    description = "DateField options"

    field1 = forms.DateField(help_text='default')
    field2 = forms.DateField(help_text='initial value', initial=timezone.now)
    field3 = forms.DateField(help_text='custom input format', input_formats=['%d %b, %Y'])


class DateTimeFieldForm(forms.Form):
    description = "DateTimeField options"

    field1 = forms.DateTimeField(help_text='default')
    field2 = forms.DateTimeField(help_text='initial value', initial=timezone.now)
    field3 = forms.DateTimeField(help_text='custom input format', input_formats=['%d %b, %Y %H:%M'])


class DecimalFieldForm(forms.Form):
    description = "DecimalField options"

    field1 = forms.DecimalField(help_text='default')
    field2 = forms.DecimalField(help_text='initial value', initial=Decimal(3.141592))
    field3 = forms.DecimalField(help_text='value between 5-10', min_value=5, max_value=10)
    field4 = forms.DecimalField(help_text='digits restriction 99.999', max_digits=5, decimal_places=3)


class DurationFieldForm(forms.Form):
    description = "DurationField options"

    field1 = forms.DurationField(help_text='default')
    field2 = forms.DecimalField(help_text='initial value', initial=timedelta(minutes=1, seconds=12))


class EmailFieldForm(forms.Form):
    description = "EmailField options"

    field1 = forms.EmailField(help_text='default')
    field2 = forms.EmailField(help_text='initial value', initial='john@doe.com')
    field3 = forms.EmailField(help_text='length between 10-20', min_length=10, max_length=20)


class FileFieldForm(forms.Form):
    description = "FileField options"

    field1 = forms.FileField(help_text='default')
    field2 = forms.FileField(help_text='initial value', initial=File(open(__file__), 'sample.py'))


class FilePathFieldForm(forms.Form):
    description = "FilePathField options"

    field1 = forms.FilePathField(help_text='default', path=os.path.dirname(__file__))
    field2 = forms.FilePathField(help_text='initial value', path=os.path.dirname(__file__),
                                 initial=__file__, match='^.*\.py$')
    field3 = forms.FilePathField(help_text='recursive directories', path=os.path.dirname(demo.__file__),
                                 recursive=True, allow_folders=True, allow_files=False, match='templates')


class FloatFieldForm(forms.Form):
    description = "FloatField options"

    field1 = forms.FloatField(help_text='default')
    field2 = forms.FloatField(help_text='initial value', initial=2.718282)
    field3 = forms.FloatField(help_text='value between 5-10', min_value=5, max_value=10)


class ImageFieldForm(forms.Form):
    description = "ImageField options"

    field1 = forms.ImageField(help_text='default')
    field2 = forms.ImageField(help_text='initial value',
                              initial=File(open(os.path.join(os.path.dirname(demo.__file__),
                                                             'static', 'img', 'logo.png')), 'logo.png'))


class IntegerFieldForm(forms.Form):
    description = "IntegerField options"

    field1 = forms.IntegerField(help_text='default')
    field2 = forms.IntegerField(help_text='initial value', initial=42)
    field3 = forms.IntegerField(help_text='value between 5-10', min_value=5, max_value=10)


class GenericIPAddressFieldForm(forms.Form):
    description = "GenericIPAddressField options"

    field1 = forms.GenericIPAddressField(help_text='default')
    field2 = forms.GenericIPAddressField(help_text='initial value', initial='::ffff:192.0.2.1',
                                         unpack_ipv4=True)
    field3 = forms.GenericIPAddressField(help_text='IPv4 only', protocol='IPv4')
    field4 = forms.GenericIPAddressField(help_text='IPv6 only', protocol='IPv6')


class MultipleChoiceFieldForm(forms.Form):
    description = "MultipleChoiceField options"
    CHOICES = (
        (None, 'Select a fruit'),
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermeloun'))
    LONG_CHOICES = ((n, n) for n in range(100))

    field1 = forms.MultipleChoiceField(help_text='default', choices=CHOICES)
    field2 = forms.MultipleChoiceField(help_text='initial value', choices=CHOICES, initial=[2, 3])
    field3 = forms.MultipleChoiceField(help_text='long choices list', choices=LONG_CHOICES)
    field4 = forms.TypedMultipleChoiceField(help_text='cource to int', coerce=int, choices=CHOICES)


class NullBooleanFieldForm(forms.Form):
    description = "NullBooleanField options"

    field1 = forms.NullBooleanField(help_text='default')
    field2 = forms.NullBooleanField(help_text='initial value', initial=True)


class RegexFieldForm(forms.Form):
    description = "RegexField options"

    field1 = forms.RegexField(help_text='default [regex=.*]', regex='.*')
    field2 = forms.RegexField(help_text='initial value [regex=test\d]', initial='test1', regex='test\d')
    field3 = forms.RegexField(help_text='length between 5-10 [regex=.*]', regex='.*', min_length=5, max_length=10)


class SlugFieldForm(forms.Form):
    description = "SlugField options"

    field1 = forms.SlugField(help_text='default')
    field2 = forms.SlugField(help_text='initial value', initial="initial_value")


class TimeFieldForm(forms.Form):
    description = "TimeField options"

    field1 = forms.TimeField(help_text='default')
    field2 = forms.TimeField(help_text='initial value', initial=timezone.now)
    field3 = forms.TimeField(help_text='custom input format', input_formats=['%H:%M:%S'])


class URLFieldForm(forms.Form):
    description = "URLField options"

    field1 = forms.URLField(help_text='default')
    field2 = forms.URLField(help_text='initial value', initial="http://viewflow.io")
    field3 = forms.URLField(help_text='length between 10-100', min_length=10, max_length=100)


class UUIDField(forms.Form):
    description = "UUIDField options"

    field1 = forms.UUIDField(help_text='default')
    field2 = forms.UUIDField(help_text='initial value', initial=uuid.uuid4())


class ComboFieldForm(forms.Form):
    description = "ComboField options"

    field1 = forms.ComboField(help_text='reference sample',
                              fields=[forms.CharField(max_length=20), forms.EmailField()])


class SplitDateTimeFieldForm(forms.Form):
    description = "SplitDateTimeField options"

    field1 = forms.SplitDateTimeField(help_text='default')
    field2 = forms.SplitDateTimeField(help_text='initial value', initial=timezone.now)
    field3 = forms.SplitDateTimeField(
        help_text='custom input format',
        input_date_formats=['%d %b, %Y'],
        input_time_formats=['%H:%M:%S'])


class ModelChoiceFieldForm(forms.Form):
    description = "ModelChoiceField options"

    field1 = forms.ModelChoiceField(help_text='default', queryset=Permission.objects.all())
    field2 = forms.ModelChoiceField(help_text='initial value', queryset=Permission.objects.all(),
                                    initial=Permission.objects.first)
    field3 = forms.ModelChoiceField(help_text='custom empty label', queryset=Permission.objects.all(),
                                    empty_label="(Nothing)")
    field4 = forms.ModelChoiceField(help_text='to_field_name=codename', queryset=Permission.objects.all(),
                                    to_field_name='codename')


class ModelMultipleChoiceFieldForm(forms.Form):
    description = "ModelMultipleChoiceField options"

    field1 = forms.ModelMultipleChoiceField(queryset=Permission.objects.all())
    field2 = forms.ModelMultipleChoiceField(help_text='initial value', queryset=Permission.objects.all(),
                                            initial=Permission.objects.first)
    field4 = forms.ModelMultipleChoiceField(help_text='to_field_name=codename', queryset=Permission.objects.all(),
                                            to_field_name='name')
