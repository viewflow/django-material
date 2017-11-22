import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fn4_(9z4f8w+3!&(j2x88^ca0m0=s+aj$jp^^cf^3h740xhr3='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = [
    '127.0.0.1'
]

# Application definition
DEV_APPS = (
    'autofixture',
    'template_debug',
)

INSTALLED_APPS = (
    # material apps
    'material',
    'material.frontend',
    'material.admin',

    # standard django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # test apps
    # 'demo.examples.accounting',
    'demo.examples.employees.apps.EmployeesConfig',
    'demo.tests.integration',

    # test admin apps
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.sites',
)

if 'test' not in sys.argv:
    INSTALLED_APPS += DEV_APPS


LOGIN_REDIRECT_URL = '/integration/'


MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SITE_ID = 1

ROOT_URLCONF = 'demo.urls'

WSGI_APPLICATION = 'demo.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'demo', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'material.frontend.context_processors.modules',
            ],
            'builtins': [
                'material.templatetags.material_form',
                'template_debug.templatetags.debug_tags'
            ],
            'debug': True,
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db{}{}.sqlite3'.format(*django.VERSION[:2])),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "demo", "static"),
)

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Django debug toolbar
# http://django-debug-toolbar.readthedocs.io/en/1.4/configuration.html
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': {
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'deploy', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'deploy', 'media')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = 587


if os.environ.get('DEBUG_TOOLBAR'):
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

try:
    from deploy.local_settings import *  # NOQA
except ImportError:
    pass
