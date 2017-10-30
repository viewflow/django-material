"""
Settings for Django-Material are all namespaced in the MATERIAL setting.
For example your project's `settings.py` file might look like this:

MATERIAL = {
    'WIDGET_RENDERERS': {
        'django.forms.DateTimeInput': 'myapp.renderers.MyDateTimeRenderer'
    }
}
"""

from copy import deepcopy

from django.conf import settings as django_settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

from material import renderers


DEFAULTS = {
    'AUTOREGISTER': True,
    'FORM_RENDERER': renderers.FormRenderer,
    'WIDGET_RENDERERS': renderers.WIDGET_RENDERERS,
    'FIELD_RENDERERS': renderers.FIELD_RENDERERS,
}


class Settings(object):
    def __init__(self, custom=None):
        if custom is None:
            custom = getattr(django_settings, 'MATERIAL', {})
        self.settings = deepcopy(DEFAULTS)

        if 'FORM_RENDERERS' in custom:
            self.settings['FORM_RENDERERS'] = import_string(custom['FORM_RENDERERS'])

        for key, value in custom.get('WIDGET_RENDERERS', {}):
            widget_class, renderer_class = import_string(key), import_string(value)
            self.settings['WIDGET_RENDERERS'][widget_class] = renderer_class()

        for key, value in custom.get('FIELD_RENDERERS', {}):
            widget, renderer = import_string(key), import_string(value)
            self.settings['FIELD_RENDERERS'][widget] = renderer

    def __getattr__(self, attr):
        if attr not in self.settings:
            raise AttributeError("Invalid Material setting: '%s'" % attr)
        return self.settings[attr]


material_settings = Settings()


def reload_settings(*args, **kwargs):
    global material_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'MATERIAL':
        material_settings = Settings(value)


setting_changed.connect(reload_settings)
