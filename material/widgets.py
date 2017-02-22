import datetime

from django.conf import settings
from django.utils import formats, six
from django.forms.widgets import Widget
from django.utils.encoding import force_str


class SelectDateWidget(Widget):
    """Wrapper around django.widgets.SelectDateWidget.

    Provides api suitable for template-based rendering
    """

    def __init__(self, widget):  # noqa: D102
        self.widget = widget

    @property
    def date_re(self):
        """Backward compatible date regexp source."""
        if hasattr(self.widget, 'date_re'):
            return self.widget.date_re
        else:
            # django 1.8
            from django.forms.widgets.extra import DATE_RE
            return DATE_RE

    def split_value(self, value):
        """Bit magic for widget value splitting into date components."""
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, six.string_types):
                if settings.USE_L10N:
                    try:
                        input_format = formats.get_format(
                            'DATE_INPUT_FORMATS')[0]
                        v = datetime.datetime.strptime(
                            force_str(value), input_format)
                        year_val, month_val, day_val = v.year, v.month, v.day
                    except ValueError:
                        pass
                else:
                    match = self.re_date.match(value)
                    if match:
                        year_val, month_val, day_val = [
                            int(v) for v in match.groups()
                        ]

        return year_val, month_val, day_val

    def parse_date_fmt(self):
        """List of year/month/day in order according to `DATE_FORMAT`."""
        fmt = formats.get_format('DATE_FORMAT')
        escaped = False
        for char in fmt:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char in 'Yy':
                yield 'year'
            elif char in 'bEFMmNn':
                yield 'month'
            elif char in 'dj':
                yield 'day'

    def none_choice(self, none_value):
        """Value for the empty select option."""
        return [] if self.widget.is_required else [none_value]

    def selects_data(self, value):
        """Content for the rendering select widgets."""
        year_val, month_val, day_val = self.split_value(value)

        year_choices = (
            self.none_choice(self.widget.year_none_value) +
            [(i, i) for i in self.widget.years]
        )

        month_choices = (
            self.none_choice(self.widget.month_none_value) +
            list(six.iteritems(self.widget.months))
        )

        day_choices = (
            self.none_choice(self.widget.day_none_value) +
            [(i, i) for i in range(1, 32)]
        )

        data = {
            'year': {
                'type': 'year',
                'value': year_val,
                'choices': year_choices
            },
            'month': {
                'type': 'month',
                'value': month_val,
                'choices': month_choices
            },
            'day': {
                'type': 'day',
                'value': day_val,
                'choices': day_choices
            },
        }

        for field in self.parse_date_fmt():
            yield data[field]
