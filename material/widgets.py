from django.forms import widgets


class _IconMixin(object):
    def __init__(self, *args, **kwargs):
        self.prefix_icon = kwargs.pop('prefix_icon', None)
        self.suffix_icon = kwargs.pop('suffix_icon', None)
        super().__init__(*args, **kwargs)


class _AutoInitMixin(object):
    autoinit = None

    def __init__(self, *args, **kwargs):
        self.autoinit = kwargs.pop('autoinit', self.autoinit)
        super().__init__(*args, **kwargs)


class MaterialTextInput(_IconMixin, _AutoInitMixin, widgets.TextInput):
    autoinit = "MDCTextfield"


class MaterialNumberInput(_IconMixin, _AutoInitMixin, widgets.NumberInput):
    autoinit = "MDCTextfield"


class MaterialEmailInput(_IconMixin, _AutoInitMixin, widgets.EmailInput):
    autoinit = "MDCTextfield"


class MaterialURLInput(_IconMixin, _AutoInitMixin, widgets.URLInput):
    autoinit = "MDCTextfield"


class MaterialPasswordInput(_IconMixin, _AutoInitMixin, widgets.PasswordInput):
    autoinit = "MDCTextfield"
