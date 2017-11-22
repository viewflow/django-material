import uuid
import os.path
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import Permission
from django.core.validators import MaxLengthValidator
from django.core.files import File
from django.forms.widgets import SelectDateWidget
from django.template import Template
from django.utils import timezone
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


# Core django fields

class BooleanFieldForm(forms.Form):
    description = "BooleanField options"

    field1 = forms.BooleanField(help_text='default')
    field2 = forms.BooleanField(help_text='initial value', initial=True)


class CharFieldForm(forms.Form):
    description = "CharField options"

    field1 = forms.CharField(help_text='default')
    field2 = forms.CharField(help_text='initial value', initial="Initial value")
    field3 = forms.CharField(help_text='length between 5-10', min_length=5, max_length=10)
    field4 = forms.CharField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class ChoiceFieldForm(forms.Form):
    description = "ChoiceField options"
    CHOICES = (
        (None, 'Select a fruit'),
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermeloun'))
    FLOAT_CHOICES = (
        (1.1, 'Perfect'),
        (1.0, 'Good'),
        (0.8, 'Bad'),
    )
    GROUPED_CHOICES = (
        (None, [(7, 'Mikhail')]),
        ('Team 1', [(1, 'Joe'), (2, 'Bob'), (3, 'Marie')]),
        ('Team 2', [(4, 'Anatoliy'), (5, 'Svetlana'), (6, 'Olga')]),
    )
    LONG_CHOICES = ((n, n) for n in range(100))

    field1 = forms.ChoiceField(help_text='default', choices=CHOICES)
    field2 = forms.ChoiceField(help_text='initial value', choices=CHOICES, initial=2)
    field3 = forms.ChoiceField(help_text='float choices', choices=FLOAT_CHOICES)
    field4 = forms.ChoiceField(help_text='groups', choices=GROUPED_CHOICES)
    field5 = forms.ChoiceField(help_text='long choices list', choices=LONG_CHOICES)
    field6 = forms.TypedChoiceField(help_text='cource to int', coerce=int, choices=CHOICES)
    field7 = forms.ChoiceField(help_text='prefix', choices=CHOICES)

    template = Template("""
    {% form %}
        {% part form.field7 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class DateFieldForm(forms.Form):
    description = "DateField options"

    field1 = forms.DateField(help_text='default')
    field2 = forms.DateField(help_text='initial value', initial=timezone.now)
    field3 = forms.DateField(help_text='custom input format', input_formats=['%d %b, %Y'])
    field4 = forms.DateField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class DateTimeFieldForm(forms.Form):
    description = "DateTimeField options"

    field1 = forms.DateTimeField(help_text='default')
    field2 = forms.DateTimeField(help_text='initial value', initial=timezone.now)
    field3 = forms.DateTimeField(help_text='custom input format', input_formats=['%d %b, %Y %H:%M'])
    field4 = forms.DateTimeField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class DecimalFieldForm(forms.Form):
    description = "DecimalField options"

    field1 = forms.DecimalField(help_text='default')
    field2 = forms.DecimalField(help_text='initial value', initial=Decimal('3.141592'))
    field3 = forms.DecimalField(help_text='value between 5-10', min_value=5, max_value=10)
    field4 = forms.DecimalField(help_text='digits restriction 99.999', max_digits=5, decimal_places=3)
    field5 = forms.DecimalField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field5 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class DurationFieldForm(forms.Form):
    description = "DurationField options"

    field1 = forms.DurationField(help_text='default')
    field2 = forms.DurationField(help_text='initial value', initial=timedelta(minutes=1, seconds=12))
    field3 = forms.DurationField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field3 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class EmailFieldForm(forms.Form):
    description = "EmailField options"

    field1 = forms.EmailField(help_text='default')
    field2 = forms.EmailField(help_text='initial value', initial='john@doe.com')
    field3 = forms.EmailField(help_text='length between 10-20', min_length=10, max_length=20)
    field4 = forms.EmailField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class FileFieldForm(forms.Form):
    description = "FileField options"

    field1 = forms.FileField(help_text='default')
    field2 = forms.FileField(help_text='initial value', initial=FakeFieldFile())
    field3 = forms.FileField(help_text='optional', required=False, initial=FakeFieldFile())


class FilePathFieldForm(forms.Form):
    description = "FilePathField options"

    field1 = forms.FilePathField(help_text='default', path=os.path.dirname(__file__))
    field2 = forms.FilePathField(help_text='initial value', path=os.path.dirname(__file__),
                                 initial=__file__, match='^.*\.py$')
    field3 = forms.FilePathField(help_text='recursive directories', path=os.path.dirname(forms.__file__),
                                 recursive=True, allow_folders=True, allow_files=False, match='templates')

    field4 = forms.FilePathField(help_text='prefix', path=os.path.dirname(__file__), required=False)

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class FloatFieldForm(forms.Form):
    description = "FloatField options"

    field1 = forms.FloatField(help_text='default')
    field2 = forms.FloatField(help_text='initial value', initial=2.718282)
    field3 = forms.FloatField(help_text='value between 5-10', min_value=5, max_value=10)
    field4 = forms.FloatField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class ImageFieldForm(forms.Form):
    description = "ImageField options"

    field1 = forms.ImageField(help_text='default')
    field2 = forms.ImageField(help_text='initial value',
                              initial=File(open(os.path.join(os.path.dirname(forms.__file__),
                                                             'static', 'img', 'logo.png')), 'logo.png'))


class IntegerFieldForm(forms.Form):
    description = "IntegerField options"

    field1 = forms.IntegerField(help_text='default')
    field2 = forms.IntegerField(help_text='initial value', initial=42)
    field3 = forms.IntegerField(help_text='value between 5-10', min_value=5, max_value=10)
    field4 = forms.IntegerField(help_text='prefix')
    field5 = forms.IntegerField(
        help_text="range", widget=forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '100'}))

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class GenericIPAddressFieldForm(forms.Form):
    description = "GenericIPAddressField options"

    field1 = forms.GenericIPAddressField(help_text='default')
    field2 = forms.GenericIPAddressField(help_text='initial value', initial='::ffff:192.0.2.1',
                                         unpack_ipv4=True)
    field3 = forms.GenericIPAddressField(help_text='IPv4 only', protocol='IPv4')
    field4 = forms.GenericIPAddressField(help_text='IPv6 only', protocol='IPv6')
    field5 = forms.GenericIPAddressField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field5 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class MultipleChoiceFieldForm(forms.Form):
    description = "MultipleChoiceField options"
    CHOICES = (
        (None, 'Select a fruit'),
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermeloun'))
    FLOAT_CHOICES = (
        (1.1, 'Perfect'),
        (1.0, 'Good'),
        (0.8, 'Bad'),
    )
    LONG_CHOICES = ((n, n) for n in range(100))

    field1 = forms.MultipleChoiceField(help_text='default', choices=CHOICES)
    field2 = forms.MultipleChoiceField(help_text='initial value', choices=CHOICES, initial=[2, 3])
    field3 = forms.MultipleChoiceField(help_text='float choices', choices=FLOAT_CHOICES)
    field4 = forms.MultipleChoiceField(help_text='long choices list', choices=LONG_CHOICES)
    field5 = forms.TypedMultipleChoiceField(help_text='cource to int', coerce=int, choices=CHOICES)
    field6 = forms.MultipleChoiceField(help_text='prefix', choices=CHOICES)

    template = Template("""
    {% form %}
        {% part form.field6 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class NullBooleanFieldForm(forms.Form):
    description = "NullBooleanField options"

    field1 = forms.NullBooleanField(help_text='default')
    field2 = forms.NullBooleanField(help_text='initial value', initial=True)


class RegexFieldForm(forms.Form):
    description = "RegexField options"

    field1 = forms.RegexField(help_text='default [regex=.*]', regex='.*')
    field2 = forms.RegexField(help_text='initial value [regex=test\d]', initial='test1', regex='test\d')
    field3 = forms.RegexField(help_text='length between 5-10 [regex=.*]', regex='.*', min_length=5, max_length=10)
    field4 = forms.RegexField(help_text='prefix [regex=.*]', regex='.*')

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class SlugFieldForm(forms.Form):
    description = "SlugField options"

    field1 = forms.SlugField(help_text='default')
    field2 = forms.SlugField(help_text='initial value', initial="initial_value")
    field3 = forms.SlugField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field3 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class TimeFieldForm(forms.Form):
    description = "TimeField options"

    field1 = forms.TimeField(help_text='default')
    field2 = forms.TimeField(help_text='initial value', initial=timezone.now)
    field3 = forms.TimeField(help_text='custom input format', input_formats=['%H:%M'])
    field4 = forms.TimeField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class URLFieldForm(forms.Form):
    description = "URLField options"

    field1 = forms.URLField(help_text='default')
    field2 = forms.URLField(help_text='initial value', initial="http://viewflow.io")
    field3 = forms.URLField(help_text='length between 10-100', min_length=10, max_length=100)
    field4 = forms.URLField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class UUIDField(forms.Form):
    description = "UUIDField options"

    field1 = forms.UUIDField(help_text='default')
    field2 = forms.UUIDField(help_text='initial value', initial=uuid.uuid4())
    field3 = forms.UUIDField(help_text='prefix')

    template = Template("""
    {% form %}
        {% part form.field3 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


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
    field5 = forms.ModelChoiceField(help_text='prefix', queryset=Permission.objects.all())

    template = Template("""
    {% form %}
        {% part form.field5 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class ModelMultipleChoiceFieldForm(forms.Form):
    description = "ModelMultipleChoiceField options"

    field1 = forms.ModelMultipleChoiceField(help_text='default', queryset=Permission.objects.all())
    field2 = forms.ModelMultipleChoiceField(help_text='initial value', queryset=Permission.objects.all(),
                                            initial=Permission.objects.first)
    field3 = forms.ModelMultipleChoiceField(help_text='to_field_name=codename', queryset=Permission.objects.all(),
                                            to_field_name='name')
    field4 = forms.ModelMultipleChoiceField(help_text='prefix', queryset=Permission.objects.all())

    template = Template("""
    {% form %}
        {% part form.field4 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


# Core django non-default widgets


class PasswordInputForm(forms.Form):
    description = "PasswordInput options"

    field1 = forms.CharField(help_text='default', widget=forms.PasswordInput)
    field2 = forms.CharField(help_text='initial value', widget=forms.PasswordInput,
                             initial="Initial value")
    field3 = forms.CharField(help_text='length between 5-10', widget=forms.PasswordInput,
                             min_length=5, max_length=10)
    field4 = forms.CharField(help_text='render value',
                             widget=forms.PasswordInput(render_value=True))
    field5 = forms.CharField(help_text='prefix', widget=forms.PasswordInput)

    template = Template("""
    {% form %}
        {% part form.field5 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class HiddenInputForm(forms.Form):
    description = "HiddenInput options"

    field1 = forms.CharField(help_text='default', initial="hello!", widget=forms.HiddenInput)


class TextareaForm(forms.Form):
    description = "Textarea options"

    field1 = forms.CharField(help_text='default', widget=forms.Textarea)
    field2 = forms.CharField(help_text='initial value', widget=forms.Textarea,
                             initial="Initial value")
    field3 = forms.CharField(help_text='hard length between 10-100', widget=forms.Textarea,
                             min_length=10, max_length=100)
    field4 = forms.CharField(help_text='soft max length 150', widget=forms.Textarea,
                             validators=[MaxLengthValidator(150)])
    field5 = forms.CharField(help_text='prefix', widget=forms.Textarea)

    template = Template("""
    {% form %}
        {% attr form.field4 'widget' length %}150{% endattr %}
        {% part form.field5 prefix %}<i class="material-icons prefix">insert_invitation</i>{% endpart %}
    {% endform %}
    """)


class RadioSelectForm(forms.Form):
    description = "RadioSelect options"
    CHOICES = (
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermeloun'))

    field1 = forms.ChoiceField(
        help_text='default', choices=CHOICES, widget=forms.RadioSelect)
    field2 = forms.ChoiceField(
        help_text='initial value', choices=CHOICES, widget=forms.RadioSelect, initial=2)
    field3 = forms.TypedChoiceField(
        help_text='cource to int', choices=CHOICES, widget=forms.RadioSelect, coerce=int)
    field4 = forms.ModelChoiceField(
        help_text='model choice radioselect with to_field_name=codename', widget=forms.RadioSelect,
        queryset=Permission.objects.filter(content_type__app_label='frontend'),
        to_field_name='codename', empty_label=None)


class CheckboxSelectMultipleForm(forms.Form):
    description = "CheckboxSelectMultiple options"
    CHOICES = (
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermeloun'))

    field1 = forms.MultipleChoiceField(
        help_text='default', choices=CHOICES, widget=forms.CheckboxSelectMultiple)
    field2 = forms.MultipleChoiceField(
        help_text='initial value', choices=CHOICES, widget=forms.CheckboxSelectMultiple, initial=[2, 3])
    field3 = forms.TypedMultipleChoiceField(
        help_text='cource to int', choices=CHOICES, widget=forms.CheckboxSelectMultiple, coerce=int)
    field4 = forms.ModelMultipleChoiceField(
        help_text='model multichoice with to_field_name=codename, 2 columns',
        widget=forms.CheckboxSelectMultiple,
        queryset=Permission.objects.filter(content_type__app_label__in=['auth', 'frontend']),
        to_field_name='codename')

    template = Template("""
    {% form %}
        {% part form.field4 columns %}2{% endpart %}
    {% endform %}
    """)


class FileInputForm(forms.Form):
    description = "FileInput options"

    field1 = forms.FileField(
        help_text='default', widget=forms.FileInput)
    field2 = forms.FileField(
        help_text='initial value', widget=forms.FileInput, initial=FakeFieldFile())


class SplitHiddenDateTimeWidgetForm(forms.Form):
    description = "SplitHiddenDateTimeWidget options"

    field1 = forms.DateTimeField(
        help_text='initial value', widget=forms.SplitHiddenDateTimeWidget, initial=timezone.now)


class SelectDateWidgetForm(forms.Form):
    description = "SelectDateWidget options"

    field1 = forms.DateField(
        help_text='default', widget=SelectDateWidget)
    field2 = forms.DateField(
        help_text='initial value', widget=SelectDateWidget, initial=timezone.now)
    field3 = forms.DateField(
        help_text='custom empty label', widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day")))
