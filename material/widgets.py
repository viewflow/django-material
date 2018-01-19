from django.forms import widgets


class _IconMixin(object):
    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.pop('prefix', None)
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)


class _AutoInitMixin(object):
    autoinit = None

    def __init__(self, *args, **kwargs):
        self.autoinit = kwargs.pop('autoinit', self.autoinit)
        super().__init__(*args, **kwargs)


class TextInput(_IconMixin, _AutoInitMixin, widgets.TextInput):
    autoinit = "MDCTextField"


class NumberInput(_IconMixin, _AutoInitMixin, widgets.NumberInput):
    autoinit = "MDCTextField"


class EmailInput(_IconMixin, _AutoInitMixin, widgets.EmailInput):
    autoinit = "MDCTextField"


class URLInput(_IconMixin, _AutoInitMixin, widgets.URLInput):
    autoinit = "MDCTextField"


class PasswordInput(_IconMixin, _AutoInitMixin, widgets.PasswordInput):
    autoinit = "DMCPasswordField"


class Select(_IconMixin, _AutoInitMixin, widgets.Select):
    autoinit = "DMCSelect"


class InlineCalendar(widgets.DateInput):
    autoinit = "DMCCalendar"
