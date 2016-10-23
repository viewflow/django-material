from django.conf import settings

def default_config():
    return {
        # configurable
        'ADMIN_NAME': 'Material Admin',
        'ADMIN_HEADER': '<i class="material-icons" style="font-size:80px">settings_applications</i>',
        'FAVICON': settings.STATIC_URL + 'images/favicon.ico',
    }


def get_config(param=None):
    config_key = 'ADMIN_CONFIG'
    if hasattr(settings, config_key):
        config = getattr(settings, config_key, {})
    else:
        config = default_config()
    if param:
        value = config.get(param)
        if value is None:
            value = default_config().get(param)
        return value
    return config
