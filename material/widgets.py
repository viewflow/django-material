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


class MaterialTextInput(_IconMixin, _AutoInitMixin, widgets.TextInput):
    autoinit = "MDCTextField"


class MaterialNumberInput(_IconMixin, _AutoInitMixin, widgets.NumberInput):
    autoinit = "MDCTextField"


class MaterialEmailInput(_IconMixin, _AutoInitMixin, widgets.EmailInput):
    autoinit = "MDCTextField"


class MaterialURLInput(_IconMixin, _AutoInitMixin, widgets.URLInput):
    autoinit = "MDCTextField"


class MaterialPasswordInput(_IconMixin, _AutoInitMixin, widgets.PasswordInput):
    autoinit = "MDCTextField"
