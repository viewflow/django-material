default_app_config = 'material.admin.apps.MaterialAdminConfig'


try:
    from . import modules
    admin = modules.Admin()
except ImportError:
    """
    Ok, karenina is not installed
    """