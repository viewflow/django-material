# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is dual-licensed under AGPL defined in file 'LICENSE' with
# LICENSE_EXCEPTION and the Commercial license defined in file 'COMM_LICENSE',
# which is part of this source code package.

from django.apps import AppConfig
from django.conf import settings


class MaterialConfig(AppConfig):
    """
    Default Material app configuration that automatically installs middleware.
    
    This configuration automatically adds the SiteMiddleware to your settings
    if it's not already included.
    """
    name = "material"
    verbose_name = "Material Design"
    
    def ready(self):
        middleware_path = "material.middleware.SiteMiddleware"
        if middleware_path not in settings.MIDDLEWARE:
            settings.MIDDLEWARE.append(middleware_path)


class MaterialManualConfig(AppConfig):
    """
    Manual Material app configuration without auto middleware setup.
    
    Use this configuration if you prefer to set up middleware manually.
    To use this config, replace 'material' with 'material.apps.MaterialManualConfig'
    in your INSTALLED_APPS setting.
    """
    name = "material"
    verbose_name = "Material Design (Manual Setup)"
    
    def ready(self):
        # Does nothing, allowing for manual middleware setup
        pass